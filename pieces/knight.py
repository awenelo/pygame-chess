import pygame

from .piece import Piece
import configs
from player import Players

class Knight(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite, hasmoved=False, promotion=None):
        super().__init__(pygame.image.load("images/knight-piece-white.png"),
                         pygame.image.load("images/knight-piece-black.png"),
                         isWhite,
                         startingsquare,
                         hasmoved=hasmoved,
                         promotion=promotion)
        # Change our name to "N"
        self.name = "N"

    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False, ignoreCheck=False, players=Players()):
        # If we're in promotion mode, we can only move to that square
        if self.promotion is not None:
            if targetSquare == self.promotion:
                return True
            else:
                return False
        # Check that our y difference is 1 or 2
        if abs(self.squarey-targetSquare[1]) not in [1,2]:
            return False
        
        # Check that the square we're moving to is either 1 square away in one direction and 2 squares away in the other
        if abs(self.squarex-targetSquare[0]) != [1,2][(([1,2].index(abs(self.squarey-targetSquare[1])))+1) % 2]:
            return False

        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture, ignoreCheck=ignoreCheck):
            return False

        # All checks have passed, return True
        return True
