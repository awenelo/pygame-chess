import pygame

from .piece import Piece
import configs

class King(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite):
        super().__init__(pygame.image.load("images/king-piece-white.png"),
                         pygame.image.load("images/king-piece-black.png"),
                         isWhite,
                         startingsquare)

    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False):
        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture):
            return False

        # Check that we're moving to a square that's at most +1/-1 away in both directions
        # That's the only check.
        if abs(self.squarex-targetSquare[0])>1 or abs(self.squarey-targetSquare[1])>1:
            return False

        # The check has passed, return True
        return True
