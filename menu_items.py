import pygame

import configs

# Class for all menu items
class MenuItem(pygame.sprite.Sprite):
    def __init__(self, image, size, center):
        # Initiallize the Sprite class
        super().__init__()
        
        # Load the image, and resize it to the correct size
        self.image = pygame.transform.smoothscale(
            pygame.image.load(image),
            size
            )
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def draw(self, screen):
        # Draw us on the screen
        screen.blit(self.image, self.rect)

    def click(self, game, menu):
        # Handle anytime we're clicked on
        pass

# Classes that contain items for the menus
class StartButton(MenuItem):
    def __init__(self):
        # Initialize the sprite object
        super().__init__("images/start_button.png", (200, 50), (configs.WIDTH//2, configs.HEIGHT//2+125))

    def click(self, game, menu):
        # Overwrite click to start the game
        menu.game_menu()
        game.start_game()

class TitleText(MenuItem):
    def __init__(self):
        # Initialize the sprite object
        super().__init__("images/title_text.png", (300, 210), (configs.WIDTH//2, 180))
