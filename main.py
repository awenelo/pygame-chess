# pygame-chess
# A. awenelo
# Chess using pygame

# Import exernal modules
import pygame

# Import internal modules
from board import Board
import configs
from menu import Menu
from game import Game

def main():
    # Initialize all pygame modules
    pygame.init()
    
    # Set the screen size
    screen = pygame.display.set_mode((configs.WIDTH, configs.HEIGHT))

    # Create a menu object
    menu = Menu()

    # Go to the main menu
    menu.main_menu()

    # Create a game object
    game = Game(menu)

    # Create a board object, and pass it the correct width and height, images and center is on the screen
    board = Board(
        configs.SQUARE_COUNT_WIDTH,
        configs.SQUARE_COUNT_HEIGHT,
        "images/board-tile-white.png",
        "images/board-tile-black.png",
        "images/board-tile-white-selected.png",
        "images/board-tile-black-selected.png",
        "images/board-tile-white-capturable.png",
        "images/board-tile-black-capturable.png",
        ((configs.WIDTH//configs.SQUARE_SIZE-configs.SQUARE_COUNT_WIDTH)//2,
         (configs.HEIGHT//configs.SQUARE_SIZE-configs.SQUARE_COUNT_HEIGHT)//2
        )
    )

    # Create a clock object
    clock = pygame.time.Clock()

    # Create a variable to store the selected piece
    selectedPiece = []

    # Store if we should show the amount of time since the last frame
    showTimeSinceTick = False

    # Main loop
    while True:
        # Store if a move was made this loop
        moveMade = False
        if game.onlineGame:
            game.recorder.moveMade

        # Wait for the next frame
        timeSinceTick = clock.tick(configs.FRAMERATE)
        
        # Event loop, fetch all events and check for certain events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If there's a quit event, quit and raise SystemExit to stop execution
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse click is a scroll, ignore the click
                if event.button not in [1,2,3]:
                    continue
                # If we're in a game and the menu doesn't want to use the click,
                if (not menu.mouse_down(event.pos, game)) and game.inGame:
                    # Check if a piece has been selected, if no piece has been selected, selectedPiece will resolve to be False
                    if len(selectedPiece)>0:
                        # Fix selectedPiece in it's current positon, if the move is valid and selectedPiece is not None
                        # Determine which square we're moving to
                        targetSquare = (
                            selectedPiece[0].rect.x//configs.SQUARE_SIZE,
                            selectedPiece[0].rect.y//configs.SQUARE_SIZE
                            )
                        # Check if the square we're moving to is valid
                        if game.players.is_valid_move(game, selectedPiece[0], targetSquare, game.gamePieces, board, capture=True):                  
                            # If so, move to the square
                            game.players.move(selectedPiece[0], game.recorder, board, targetSquare[0], targetSquare[1], game.gamePieces, countMovement=True)

                            # Store that we've made a move
                            moveMade = True

                        # Set the piece to have the deselected image, then clear the selected piece
                        selectedPiece[0].deselect()
                        selectedPiece.pop(0)

                        # Clear the board highlights
                        board.remove_highlights()

                        # If there's still a piece in selectedPiece, probably due to an error, select that one
                        # Repeat until we select one with legal moves
                        while len(selectedPiece)>0:
                            selectedPiece[0].select()
                            board.remove_highlights()
                            if game.players.highlight_moves(game, selectedPiece[0], game.gamePieces, board):
                                break
                            selectedPiece[0].deselect()
                            selectedPiece.pop(0)
                    else:
                        # We don't have a selected piece, so select one if possible
                        # Determine which piece the mouse is over, and set selectedPiece to that
                        # If there are multiple possible pieces, use the first one
                        selectedPiece = game.gamePieces.spriteCollidedWithPoint(event.pos)

                        # If we selected a piece (selectedPiece != None), set the piece to be selected and highlight legal moves
                        # Repeat until we select one with legal moves
                        while len(selectedPiece)>0:
                            selectedPiece[0].select()
                            board.remove_highlights()
                            if game.players.highlight_moves(game, selectedPiece[0], game.gamePieces, board):
                                break
                            selectedPiece[0].deselect()
                            selectedPiece.pop(0)
            elif event.type == pygame.KEYDOWN:
                # If there is a key pushed, check if it's crtl-D, if it is, enable the time since the last frame
                if event.key == pygame.K_d and (event.mod & pygame.KMOD_CTRL):
                    showTimeSinceTick = not showTimeSinceTick
                # Otherwise, check if the recorder wants key presses
                elif game.onlineGame:
                    if game.recorder.status == "get_key":
                        game.recorder.add_char(event.unicode, menu, backspace=event.key == pygame.K_BACKSPACE)
                        
        # If there's no selected piece, and we're in a game, highlight the square the mouse is over, if the square has a piece with valid moves
        if game.inGame and len(selectedPiece) == 0:
            mousePos = pygame.mouse.get_pos()
            # Get the pieces the mouse is over
            for piece in game.gamePieces.spriteCollidedWithPoint(mousePos):
                # Check if there's a move that can be highlighted
                if game.players.highlight_moves(game, piece, game.gamePieces, board):
                    # If there is, clear the highlights and highlight the square the mouse is over
                    board.remove_other_highlight_points(mousePos)
                    board.highlight_point(mousePos)
                    # Then break, to skip the else block below
                    break
            else:
                # If no piece that the mouse is over has a valid move, clear all highlights
                board.remove_highlights()

        # Update the game pieces
        game.gamePieces.update(game.gamePieces, board, moveMade or (False if not game.onlineGame else game.recorder.moveMade), players=game.players)

        # Check if a king is in check, and report it to the server
        if moveMade and game.onlineGame:
            for king in game.gamePieces.get_kings(False):
                if king.checkmate:
                    game.recorder.request_lose(game, menu, False)
                    break
            for king in game.gamePieces.get_kings(True):
                if king.checkmate:
                    game.recorder.request_lose(game, menu, True)
                    break
        
        # Clear the screen
        screen.fill((255,255,255))
        
        # Draw the board
        board.draw(screen, pygame.mouse.get_pos() if len(selectedPiece) == 0 else selectedPiece[0].rect.center, nameSquare=game.inGame)


        # Update the players
        game.players.update(game.gamePieces)

        # Draw the game pieces
        game.gamePieces.draw(screen, selectedPiece=selectedPiece)

        # Draw the player information
        game.players.draw(screen, game)

        # Draw the selectedPiece above everything else, if there is a selected piece
        if len(selectedPiece)>0:
            selectedPiece[0].draw(screen)
            
        # No matter what,
        # Update the game, then draw anything for it
        game.update()
        game.draw(screen)
        

        # Update the menu, then draw it
        menu.update()
        menu.draw(screen)

        # Draw the amount of ms since the last frame in the bottom left, if we should
        if showTimeSinceTick:
            txt = pygame.font.Font(configs.FONT, 25).render(str(timeSinceTick), True, (0,0,0))
            txt_rect = txt.get_rect()
            txt_rect.right = configs.WIDTH
            txt_rect.top = 0
            screen.blit(txt, txt_rect)

        # Show the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()
