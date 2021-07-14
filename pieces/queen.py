import pygame

from .piece import Piece
import configs

# This is a combination of the rook and bishop pieces

class Queen(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite):
        super().__init__(pygame.image.load("images/queen-piece-white.png"),
                         pygame.image.load("images/queen-piece-black.png"),
                         isWhite,
                         startingsquare)

    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False, ignoreCheck=False):

        # Check that we're not on targetSquare
        if self.squarex == targetSquare[0] and self.squarey == targetSquare[1]:
            return False
        # See if we're moving to a square that's the same distance away on x as it is on y
        # If we are, we're going diagonally
        if abs(self.squarex - targetSquare[0]) == abs(self.squarey - targetSquare[1]):

            # Determine if we're heading in the positive or negative direction along x and y
            directionX = (targetSquare[0]-self.squarex)/abs(self.squarex - targetSquare[0])
            directionY = (targetSquare[1]-self.squarey)/abs(self.squarey - targetSquare[1])
            
            # Check that every square along our path is a valid non-capture move
            for distance in range(1, int(abs(self.squarex-targetSquare[0]))):
                testPosX = self.squarex+directionX*distance
                testPosY = self.squarey+directionY*distance
                
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((testPosX, testPosY), gamePieces, board, ignoreCheck=ignoreCheck):
                    return False
                         
        # Check if we're going horizontally
        elif self.squarey == targetSquare[1]:
            
            # We're going horizontally, check every square between us and the target square along x
            for xpos in range(int(min(self.squarex, targetSquare[0])+1), int(max(self.squarex, targetSquare[0]))):
                
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((xpos, targetSquare[1]), gamePieces, board, ignoreCheck=ignoreCheck):
                    return False
        # Check if we're going vertically
        elif self.squarex == targetSquare[0]:
            # We're going vertically, check every square between us and the target square along y
            for ypos in range(int(min(self.squarey, targetSquare[1])+1), int(max(self.squarey, targetSquare[1]))):
                
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((targetSquare[0], ypos), gamePieces, board, ignoreCheck=ignoreCheck):
                    return False
        # If we're not going horizontally, vertically or diagonally, return False
        else:
            return False

        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture, ignoreCheck=ignoreCheck):
            return False

        # Whatever checks we did passed, return True
        return True
                    
    
