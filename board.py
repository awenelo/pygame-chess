import pygame
import configs

# A single tile of the board, used by Board()
class BoardTile(pygame.sprite.Sprite):
    def __init__(self, tile_image, tile_top_left):
        super().__init__()
        self.image = pygame.image.load(tile_image)
        self.rect = self.image.get_rect()
        self.rect.topleft = tile_top_left

# The board itself, contains a group of BoardTiles
class Board():
    # Initialization function 
    def __init__(self,
                 # Number of squares the board is wide
                 square_count_width,
                 # Number of squares the board is tall
                 square_count_height,
                 # Image file for white squares
                 board_tile_white_image,
                 # Image file for black squares
                 board_tile_black_image,
                 # Top left point of the board, defaults to (0,0)
                 top_left_point=(0,0)):
        # Create a group for board tiles
        self.boardGroup = pygame.sprite.Group()

        # Add square_count_width*square_count_height tiles to the group
        for h in range(square_count_height):
            for w in range(square_count_width):
                # Add a tile to the group
                self.boardGroup.add(
                    BoardTile(
                        # Determine which image to use
                        (board_tile_white_image
                         if w % 2 == h % 2
                         else board_tile_black_image),
                        # Determine where the tile should go
                        (top_left_point[0]+w*configs.SQUARE_SIZE,
                         top_left_point[1]+h*configs.SQUARE_SIZE)
                    )
                )
        
    
    def draw(self, screen):
        self.boardGroup.draw(screen)
