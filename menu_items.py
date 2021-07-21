import pygame

import configs

# Classes that contain items for the menus
class StartButton(pygame.sprite.Sprite):
    def __init__(self):
        # Store the font that we're using
        self.font = pygame.font.Font(configs.FONT, 50)

        # Initialize the sprite object, using the Play! text as the image
        super().__init__()
        # Load the start button image, and resize it to 75x50
        self.image = pygame.transform.smoothscale(
            pygame.image.load("images/start_button.png"),
            (200, 50)
            )
        self.rect = self.image.get_rect()

        # Center the image rect
        self.rect.center = (configs.WIDTH//2, configs.HEIGHT//2)

    def draw(self, screen):
        # Draw the text
        screen.blit(self.image, self.rect)

    def click(self, game, menu):
        menu.game_menu()
        game.start_game()
