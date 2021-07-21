import pygame

import configs
import menu_items

class Menu():
    # Menu management class
    def __init__(self):
        
        # Store where the places that we can click are
        self.menu_items = pygame.sprite.Group()

    # Got back to the main menu
    def main_menu(self):
        self.menu_items.empty()
        # Add the start button
        self.menu_items.add(menu_items.StartButton())

    # Go into a game
    def game_menu(self):
        self.menu_items.empty()


    # Draw function, draws whatever the current menu screen is
    def draw(self, screen):
        # Draw all the menu items
        for sprite in self.menu_items:
            sprite.draw(screen)
            

    # Update function, do any necessary animations
    def update(self):
        pass

    # MOUSEDOWN event handler
    def mouse_down(self, pos, game):
        if not game.inGame:
            # If there's a on a click target and we're not in a game, run that click target's click function
            for target in self.menu_items:
                if target.rect.collidepoint(pos):
                    target.click(game, self)
                    return True
            return False
        else:
            return False
