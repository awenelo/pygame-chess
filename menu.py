import pygame

import configs

class Menu():
    # Menu management class
    def __init__(self):
        self.screen = "main"

    # Draw function, draws whatever the current menu screen is
    def draw(self, screen):
        text = pygame.font.Font(configs.FONT, 50).render("Click to start", True, (0,0,0))
        text_rect = text.get_rect()
        # Center the rect
        text_rect.center = (configs.WIDTH//2, configs.HEIGHT//2)
        # Draw the rect
        screen.blit(text, text_rect)

    # Update function, do any necessary animations
    def update(self):
        pass

    # MOUSEDOWN event handler
    def mouse_down(self, pos, game):
        if not game.inGame:
            # If there's a click and we're not in a game, start a game and use the click
            game.start_game()
            # Set us to use the game screen
            self.screen = "game"
            return True
        else:
            return False
