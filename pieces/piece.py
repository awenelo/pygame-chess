import pygame
import configs

# General piece class, all pieces should have this as their parent
class Piece(pygame.sprite.Sprite):
    def __init__(self, whiteImage, blackImage, isWhite, startingsquare):
        # Initialize the sprite
        super().__init__()
        
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

    def move(self, squarex, squarey, gamePieces):
        # Kill any other pieces we will overlap with
        for sprite in gamePieces.spriteCollidedWithPoint((squarex*configs.SQUARE_SIZE, squarey*configs.SQUARE_SIZE)):
            sprite.kill()
            
        # Move to a square
        # Set the position of the piece
        self.rect.x = squarex * configs.SQUARE_SIZE
        self.rect.y = squarey * configs.SQUARE_SIZE

        # Store what square we're on
        self.squarex = squarex
        self.squarey = squarey

    def update(self):
        # Do any animations, should the peice have them

        # Move to the mouse, but don't update what square we're on
        if self.followMouse:
            self.rect.center = pygame.mouse.get_pos()

        # If we're dead, force us to the top-left corner
        #if self.dead:
        #    self.rect.center = (0,0)
        #    self.squarex, self.squarey = (0,0)
    
    def draw(self, screen):
        # Draw the image on the screen at the same position as rect
        if not self.dead:
            screen.blit(self.image, self.rect)

    def is_valid_move(self, targetSquare, gamePieces, board, capture=False):
        # With the defualt piece, any move that doesn't overlap another piece is legal
        # We check that by calling spriteCollidedWithPoint on the target square
        foundPieces = gamePieces.spriteCollidedWithPoint((targetSquare[0]*configs.SQUARE_SIZE, targetSquare[1]*configs.SQUARE_SIZE))
        if len(foundPieces)>0:
            # If we can capture pieces, check each piece for if it's the enemy. If it is, the move is legal
            if capture:
                for sprite in foundPieces:
                    if sprite.white != self.white:
                        return True
            return False
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
        # Highlight all squares that we can legally move to
        for boardTile in board.boardGroup.sprites():
            # Check if we can move with capture
            if self.is_valid_move((boardTile.squarex, boardTile.squarey), gamePieces, board, capture=True):
                # If we can, highlight the tile with capture
                boardTile.highlight(True)
            # Check if we can move without capturing
            if self.is_valid_move((boardTile.squarex, boardTile.squarey), gamePieces, board):
                # If we can, highlight the tile without capture (overrides tiles highlighted above)
                boardTile.highlight(False)
                

    def collide_point(self, point):
        # If we're dead, return that we're not colliding
        if self.dead:
            return False
        # Reset the position to the last tile we were on, using a new PieceGroup to satisfy the gamePieces argument
        self.move(self.squarex, self.squarey, PieceGroup())

        # Then check if we're colliding
        return self.rect.collidepoint(point)

    def capture(self):
        # Kills the piece, leaving it in place
        self.dead = True

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
    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)
    
