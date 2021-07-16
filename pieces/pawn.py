import pygame

from .piece import Piece
from .queen import Queen
from .knight import Knight
from .bishop import Bishop
from .rook import Rook
import configs
from player import Players

class Pawn(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite, hasmoved=False, promotion=None):
        super().__init__(pygame.image.load("images/pawn-piece-white.png"),
                         pygame.image.load("images/pawn-piece-black.png"),
                         isWhite,
                         startingsquare,
                         hasmoved=hasmoved,
                         promotion=promotion)

    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False, ignoreCheck=False, players=Players()):
        # If we're in promotion mode, we can only move to that square
        if self.promotion is not None:
            if targetSquare == self.promotion:
                return True
            else:
                return False
        # Check that we're moving 1 forward and at most 1 to the left or right
        # Figure out if we should be moving in the + or - y direction
        yDirection = [self.white*2-1] + ([(self.white*2-1)*2] if not self.hasMoved else [])

        # Check that we're moving in the correct direction
        if self.squarey - targetSquare[1] not in yDirection:
            return False

        # If we're moving horizontally, check that we're not moving 2 forwards/backwards
        if self.squarey - targetSquare[1] != yDirection[0] and self.squarex != targetSquare[0]:
            return False

        # If we're capturing, allow us to go -1 or +1 in the x direction, otherwise force us to only go straight up/down
        if not capture and self.squarex != targetSquare[0]:
            return False
        # Check that we're moving -1 to 1 in the x direction
        elif abs(self.squarex-targetSquare[0]) > 1:
            return False

        # Store if we can move to the targetSquare if we're capturing, and if we're not capturing
        noCaptureTargetSquare = super().is_valid_move(targetSquare, gamePieces, board, capture=False)
        captureTargetSquare = super().is_valid_move(targetSquare, gamePieces, board, capture=True)

        # If we're moving forwards, check that we can move without capturing
        if self.squarex == targetSquare[0] and not noCaptureTargetSquare:
            return False
        

        # If we're moving horizontally, check that we need to capture to move
        if self.squarex != targetSquare[0]:
            if not(captureTargetSquare and not noCaptureTargetSquare):
                return False

        # Check that Piece doesn't have something against moving here
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture, ignoreCheck=ignoreCheck):
            return False

        # All checks have passed, return True
        return True
    # Adds promotions to move
    def move(self, squarex, squarey, gamePieces, capture=True, countMovement=False):
        super().move(squarex, squarey, gamePieces, capture=capture, countMovement=countMovement)
        # Check if we're at the top or bottom of the board and this move is permentant
        if countMovement and self.squarey in [1,8]:
            # If we're at the top or bottom, remove us and add a new queen to pieces
            gamePieces.remove(self)
            gamePieces.add(Queen((3,9), self.white, hasmoved=True, promotion=(self.squarex, self.squarey)))
            gamePieces.add(Knight((4,9), self.white, hasmoved=True, promotion=(self.squarex, self.squarey)))
            gamePieces.add(Bishop((5,9), self.white, hasmoved=True, promotion=(self.squarex, self.squarey)))
            gamePieces.add(Rook((6,9), self.white, hasmoved=True, promotion=(self.squarex, self.squarey)))
            return False
        return True
