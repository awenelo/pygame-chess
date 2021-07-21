import pygame

import configs

# Classes that contain items for the menus
class StartButton(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize the sprite object
        super().__init__()
        
        # Load the start button image, and resize it to 75x50
        self.image = pygame.transform.smoothscale(
            pygame.image.load("images/start_button.png"),
            (200, 50)
            )
        self.rect = self.image.get_rect()

        # Center the image rect
        self.rect.center = (configs.WIDTH//2, configs.HEIGHT//2+75)

    def draw(self, screen):
        # Draw us on the screen
        screen.blit(self.image, self.rect)

    def click(self, game, menu):
        # Start the game on click
        menu.game_menu()
        game.start_game()

class TitleText(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize the sprite object
        super().__init__()
        
        # Load the start button image, and resize it to 300x210
        self.image = pygame.transform.smoothscale(
            pygame.image.load("images/title_text.png"),
            (300, 210)
            )
        self.rect = self.image.get_rect()

        # Move the rect into position
        self.rect.center = (configs.WIDTH//2, configs.HEIGHT//2-100)

    def draw(self, screen):
        # Draw us on the screen
        screen.blit(self.image, self.rect)

    def click(self, game, menu):
        # Right now, do nothing on click
        pass
