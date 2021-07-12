import pygame
import configs

# A single tile of the board, used by Board()
class BoardTile(pygame.sprite.Sprite):
    def __init__(self, tile_image, tile_image_selected, tile_top_left):
        # Initialize the pygame.sprite.Sprite class
        super().__init__()
        
        # Save the images
        self.image = tile_image
        self.normal_image = self.image
        self.highlighted_image = tile_image_selected

        # Store whether or not the tile is highlighted
        self.highlighted = False

        # Store which square we're on
        self.squarex = tile_top_left[0]
        self.squarey = tile_top_left[1]

        # Create and position a rectangle to draw the tile in
        self.rect = self.image.get_rect()
        self.rect.topleft = (tile_top_left[0]*configs.SQUARE_SIZE,
                             tile_top_left[1]*configs.SQUARE_SIZE)
        
    # Function to switch a tile to the highlighted image
    def highlight(self):
        self.image = self.highlighted_image
        self.highlighted = True

    # Function to return a tile to the normal image
    def dehighlight(self):
        self.image = self.normal_image
        self.highlighted = False

    # Function to toggle the highlight on a tile
    def toggle_highlight(self):
        if highlighted:
            self.dehighlight()
        else:
            self.highlight()
    

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
                 # Image file for highlighted white squares
                 board_tile_white_selected_image,
                 # Image file for highlighted black squares
                 board_tile_black_selected_image,
                 # Top left point of the board, defaults to (0,0)
                 top_left_point=(0,0)):
        # Create a group for board tiles
        self.boardGroup = pygame.sprite.Group()

        # Load the images
        board_tile_white_image = pygame.image.load(board_tile_white_image)
        board_tile_black_image = pygame.image.load(board_tile_black_image)
        board_tile_white_selected_image = pygame.image.load(board_tile_white_selected_image)
        board_tile_black_selected_image = pygame.image.load(board_tile_black_selected_image)

        # Add square_count_width*square_count_height tiles to the group
        for h in range(square_count_height):
            for w in range(square_count_width):
                # Add a tile to the group
                self.boardGroup.add(
                    BoardTile(
                        # Determine which images to use, if both width and height are even or odd, use a white tile
                        (board_tile_white_image
                         if w % 2 == h % 2
                         else board_tile_black_image),
                         (board_tile_white_selected_image
                         if w % 2 == h % 2
                         else board_tile_black_selected_image),
                        # Determine where the tile should go
                        (top_left_point[0]+w,
                         top_left_point[1]+h)
                    )
                )
    # Highlights all board tiles that collide with a point
    def highlight_point(self, point):
        for sprite in self.boardGroup.sprites():
            if sprite.rect.collidepoint(point):
                sprite.highlight()

    # Dehighlights all board tiles that collide with a point
    def dehighlight_point(self, point):
        for sprite in self.boardGroup.sprites():
            if sprite.rect.collidepoint(point):
                sprite.dehighlight()

    # Toggles the highlight on all board tiles that collide with a point
    def toggle_highlight_point(self, point):
        for sprite in self.boardGroup.sprites():
            if sprite.rect.collidepoint(point):
                sprite.toggle_highlight()

    # Removes the highlight from all tiles that don't collide with a point
    def remove_other_highlight_points(self, point):
        for sprite in self.boardGroup.sprites():
            if not sprite.rect.collidepoint(point):
                sprite.dehighlight()

    # Clears highlights
    def remove_highlights(self):
        for sprite in self.boardGroup.sprites():
            sprite.dehighlight()

    # Checks if a point is on the board
    def is_on_board(self, point):
        for sprite in self.boardGroup.sprites():
            if sprite.rect.collidepoint(point):
                return True
    
    def draw(self, screen):
        # Draw every item in boardGroup
        self.boardGroup.draw(screen)
