import pygame
import configs
from player import Players

# General piece class, all pieces should have this as their parent
class Piece(pygame.sprite.Sprite):
    def __init__(self, whiteImage, blackImage, isWhite, startingsquare, hasmoved=False, promotion=None):
        # Initialize the sprite
        super().__init__()

        # Scale the images to the correct size
        whiteImage = pygame.transform.smoothscale(whiteImage, (configs.SQUARE_SIZE, configs.SQUARE_SIZE))
        blackImage = pygame.transform.smoothscale(blackImage, (configs.SQUARE_SIZE, configs.SQUARE_SIZE))
                                                  
        
        # Set our image and store the other
        self.image = whiteImage if isWhite else blackImage
        self.whiteImage = whiteImage
        self.blackImage = blackImage
        
        # Create a rectangle for positioning the image
        self.rect = self.image.get_rect()

        # Store what square we're on
        self.squarex, self.squarey = startingsquare

        # Set the position of the piece
        self.rect.x = self.squarex * configs.SQUARE_SIZE
        self.rect.y = self.squarey * configs.SQUARE_SIZE

        # Store if we're white or black
        self.white = isWhite

        # Create a variable to store if we should follow the mouse
        self.followMouse = False

        # Store if we're dead or not
        self.dead = False
        
        # Store the last known mouse position
        self.lastMousePos = pygame.mouse.get_pos()

        # Create a cache of valid moves
        self.validMoves = []

        # Store that we are not a king
        self.isKing = False

        # Record if we've moved or not
        self.hasMoved = hasmoved

        # Record if we've just made a movement
        self.justMoved = False

        # Record if we have a target square to be promoted to
        self.promotion = promotion

        # Set our single-character name
        self.name = "X"

    def get_square(self, capture=False, precisionXNeeded=False, precisionYNeeded=False):
        # When turned into a string, return our square and name ("K", "Q", ...)
        return self.name + ("abcdefgh"[self.squarex-1].lower() if precisionXNeeded else "") + (str(9-self.squarey) if precisionYNeeded else "") + ("x" if capture else "")
    
    def move(self, squarex, squarey, gamePieces, capture=True, countMovement=False):
        # If we're moving and the move is final, clear promotion
        if countMovement:
            self.promotion = None
        # Prevent moving if we're captured
        if self.dead:
            return True
        # Kill any other pieces we will overlap with, if capture is True
        if capture:
            for sprite in gamePieces.spriteCollidedWithPoint((squarex*configs.SQUARE_SIZE, squarey*configs.SQUARE_SIZE)):
                sprite.kill()

        # If we're counting this move, record that we've made a move
        if countMovement:
            self.justMoved = True
            
        # Move to a square
        # Set the position of the piece
        self.rect.x = squarex * configs.SQUARE_SIZE
        self.rect.y = squarey * configs.SQUARE_SIZE

        # Store what square we're on
        self.squarex = squarex
        self.squarey = squarey
        return True

    def copy(self):
        # Return a copy of us
        if self.__class__ == Piece:
            return self.__class__(self.whiteImage, self.blackImage, self.white, (self.squarex, self.squarey), hasmoved=(self.hasMoved or self.justMoved))
        else:
            return self.__class__((self.squarex, self.squarey), self.white, hasmoved=self.hasMoved)
        
    def update(self, gamePieces, board, moveMade, players=Players()):
        # Do any animations, should the peice have them

        # Check if we have a promotion square, and if we do, that it's not occupied
        if self.promotion is not None:
            if gamePieces.spriteCollidedWithPoint((self.promotion[0]*configs.SQUARE_SIZE, self.promotion[1]*configs.SQUARE_SIZE)):
                gamePieces.remove(self)
                self.capture()

        # Move to the mouse if needed, but don't update what square we're on
        if self.followMouse:
            # Get the mouse's position
            mousePos = pygame.mouse.get_pos()

            # Check that the mouse's position isn't the same as the last time we ran
            # If it is, return without doing any calculations, since our situation is the same as before
            if mousePos != self.lastMousePos:
                self.lastMousePos = mousePos
                mouseSquare = (mousePos[0]//configs.SQUARE_SIZE, mousePos[1]//configs.SQUARE_SIZE)
                # If we're not over a legal move, snap to the nearest one
                # Determine the distance of each move from the mouse point using the Pythagorean Theorem
                moveDistances = {}
                for move in self.validMoves:
                    # Get the distance from the mouse to the center of each tile along x and y
                    moveXDif = abs((move[0]*configs.SQUARE_SIZE+configs.SQUARE_SIZE/2)-mousePos[0])
                    moveYDif = abs((move[1]*configs.SQUARE_SIZE+configs.SQUARE_SIZE/2)-mousePos[1])
                    # Caluclulate the distance between the mouse and the tile
                    moveDif = (moveXDif**2+moveYDif**2)**0.5
                    # Store the move
                    moveDistances[moveDif] = move
                    
                # Determine the closest move and set out position to that
                closestMove = moveDistances[min(moveDistances)]
                
                # Move to the closest move
                self.rect.x = closestMove[0]*configs.SQUARE_SIZE
                self.rect.y = closestMove[1]*configs.SQUARE_SIZE
        else:
            # If we're not following the mouse, snap to our square
            self.rect.x = self.squarex*configs.SQUARE_SIZE
            self.rect.y = self.squarey*configs.SQUARE_SIZE
                
                    
    
    def draw(self, screen):
        # Draw the image on the screen at the same position as rect
        if not self.dead:
            screen.blit(self.image, self.rect)

    def is_valid_move(self, targetSquare, gamePieces, board, capture=False, ignoreCheck=False, players=Players()):
        # If we're captured, we can't move
        if self.dead:
            return False

        # Check that we're not trying to move to the same place
        if self.squarex == targetSquare[0] and self.squarey == targetSquare[1]:
            return False

        # Check that we're not trying to move off the board
        if not board.is_on_board((targetSquare[0]*configs.SQUARE_SIZE, targetSquare[1]*configs.SQUARE_SIZE)):
            return False        
                
        # With the defualt piece, any move that doesn't overlap another piece is legal
        # We check that by calling spriteCollidedWithPoint on the target square
        foundPieces = gamePieces.spriteCollidedWithPoint((targetSquare[0]*configs.SQUARE_SIZE, targetSquare[1]*configs.SQUARE_SIZE))
        if len(foundPieces)>0:
            # If we can capture pieces, check each piece for if it's the enemy. If it is, the move is probably legal
            # Store if the tile is capturable
            capturable = False
            if capture:
                for sprite in foundPieces:
                    if sprite.white != self.white:
                        capturable = True
                        # Force ignoreCheck to be True if we could kill the king
                        if sprite.isKing:
                            ignoreCheck=True
            if not capturable:
                return False  
        # Check that we're not putting our king/kings in check, if ignoreCheck is False
        if not ignoreCheck: 
            kings = gamePieces.get_kings(self.white)
            # Make a copy of our move and game pieces
            spriteCopy = self.copy()
            gamePieces.remove(self)
            gamePieces.add(spriteCopy)
            # Remove any pieces that would be killed from moving
            threatenedPieces = gamePieces.spriteCollidedWithPoint((targetSquare[0]*configs.SQUARE_SIZE, targetSquare[1]*configs.SQUARE_SIZE))
            if self.name == "P":
                threatenedPawns = gamePieces.spriteCollidedWithPoint((targetSquare[0]*configs.SQUARE_SIZE, self.squarey*configs.SQUARE_SIZE))
                for pawn in threatenedPawns:
                    if (
                        pawn.name == "P"
                        and not pawn.hasMoved
                        and pawn.justMoved
                        and pawn.squarex == targetSquare[0]
                        and pawn.squarey == self.squarey
                        ):
                        threatenedPieces.append(pawn)
            for piece in threatenedPieces:
                gamePieces.remove(piece)
            spriteCopy.move(targetSquare[0], targetSquare[1], gamePieces, capture=True)
            for king in kings:
                if len(king.in_check((king.squarex, king.squarey), gamePieces, board, players))>0:
                    # Undo the changes to gamePieces we've done
                    for piece in threatenedPieces:
                        gamePieces.add(piece)
                    gamePieces.remove(spriteCopy)
                    gamePieces.add(self)
                    return False
            # Undo the changes to gamePieces we've done
            for piece in threatenedPieces:
                gamePieces.add(piece)
            gamePieces.remove(spriteCopy)
            gamePieces.add(self)
        
        # All checks have passed
        return True

    def select(self):
        # Set the piece to follow the mouse
        self.followMouse = True

    def deselect(self):
        # Set the piece to stop following the mouse
        self.followMouse = False
        # Reset the position to the last tile we were on, using a new PieceGroup to satisfy the gamePieces argument
        self.move(self.squarex, self.squarey, PieceGroup())

    def highlight_moves(self, gamePieces, board):
        # Clear the cache of valid moves, setting it to only have our current position
        self.validMoves = [(self.squarex, self.squarey)]
        # Create variable to store if we've found a move
        foundMove = False
        # Highlight all squares that we can legally move to
        for boardTile in board.boardGroup.sprites():
            # Check if we can move with capture
            if self.is_valid_move((boardTile.squarex, boardTile.squarey), gamePieces, board, capture=True):
                # If we can, highlight the tile with capture
                boardTile.highlight(True)
                # Record that we've found a valid move
                foundMove = True
                # Cache the move
                self.validMoves.append((boardTile.squarex, boardTile.squarey))
            # Check if we can move without capturing
            if self.is_valid_move((boardTile.squarex, boardTile.squarey), gamePieces, board):
                # If we can, highlight the tile without capture (overrides tiles highlighted above)
                boardTile.highlight(False)
                # Record that we've found a valid move
                foundMove = True
        # Return if we've found a move or not
        return foundMove

    def collide_point(self, point):
        # If we're dead, return that we're not colliding
        if self.dead:
            return False
        
        # Make a copy of our rectangle
        newRect = self.rect.copy()

        # Move it to the square we're on
        newRect.topleft = (self.squarex*configs.SQUARE_SIZE, self.squarey*configs.SQUARE_SIZE)
        
        # Then use it to check if we're colliding
        return newRect.collidepoint(point)

    def capture(self):
        # Kill the piece, leaving it in place
        self.dead = True
        # Then, remove it from all groups, leaving it for garbage collection
        self.kill()

# Sprite group class, adds some extra functionality to the default class
class PieceGroup(pygame.sprite.Group):
    # No initialization function, as all we need is the sprite group initialization

    def spriteCollidedWithPoint(self, point):
        # Loops through all the srites, finding sprites that collide with the point
        # If no sprites collide with the point, it returns an empty list

        # Store found sprites
        foundSprites = []
    
        for sprite in self.sprites():
            if sprite.collide_point(point):
                foundSprites.append(sprite)
        return foundSprites

    # Overwrite the draw function to call the draw function of each sprite
    def draw(self, screen, selectedPiece=[]):
        drawnLocs = []
        for sprite in self.sprites():
            # Draw the sprite if it's not over another sprite and it's not over the selectedPiece
            if (
                (False if len(selectedPiece) == 0 else (sprite is selectedPiece[0]))
                or (sprite.rect.center not in drawnLocs
                    and (True if len(selectedPiece) == 0 else sprite.rect.center != selectedPiece[0].rect.center)
                )): 
                sprite.draw(screen)
                # Add it's position to the list of sprites that we've drawn
                drawnLocs.append(sprite.rect.center)

    # Overwrite the update function to add extra parameters
    def update(self, gamePieces, board, moveMade, players=Players()):
        for sprite in self.sprites():
            sprite.update(gamePieces, board, moveMade)

    # Overwrite the copy function
    def copy(self, excludelist=[]):
        # Create a new piece group, and add a copy of every piece to it
        retGroup = PieceGroup()
        for sprite in self.sprites():
            if sprite not in excludelist:
                retGroup.add(sprite.copy())
        return retGroup
        
    # Get kings
    def get_kings(self, white):
        kings = []
        for sprite in self.sprites():
            if sprite.isKing and sprite.white == white:
                kings.append(sprite)
        return kings
    
