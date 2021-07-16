import pygame

import configs

# Class to store data about players
class Player():
    def __init__(self, playerNumber):
        # Store our player number (0 or 1) - 1 is white, 0 is black
        self.playerNumber = playerNumber
        
        # Store if we're the acitve player
        self.activePlayer = False

        # Store if we've lost
        self.lost = False

    def make_active(self):
        # Make us the active player
        self.activePlayer = True

    def make_deactive(self):
        # Remove our active player status
        self.activePlayer = False

    def toggle_active(self):
        # Toggle if we're the active player or not
        self.activePlayer = not self.activePlayer

    def draw(self, screen):
        if self.activePlayer:
            text = pygame.font.Font(configs.FONT, 25).render(f"Player {abs(self.playerNumber-1)+1} - {'white' if self.playerNumber==1 else 'black'}{' loses' if self.lost else ''}", True, (0,0,0))
            textRect = text.get_rect()
            textRect.centerx = configs.WIDTH//2
            textRect.top = 12
            screen.blit(text, textRect)
            
            

# Class to store players and preform operations on them
class Players():
    def __init__(self):
        # Store players
        self.players = []

        # Store if the game is running
        self.gameOver = False
        
    def add(self, player):
        # Add a player to players, if it's white, make it active
        self.players.append(player)
        if player.playerNumber: # 1(True) is white
            player.make_active()

    # Get the first player that's active
    def get_active_player(self):
        for player in self.players:
            if player.activePlayer:
                return player

    # Check if a move is valid
    def is_valid_move(self, piece, *args, **kwargs):
        # Check if the game is running
        if self.gameOver:
            return False
        
        # Check if it's the same colour as the current player
        if piece.white != self.get_active_player().playerNumber:
            return False

        # If it is the same colour, run the piece's is_valid_move function
        return piece.is_valid_move(*args, **kwargs)

    def highlight_moves(self, piece, *args, **kwargs):
        # Highlight valid moves
        if piece.white != self.get_active_player().playerNumber:
            return False
        # If they're the same colour, run the pieces' function and return the result
        return piece.highlight_moves(*args, **kwargs)

    def move(self, piece, *args, **kwargs):
        if (piece.move(*args, **kwargs)):
            # Move to a square, switch active players if the move is final
            self.toggle_activations()

    def toggle_activations(self):
        for player in self.players:
            player.toggle_active()
        

    def draw(self, screen):
        # Draw each player's information
        for player in self.players:
            player.draw(screen)

    def update(self, pieces):
        # Check if the game is over
        for king in pieces.get_kings(False):
            if king.checkmate:
                # If a black king is in checkmate, the game is over
                self.gameOver=True
                # If playerNumber is 0 (black), set them to have lost and set them active
                for player in self.players:
                    if not player.playerNumber:
                        player.make_active()
                        player.lost = True
                    else:
                        # If playerNumber is 1 (white), set them to not be active
                        player.make_deactive()

        for king in pieces.get_kings(True):
            if king.checkmate:
                # If a white king is in checkmate, the game is over
                self.gameOver=True
                # If playerNumber is 1 (white), set them to have lost and set them active
                for player in self.players:
                    if player.playerNumber:
                        player.make_active()
                        player.lost = True
                    else:
                        # If playerNumber is 0 (black), set them to not be active
                        player.make_deactive()
            
                        
        
        