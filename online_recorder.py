import requests
from json import dumps
from secrets import token_urlsafe
import pygame
from time import monotonic

import configs

class Recorder():
    # Recorder for online games
    # Instead of logging games locally, we send the data to a Firebase RealTime Database
    def __init__(self, onlineGameKey, joinGame, talkToServer=True):
        self.url = configs.SERVER_URL
        if talkToServer:
            # Join the game
            self.join_game(joinGame, onlineGameKey)

        else:
            # Set our status to getting key
            self.status = "get_key"
            # Store if the underline should be there or not
            self.showUnderline = True

            # Store the part of the key we have
            self.pendingKey = ""

        # Count which move we're on
        self.move = 1

        # Store the angle of the loading circle
        self.loadingCircleAngle = 0

        # Make the loading circle
        self.loadingCircle = pygame.image.load("images/loading_circle.png")
        self.loadingCircle = pygame.transform.smoothscale(self.loadingCircle, (50, 50))
        self.loadingCircleRect = self.loadingCircle.get_rect()
        self.loadingCircleRect.left = 0
        self.loadingCircleRect.bottom = configs.HEIGHT

        # Store who's going next
        self.nextPlayer = 1

        # Store when we last updated
        self.lastUpdate = monotonic()

        # Store if the last update failed
        self.lastUpdateFailed = False

        # Mark if the next move is completing a promotion
        self.promotion = False
        self.pendingInstruction = ""

    def record_move(self, piece, moveTo, gamePieces, board, promotion=False):
        # Send the request
        req = requests.put(
            self.url + f"/gamemoves/{self.game_key}/{self.move}.json",
            dumps({"piece_name":piece.name,
                   "piece_pos":(piece.squarex*configs.SQUARE_SIZE+configs.SQUARE_SIZE//2, piece.squarey*configs.SQUARE_SIZE+configs.SQUARE_SIZE//2),
                   "move_to":moveTo,
                   })
            )

        self.move += 1

    def join_game(self, joinGame, onlineGameKey):
        self.game_key = onlineGameKey
        self.player_key = token_urlsafe(32)
        req = requests.put(self.url + "/games", data=dumps({"key": onlineGameKey, onlineGameKey: {"state":"waiting", "playerKey":self.player_key, "joiningGame":joinGame}}), headers={"Content-Type": "application/json"})
        if req.status_code not in [200, 201]:
            if req.status_code == 400:
                # The server rejected our request because the game already exists and is full, return that we didn't succeed
                return False
            else:
                # The server encountered an error, try again later
                raise Exception("The server encountered an error, please try again later.")
            
        # Set our status to waiting
        self.status = "waiting"
        # Return that we succeeded in joinging the game
        return True
    
    def draw(self, screen):
        if self.status == "get_key":
            # If we're getting a key, display what we have right now
            font = pygame.font.Font(configs.FONT, 25)
            # Create the text
            pendingtxt = font.render("Enter a game code: " + self.pendingKey, True, (0,0,0))
            # Create a rectangle that holds the text and center it
            pendingtxtRect = pendingtxt.get_rect()
            pendingtxtRect.centerx = configs.WIDTH//2
            pendingtxtRect.top = 12
            if not self.showUnderline:
                txt = pendingtxt
            else:
                # If we should show an underline, show the underline, but keep the text in the same spot
                txt = font.render("Enter a game code: " + self.pendingKey + "_", True, (0,0,0))
            # Create the rectangle that we'll actually show the text in and align it with the top-left of the other one
            txtRect = txt.get_rect()
            txtRect.topleft = pendingtxtRect.topleft
            screen.blit(txt, txtRect)
        elif self.status == "waiting":
            # If we're waiting for a second player, display the game key
            txt = pygame.font.Font(configs.FONT, 25).render(f"Your game code is: {self.game_key}", True, (0,0,0))
            txtRect = txt.get_rect()
            txtRect.centerx = configs.WIDTH//2
            txtRect.top = 12
            screen.blit(txt, txtRect)
            
        if self.lastUpdateFailed:
            # If we've lost connection to the server, rotate the loading circle and draw it
            loadingCircleRotated = pygame.transform.rotozoom(
                self.loadingCircle,
                self.loadingCircleAngle,
                1
            )
            self.loadingCircleAngle -= 1
            loadingCircleRotatedRect = loadingCircleRotated.get_rect()
            loadingCircleRotatedRect.center = self.loadingCircleRect.center
            screen.blit(loadingCircleRotated, loadingCircleRotatedRect)

    def update(self, game, menu):
        # Get the status of the game, if it's been at least 5 seconds since we last did and we're not still getting a key
        if self.status != "get_key" and monotonic() - self.lastUpdate > 5:
            # Reset the time since the last update
            self.lastUpdate = monotonic()

            # Store our previous status
            previousStatus = self.status
            
            req = requests.get(self.url + "/games", params={"gameId":self.game_key})
            if req.status_code != 200:
                #if self.lastUpdateFailed:
                #    raise Exception("Connection to server lost.")
                # If the last update was successful, then just mark this one as unsuccessfull
                self.lastUpdateFailed = True
                return
            self.lastUpdateFailed = False
            returnedData = req.json()
            if returnedData["gameFound"]:
                self.status = returnedData["status"]
                self.nextPlayer = returnedData["nextPlayerTurn"]
            else:
                print("The game you were in no longer exists. You were sent back to the main menu")
                menu.main_menu()

            if self.status != previousStatus:
                menu.game_screen()
                
        if self.status == "get_key":
            self.showUnderline = monotonic()%1 >= 0.5

    def add_char(self, char, menu, backspace=False):
        # Add the character to the key
        if self.status == "get_key":
            if backspace:
                self.pendingKey = self.pendingKey[:-1]
            else:
                self.pendingKey += char

        # Then, check if it's a valid key
        # If it is, then join that game
        if self.join_game(True, self.pendingKey):
            menu.game_screen()
            self.status = "playing"
            
            
