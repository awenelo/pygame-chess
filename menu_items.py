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

class MenuButton(MenuItem):
    # Button to bring up the menu in the game
    def __init__(self):
        # Initialize the menu item
        super().__init__("images/menu_button.png", (80,40), (45, 25))

    # On click, open the game menu
    def click(self, game, menu):
        menu.game_menu()
        game.inGame = False

class MenuXButton(MenuItem):
    # Button to close the in-game menu
    def __init__(self):
        # Initialize the menu item
        super().__init__("images/x_button.png", (50, 50), (25, 25))

    # On click, exit the game menu
    def click(self, game, menu):
        menu.game_screen()
        game.inGame = True

class MenuBackground(MenuItem):
    # Background for when the menu is open during the game
    def __init__(self):
        # Initialize the menu item
        super().__init__("images/game_menu_background.png", (500, 500), (configs.WIDTH//2, configs.HEIGHT//2))

class MenuQuit(MenuItem):
    # Quit button for menu, goes to main menu
    def __init__(self):
        # Initialize the menu item
        super().__init__("images/quit_button.png", (120, 40), (65, configs.HEIGHT-25))

    # On click, exit to the main menu
    def click(self, game, menu):
        menu.main_menu()
        game.end_game()

class StartButton(MenuItem):
    # Start button for the game
    def __init__(self):
        # Initialize the menu item
        super().__init__("images/start_button.png", (200, 50), (configs.WIDTH//2, configs.HEIGHT//2+125))
        
    # On click, start the game
    def click(self, game, menu):
        menu.game_screen()
        game.start_game()

class TitleText(MenuItem):
    # Title of the game
    def __init__(self):
        # Initialize the menu item
        super().__init__("images/title_text.png", (300, 210), (configs.WIDTH//2, 180))
