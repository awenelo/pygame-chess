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
    
    # Create 2 pieces and add them to the group
    gamePieces.add(pieces.Piece("pieces/images/default-piece.png", "pieces/images/default-piece-selected.png", (0,0)))
    gamePieces.add(pieces.Piece("pieces/images/default-piece.png", "pieces/images/default-piece-selected.png", (2,2)))

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a piece has been selected, if no piece has been selected, selectedPiece will resolve to be False
                if selectedPiece:
                    # Move selectedPiece to the new location, if the move is valid and selectedPiece is not None
                    # Determine which square we're moving to
                    targetSquare = (
                        event.pos[0]//configs.SQUARE_SIZE,
                        event.pos[1]//configs.SQUARE_SIZE
                        )
                    # Check if the square we're moving to is valid
                    if selectedPiece.isValidMove(targetSquare, gamePieces):
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

        # Clear the screen
        screen.fill((255,255,255))
        
        # Draw the game pieces
        gamePieces.draw(screen)

        # Show the screen
        pygame.display.flip()

        # Wait for the remainder of the frame
        clock.tick(configs.FRAMERATE)

if __name__ == "__main__":
    main()
