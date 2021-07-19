import pygame

from .piece import Piece
from player import Players
import configs

class King(Piece):
    # Overwrite the __init__ function to pass different images
    def __init__(self, startingsquare, isWhite, hasmoved=False, promotion=None):
        super().__init__(pygame.image.load("images/king-piece-white.png"),
                         pygame.image.load("images/king-piece-black.png"),
                         isWhite,
                         startingsquare,
                         hasmoved=hasmoved,
                         promotion=promotion)
        # Store the white and black check images
        self.whiteCheckImage = pygame.transform.smoothscale(
            pygame.image.load("images/king-piece-white-check.png"),
            (configs.SQUARE_SIZE, configs.SQUARE_SIZE)
            )
        self.blackCheckImage = pygame.transform.smoothscale(
            pygame.image.load("images/king-piece-black-check.png"),
            (configs.SQUARE_SIZE, configs.SQUARE_SIZE)
            )

        # Store the white and black checkmate images
        self.whiteCheckmateImage = pygame.transform.smoothscale(
            pygame.image.load("images/king-piece-white-checkmate.png"),
            (configs.SQUARE_SIZE, configs.SQUARE_SIZE)
            )
        self.blackCheckmateImage = pygame.transform.smoothscale(
            pygame.image.load("images/king-piece-black-checkmate.png"),
            (configs.SQUARE_SIZE, configs.SQUARE_SIZE)
            )

        # Store that we are a king
        self.isKing = True

        # Store if we're in check/checkmate
        self.incheck = False
        self.checkmate = False

        # Change our name to "K"
        self.name = "K"

    # Function to check if move is leagal, overwrites the default function
    def is_valid_move(self, targetSquare, gamePieces, board, capture=False, ignoreCheck=False, players=Players()):
        # If we're in promotion mode, we can only move to that square
        if self.promotion is not None:
            if targetSquare == self.promotion:
                return True
            else:
                return False
            
        # Check that Piece doesn't have something against moving here, ignoreCheck is always True, since we have our own check handling code
        if not super().is_valid_move(targetSquare, gamePieces, board, capture=capture, ignoreCheck=True):
            return False

        # Check that we're moving to a square that's at most +1/-1 away in both directions
        if abs(self.squarex-targetSquare[0])>1 or abs(self.squarey-targetSquare[1])>1:
            # Check if we're moving to a castle position - 2 squares left or right, haven't moved and same square vertically
            if (not self.hasMoved) and self.squarey==targetSquare[1] and abs(self.squarex-targetSquare[0])==2:
                # If we're on a square we can castle to, check that the rook is still in place, and can move to the correct square
                for piece in gamePieces:
                    if piece.name == "R" and piece.white == self.white and piece.hasMoved == False and piece.squarex == (8 if self.squarex-targetSquare[0]<0 else 1):
                        castlingRook = piece
                        break
                else:
                    # If the rook we want to castle with has moved, the the move is not valid
                    return False
                # Check that the square 1 to our right/left is a valid move and would not put us in check
                if not self.is_valid_move((targetSquare[0]+((self.squarex-targetSquare[0])//2), targetSquare[1]), gamePieces, board, capture=False, ignoreCheck=ignoreCheck):
                    return False

                # Check that the rook can move to the square 1 to our right/left - note that this will return False if the king is in check, as a castling move can't happen in check
                if not castlingRook.is_valid_move((targetSquare[0]+((self.squarex-targetSquare[0])//2), targetSquare[1]), gamePieces, board, capture=False, ignoreCheck=ignoreCheck):
                    return False

                # If we can castle, do the rest of the checks, forcing capture False, as a castling move can't capture
                capture = False
            else:
                return False
        
        # If we're told to ignore check, return True since the check for if we would be in check is the last check
        if ignoreCheck:
            return True
        
        # Check that the square we're moving to won't put us in check
        # For each piece, check if moving to our square is a valid move for them
        # If it is, then we're in check
        # Move us to target square, to simulate our presence there and store where we were before
        pastSquare = (self.squarex, self.squarey)
        self.squarex, self.squarey = targetSquare
        for sprite in gamePieces.sprites():
            # If the piece is on our side, skip checking any further
            if sprite.white == self.white:
                continue

            # Check if the sprite is a king, if so, we need to pass ignoreCheck
            ignoreCheckDict = {}
            if sprite.isKing:
                ignoreCheckDict["ignoreCheck"] = True
            if sprite.is_valid_move(targetSquare, gamePieces, board, capture=True, **ignoreCheckDict):
                # If it is a valid move for another piece, we can't move to that square
                # Move us back
                self.squarex, self.squarey = pastSquare
                return False
        # We're not going to be in check, move us back
        self.squarex, self.squarey = pastSquare
        
        # The checks have passed, return True
        return True

    # Overwrite move() to castle if we're castling
    def move(self, squarex, squarey, gamePieces, capture=True, countMovement=False):
        # Check if we're castling - moving more than 1 square in the x direction
        # If we are, find the rook we're castling with and move it to the correct position
        if abs(self.squarex-squarex)>1:
            for piece in gamePieces:
                if piece.name == "R" and piece.white == self.white and piece.hasMoved == False and piece.squarex == (8 if self.squarex-squarex<0 else 1):
                    castlingRook = piece
                    break
            else:
                return super().move(squarex, squarey, gamePieces, capture=capture, countMovement=countMovement)

            # Move the rook to the square next to us
            castlingRook.move(self.squarex-(self.squarex-squarex)//2, squarey, gamePieces, capture=False, countMovement=True)

            # Then move to the target square
            return super().move(squarex, squarey, gamePieces, capture=capture, countMovement=countMovement)
        # If we aren't castling, make a normal move
        return super().move(squarex, squarey, gamePieces, capture=capture, countMovement=countMovement)

    # Overwrite update() to check if we're in check
    def update(self, gamePieces, board, moveMade, players=Players()):
        # Do Piece.update()
        super().update(gamePieces, board, moveMade)
        # If a piece has moved, check for if we're in check
        if moveMade:
            # Clear our check state
            self.incheck = False
            self.checkmate = False
            # Store a list of the pieces that can capture us
            threats = []
            self.image = self.whiteImage if self.white else self.blackImage

            # Use in_check to check if we're in check
            threats = self.in_check((self.squarex, self.squarey), gamePieces, board, players)

            # If there is a threat, set us to incheck
            self.incheck = len(threats)>0

            # If we're in check, check if there's an escape
            if self.incheck:
                # Assume there isn't an escape
                self.checkmate = True
                for xdiff in [-1, 0, 1]:
                    for ydiff in [-1, 0, 1]:
                        if self.is_valid_move((self.squarex+xdiff, self.squarey+ydiff), gamePieces, board, capture=True):
                            # If there is an escape, record that there was an escape and break
                            self.checkmate = False
                            break
                # If there's no escape, check if the threat can be removed, or we can block the threat
                if self.checkmate:
                    # We can only remove 1 threat, if there's multiple, we're in checkmate no matter what
                    if len(threats)>0 and not len(threats)>1:
                        for sprite in gamePieces.sprites():
                            # Check if the piece is on our side
                            if sprite.white == self.white:
                                # Check if the piece can move to the threat
                                if sprite.is_valid_move((threats[0].squarex, threats[0].squarey), gamePieces, board, capture=True):
                                    # If the piece can capture it, cancel being in checkmate, set our image to check and exit
                                    self.checkmate = False
                                    break
                                # Check that there's not a square we can move to to cancel check
                                for boardTile in board.boardGroup.sprites():
                                    if sprite.is_valid_move((boardTile.squarex, boardTile.squarey), gamePieces, board, capture=True):
                                        # If it's a valid move, create a copy of gamePieces, with the sprite in both the new and old positions
                                        gamePiecesCopy = gamePieces.copy()
                                        spriteCopy = sprite.copy()
                                        spriteCopy.move(boardTile.squarex, boardTile.squarey, gamePiecesCopy, capture=False)
                                        gamePiecesCopy.add(spriteCopy)
                                        if len(self.in_check((self.squarex, self.squarey), gamePiecesCopy, board, players=players)) == 0:
                                            # We've found a way to escape, break and cancel being in checkmate
                                            self.checkmate = False
                                            break
                                # If we've found a way out of checkmate, break
                                if not self.checkmate:
                                    break
                                    
                # Update our image, if needed
                if self.checkmate:
                    self.image = self.whiteCheckmateImage if self.white else self.blackCheckmateImage
                elif self.incheck:
                    self.image = self.whiteCheckImage if self.white else self.blackCheckImage

    def in_check(self, square, gamePieces, board, players):
        # Create a variable to store threats
        threats = []
        # For each piece, check if moving to our square is a valid move for them
        # If it is, then we're in check
        for sprite in gamePieces.sprites():
            # If the piece is on our side, skip checking any further
            if sprite.white == self.white:
                continue
            # Check if the sprite can move to us
            if players.is_valid_move(sprite, square, gamePieces, board, ignoreTurn=True, capture=True, ignoreCheck=True):
                threats.append(sprite)
        return threats
        
        
