import pygame

from .piece import Piece
import configs

class Rook(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite, hasmoved=False):
        super().__init__(pygame.image.load("images/rook-piece-white.png"),
                         pygame.image.load("images/rook-piece-black.png"),
                         isWhite,
                         startingsquare,
                         hasmoved=hasmoved)
        
    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False, ignoreCheck=False):
        # Check that we're moving to a square with the same horizontal or vertical position
        if not(self.squarex == targetSquare[0] or self.squarey == targetSquare[1]):
            return False

        # Determine if we're going horizontally or vertically
        if self.squarey == targetSquare[1]:
            # We're going horizontally, check every square between us and the target square along x
            for xpos in range(min(self.squarex, targetSquare[0])+1, max(self.squarex, targetSquare[0])):
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((xpos, targetSquare[1]), gamePieces, board, ignoreCheck=True):
                    return False
        else:
            # We're going vertically, check every square between us and the target square along y
            for ypos in range(min(self.squarey, targetSquare[1])+1, max(self.squarey, targetSquare[1])):
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((targetSquare[0], ypos), gamePieces, board, ignoreCheck=True):
                    return False
                
        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture):
            return False
        
        # All checks passed, return True
        return True
