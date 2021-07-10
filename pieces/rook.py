import pygame

from .piece import Piece

class Rook(Piece):
    # Overwrite the __init__ function to pass different images without input from main.py
    def __init__(self, startingsquare):
        super().__init__("images/rook-piece.png",
                         "images/rook-piece-selected.png",
                         startingsquare)
    # Function to check if move is leagal, overwrites the default function
    def isValidMove(self, targetSquare, gamePieces, board):
        # Check that the piece is on the board, if it's not, make the move invalid no matter what
        if not board.is_on_board(self.rect.center):
            return False

        # Check that we're moving to a square with the same horizontal or vertical position
        if self.squarex == targetSquare[0] or self.squarey == targetSquare[1]:
            return True

        # All checks failed, return False
        return False
