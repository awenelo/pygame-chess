import pygame

from .piece import Piece
import configs

class Rook(Piece):
    # Overwrite the __init__ function to pass different images without input from main.py
    def __init__(self, startingsquare, isWhite):
        super().__init__(pygame.image.load("images/rook-piece-white.png"),
                         pygame.image.load("images/rook-piece-black.png"),
                         isWhite,
                         startingsquare)
    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False):
        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture):
            return False
        
        # Check that the piece is on the board or if it's moving to the board, if it's not, make the move valid no matter what
        if not board.is_on_board(self.rect.center) or not board.is_on_board((targetSquare[0]*configs.SQUARE_SIZE, targetSquare[1]*configs.SQUARE_SIZE)):
            return True

        # Check that we're moving to a square with the same horizontal or vertical position
        if not(self.squarex == targetSquare[0] or self.squarey == targetSquare[1]):
            return False

        # Determine if we're going horizontally or vertically
        if self.squarey == targetSquare[1]:
            # We're going horizontally, check every square between us and the target square along x
            for xpos in range(min(self.squarex, targetSquare[0])+1, max(self.squarex, targetSquare[0])):
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((xpos, targetSquare[1]), gamePieces, board):
                    return False
        else:
            # We're going vertically, check every square between us and the target square along y
            for ypos in range(min(self.squarey, targetSquare[1])+1, max(self.squarey, targetSquare[1])):
                # For each square, check that we can "exist" in it using the checks in the default isValidMove
                if not super().is_valid_move((targetSquare[0], ypos), gamePieces, board):
                    return False
        

        # All checks passed, return True
        return True
