# pygame-chess
# A. awenelo
# Chess using pygame

# Import exernal modules
import pygame

# Import internal modules
from board import Board
import pieces
import configs
from player import Player, Players
from PGN_recorder import Recorder

def main():
    # Initialize all pygame modules
    pygame.init()
    
    # Set the screen size
    screen = pygame.display.set_mode((configs.WIDTH, configs.HEIGHT))

    # Create a group to store game pieces
    gamePieces = pieces.PieceGroup()
    
    # Create pieces
    ##gamePieces.add(pieces.Piece(
    ##    pygame.image.load("images/default-piece-white.png"),
    ##    pygame.image.load("images/default-piece-black.png"),
    ##    False,
    ##    (0,0)))
    ##gamePieces.add(pieces.Piece(
    ##    pygame.image.load("images/default-piece-white.png"),
    ##    pygame.image.load("images/default-piece-black.png"),
    ##    True, (9,9)))
    gamePieces.add(pieces.Rook((1,1), False))
    gamePieces.add(pieces.Rook((8,1), False))
    gamePieces.add(pieces.Rook((1,8), True))
    gamePieces.add(pieces.Rook((8,8), True))
    gamePieces.add(pieces.Bishop((3,1), False))
    gamePieces.add(pieces.Bishop((6,1), False))
    gamePieces.add(pieces.Bishop((3,8), True))
    gamePieces.add(pieces.Bishop((6,8), True))
    gamePieces.add(pieces.Queen((4,1), False))
    gamePieces.add(pieces.Queen((4,8), True))
    gamePieces.add(pieces.King((5,1), False))
    gamePieces.add(pieces.King((5,8), True))
    gamePieces.add(pieces.Knight((2,1), False))
    gamePieces.add(pieces.Knight((7,1), False))
    gamePieces.add(pieces.Knight((2,8), True))
    gamePieces.add(pieces.Knight((7,8), True))
    for position in range(1,9):
        gamePieces.add(pieces.Pawn((position, 2), False))
        gamePieces.add(pieces.Pawn((position, 7), True))
        
    # Create players and add them to a list of players
    players = Players()
    players.add(Player(1))
    players.add(Player(0))

    # Create a recorder object
    recorder = Recorder()

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

    # Main loop
    while True:
        # Store if a move was made this loop
        moveMade = False
        
        # Event loop, fetch all events and check for certain events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If there's a quit event, quit and raise SystemExit to stop execution
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a piece has been selected, if no piece has been selected, selectedPiece will resolve to be False
                if len(selectedPiece)>0:
                    # Fix selectedPiece in it's current positon, if the move is valid and selectedPiece is not None
                    # Determine which square we're moving to
                    targetSquare = (
                        selectedPiece[0].rect.x//configs.SQUARE_SIZE,
                        selectedPiece[0].rect.y//configs.SQUARE_SIZE
                        )
                    # Check if the square we're moving to is valid
                    if players.is_valid_move(selectedPiece[0], targetSquare, gamePieces, board, capture=True):                  
                        # If so, move to the square
                        players.move(selectedPiece[0], recorder, board, targetSquare[0], targetSquare[1], gamePieces, countMovement=True)

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
                        if players.highlight_moves(selectedPiece[0], gamePieces, board):
                            break
                        selectedPiece[0].deselect()
                        selectedPiece.pop(0)
                else:
                    # We don't have a selected piece, so select one if possible
                    # Determine which piece the mouse is over, and set selectedPiece to that
                    # If there are multiple possible pieces, use the first one
                    selectedPiece = gamePieces.spriteCollidedWithPoint(event.pos)

                    # If we selected a piece (selectedPiece != None), set the piece to be selected and highlight legal moves
                    # Repeat until we select one with legal moves
                    while len(selectedPiece)>0:
                        selectedPiece[0].select()
                        board.remove_highlights()
                        if players.highlight_moves(selectedPiece[0], gamePieces, board):
                            break
                        selectedPiece[0].deselect()
                        selectedPiece.pop(0)

            elif event.type == pygame.KEYDOWN:
                # Check if the key is escape - cancel the move
                if event.key == pygame.K_ESCAPE:
                    # If it is, clear the selected piece, if there's a piece selected
                    if len(selectedPiece)>0:
                        selectedPiece[0].deselect()
                        selectedPiece.pop(0)
                        
                    # Clear the board highlights
                    board.remove_highlights()
                    
                    # If there's still a piece in selectedPiece, probably due to an error, select that one
                    # Repeat until we select one with legal moves
                    while len(selectedPiece)>0:
                        selectedPiece[0].select()
                        board.remove_highlights()
                        if players.highlight_moves(selectedPiece[0], gamePieces, board):
                            break
                        selectedPiece[0].deselect()
                        selectedPiece.pop(0)
                        
                # Check if the key is return - do the move
                elif event.key == pygame.K_RETURN:
                    if len(selectedPiece)>0:
                        # Fix selectedPiece in it's current positon, if the move is valid and selectedPiece is not None
                        # Determine which square we're moving to
                        targetSquare = (
                            selectedPiece[0].rect.x//configs.SQUARE_SIZE,
                            selectedPiece[0].rect.y//configs.SQUARE_SIZE
                            )
                        # Check if the square we're moving to is valid
                        if selectedPiece[0].is_valid_move(targetSquare, gamePieces, board, capture=True):
                            # If so, move to the square
                            selectedPiece[0].move(targetSquare[0], targetSquare[1], gamePieces)

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
                            if players.highlight_moves(selectedPiece[0], gamePieces, board):
                                break
                            selectedPiece[0].deselect()
                            selectedPiece.pop(0)
        # If there's no selected piece, highlight the square the mouse is over, if the squarehas a piece with valid moves
        if len(selectedPiece) == 0:
            mousePos = pygame.mouse.get_pos()
            # Get the pieces the mouse is over
            for piece in gamePieces.spriteCollidedWithPoint(mousePos):
                # Check if there's a move that can be highlighted
                if players.highlight_moves(piece, gamePieces, board):
                    # If there is, clear the highlights and highlight the square the mouse is over
                    board.remove_other_highlight_points(mousePos)
                    board.highlight_point(mousePos)
                    # Then break, to skip the else block below
                    break
            else:
                # If no piece that the mouse is over has a valid move, clear all highlights
                board.remove_highlights()
        # Update the game pieces
        gamePieces.update(gamePieces, board, moveMade, players=players)

        # Update the players
        players.update(gamePieces)
        
        # Clear the screen
        screen.fill((255,255,255))

        # Draw the board
        board.draw(screen, pygame.mouse.get_pos() if len(selectedPiece) == 0 else selectedPiece[0].rect.center)
        
        # Draw the game pieces
        gamePieces.draw(screen)

        # Draw the player information
        players.draw(screen)

        # Re-draw the selectedPiece above everything else, if there is a selected piece
        if len(selectedPiece)>0:
            selectedPiece[0].draw(screen)

        # Show the screen
        pygame.display.flip()

        # Wait for the remainder of the frame
        clock.tick(configs.FRAMERATE)

if __name__ == "__main__":
    main()
