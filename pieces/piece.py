import pygame
from configs import SQUARE_SIZE

# General piece class, all pieces should have this as their parent
class Piece(pygame.sprite.Sprite):
    def __init__(self, deselectedImage, selectedImage, startingsquare):
        # Initialize the sprite
        super().__init__()
        
        # Store images
        self.image = pygame.image.load(deselectedImage)
        self.deselectedImage = self.image
        self.selectedImage = pygame.image.load(selectedImage)
        
        # Create a rectangle for positioning the image
        self.rect = self.image.get_rect()

        # Store what square we're on
        self.squarex, self.squarey = startingsquare

        # Set the position of the piece
        self.rect.x = self.squarex * SQUARE_SIZE
        self.rect.y = self.squarey * SQUARE_SIZE

    def move(self, squarex, squarey):
        # Move to a square
        # No collision checking right now, just set the position of the piece
        self.rect.x = squarex * SQUARE_SIZE
        self.rect.y = squarey * SQUARE_SIZE

        # Store what square we're on
        self.squarex = squarex
        self.squarey = squarey

    def update(self):
        # Do any animations, should the peice have them
        pass
    
    def draw(self, screen):
        # Draw the image on the screen at the same position as rect
        screen.blit(self.image, self.rect)

    def isValidMove(self, targetSquare, gamePieces, board):
        # With the defualt piece, any move is legal
        return True

    def select(self):
        # Set the piece to have the selected image
        self.image = self.selectedImage

    def deselect(self):
        # Set the piece to have the deselected image
        self.image = self.deselectedImage

# Sprite group class, adds some extra functionality to the default class
class PieceGroup(pygame.sprite.Group):
    # No initialization function, as all we need is the sprite group initialization

    def spriteCollidedWithPoint(self, point):
        # Loops through all the srites until it finds a sprite that collides with the point
        # If no sprites collide with the point, it returns None
        for sprite in self.sprites():
            if sprite.rect.collidepoint(point):
                return sprite
        return None
            
    
