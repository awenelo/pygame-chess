import pygame

from .piece import Piece
import configs

class Bishop(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite):
        super().__init__(pygame.image.load("images/bishop-piece-white.png"),
                         pygame.image.load("images/bishop-piece-black.png"),
                         isWhite,
                         startingsquare)

    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False):
        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture):
            return False

        # Check that we're moving to a square that's the same distance away on x as it is on y
        if abs(self.squarex - targetSquare[0]) != abs(self.squarey - targetSquare[1]):
            return False
        # Determine if we're heading in the positive or negative direction along x and y
        directionX = (targetSquare[0]-self.squarex)/abs(self.squarex - targetSquare[0])
        directionY = (targetSquare[1]-self.squarey)/abs(self.squarey - targetSquare[1])
        # Check that every square along our path is a valid non-capture move
        for distance in range(1, abs(self.squarex-targetSquare[0])):
            testPosX = self.squarex+directionX*distance
            testPosY = self.squarey+directionY*distance
            # For each square, check that we can "exist" in it using the checks in the default isValidMove
            if not super().is_valid_move((testPosX, testPosY), gamePieces, board):
                return False
            

        # All checks have passed, return True
        return True
