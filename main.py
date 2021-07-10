# pygame-chess
# A. awenelo
# Chess using pygame

# Import exernal modules
import pygame

# Import internal modules
from board import Board
import pieces
import configs

def main():
    # Initialize all pygame modules
    pygame.init()
    
    # Set the screen size
    screen = pygame.display.set_mode((configs.WIDTH, configs.HEIGHT))

    # Create a group to store game pieces
    gamePieces = pieces.PieceGroup()
    
    # Create 4 pieces and add them to the group
    gamePieces.add(pieces.Piece("images/default-piece.png", "images/default-piece-selected.png", (0,0)))
    gamePieces.add(pieces.Piece("images/default-piece.png", "images/default-piece-selected.png", (0,9)))
    gamePieces.add(pieces.Rook((8,1)))
    gamePieces.add(pieces.Piece("images/default-piece.png", "images/default-piece-selected.png", (9,9)))

    # Create a board object, and pass it the correct width and height, images and center is on the screen
    board = Board(
        configs.SQUARE_COUNT_WIDTH,
        configs.SQUARE_COUNT_HEIGHT,
        "images/board-tile-white.png",
        "images/board-tile-black.png",
        "images/board-tile-white-selected.png",
        "images/board-tile-black-selected.png",
        ((configs.WIDTH-configs.SQUARE_SIZE*configs.SQUARE_COUNT_WIDTH)//2,
         (configs.HEIGHT-configs.SQUARE_SIZE*configs.SQUARE_COUNT_HEIGHT)//2
        )
    )

    # Create a clock object
    clock = pygame.time.Clock()

    # Create a variable to store the selected piece, set it to None for now
    selectedPiece = None

    # Main loop
    while True:
        # Event loop, fetch all events and check for certain events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If there's a quit event, quit and raise SystemExit to stop execution
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a piece has been selected, if no piece has been selected, selectedPiece will resolve to be False
                if selectedPiece:
                    # Move selectedPiece to the new location, if the move is valid and selectedPiece is not None
                    # Determine which square we're moving to
                    targetSquare = (
                        event.pos[0]//configs.SQUARE_SIZE,
                        event.pos[1]//configs.SQUARE_SIZE
                        )
                    # Check if the square we're moving to is valid
                    if selectedPiece.isValidMove(targetSquare, gamePieces, board):
                        # If so, move to the square
                        selectedPiece.move(targetSquare[0], targetSquare[1])

                    # Set the piece to have the deselected image, then clear the selected piece
                    selectedPiece.deselect()
                    selectedPiece = None
                else:
                    # We don't have a selected piece, so select one if possible
                    # Determine which piece the mouse is over, and set selectedPiece to that
                    selectedPiece = gamePieces.spriteCollidedWithPoint(event.pos)

                    # If we selected a piece (selectedPiece != None), set the piece to be selected
                    if selectedPiece:
                        selectedPiece.select()
            elif event.type == pygame.MOUSEMOTION:
                # Highlight the square the mouse is hovering over/dragging over
                board.highlight_point(event.pos)

                # Dehighlight every other square
                board.remove_other_highlight_points(event.pos)

        # Clear the screen
        screen.fill((255,255,255))

        # Draw the board
        board.draw(screen)
        
        # Draw the game pieces
        gamePieces.draw(screen)

        # Show the screen
        pygame.display.flip()

        # Wait for the remainder of the frame
        clock.tick(configs.FRAMERATE)

if __name__ == "__main__":
    main()
