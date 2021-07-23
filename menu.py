import pygame

import configs
import menu_items

class Menu():
    # Menu management class
    def __init__(self):
        
        # Store where the places that we can click are
        self.menu_items = []

    # Got back to the main menu
    def main_menu(self):
        self.menu_items = list()
        # Add the start button
        self.menu_items.append(menu_items.StartButton())
        self.menu_items.append(menu_items.MoreButton())
        self.menu_items.append(menu_items.TitleText())

    # Go into a game
    def game_screen(self):
        self.menu_items = list()
        self.menu_items.append(menu_items.MenuButton())

    # Open the quit and settings menu above a game
    def game_menu(self):
        self.menu_items = list()
        self.menu_items.append(menu_items.MenuXButton())
        self.menu_items.append(menu_items.MenuQuit())
        self.menu_items.append(menu_items.MenuBackground())

    # Open a more options page
    def more_options_screen(self):
        self.menu_items = list()
        self.menu_items.append(menu_items.BackButton())
        self.menu_items.append(menu_items.NewOnlineGameButton())
        self.menu_items.append(menu_items.JoinOnlineGameButton())

    # Clear the menu
    def clear(self):
        self.menu_items = list()

    # Draw function, draws whatever the current menu screen is
    def draw(self, screen):
        # Draw all the menu items
        for sprite in self.menu_items[::-1]:
            sprite.draw(screen)
            

    # Update function, do any necessary animations
    def update(self):
        pass

    # MOUSEDOWN event handler
    def mouse_down(self, pos, game):
        # If there's a click that we can trigger, trigger that, otherwise, let a piece be selected
        for target in self.menu_items:
            if target.rect.collidepoint(pos):
                target.click(game, self)
                return True
        return False
