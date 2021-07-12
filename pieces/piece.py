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

    def move(self, squarex, squarey):
        # Move to a square
        # No collision checking right now, just set the position of the piece
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
    
    def draw(self, screen):
        # Draw the image on the screen at the same position as rect
        screen.blit(self.image, self.rect)

    def is_valid_move(self, targetSquare, gamePieces, board):
        # With the defualt piece, any move that doesn't overlap another piece is legal
        # We check that by calling spriteCollidedWithPoint on the target square, and checking if it returns none
        if gamePieces.spriteCollidedWithPoint((targetSquare[0]*configs.SQUARE_SIZE, targetSquare[1]*configs.SQUARE_SIZE)):
            return False
        # All checks have passed
        return True

    def select(self):
        # Set the piece to follow the mouse
        self.followMouse = True

    def deselect(self):
        # Set the piece to stop following the mouse
        self.followMouse = False
        # Reset the position to the last tile we were on
        self.move(self.squarex, self.squarey)

    def highlight_moves(self, gamePieces, board):
        # Highlight all squares that we can legally move to
        for boardTile in board.boardGroup.sprites():
            if self.is_valid_move((boardTile.squarex, boardTile.squarey), gamePieces, board):
                boardTile.highlight()

    def collide_point(self, point):
        # Reset the position to the last tile we were on
        self.move(self.squarex, self.squarey)

        # Then check if we're colliding
        return self.rect.collidepoint(point)

# Sprite group class, adds some extra functionality to the default class
class PieceGroup(pygame.sprite.Group):
    # No initialization function, as all we need is the sprite group initialization

    def spriteCollidedWithPoint(self, point):
        # Loops through all the srites until it finds a sprite that collides with the point
        # If no sprites collide with the point, it returns None
        for sprite in self.sprites():
            if sprite.collide_point(point):
                return sprite
        return None
            
    
