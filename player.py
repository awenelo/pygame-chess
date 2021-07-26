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
            text = pygame.font.Font(configs.FONT, 25).render(f"Player {abs(self.playerNumber-1)+1} - {'white' if self.playerNumber==1 else 'black'}{' loses' if self.lost else ' move'}", True, (0,0,0))
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

        # Store if we need to make the next move be a promotion
        self.nextMovePromotion = False
        
    def add(self, player):
        # Add a player to players, if it's white, make it active
        self.players.append(player)
        if player.playerNumber: # 1(True) is white
            player.make_active()

    def empty(self):
        # Reset ourselves
        self.__init__()

    # Get the first player that's active
    def get_active_player(self):
        for player in self.players:
            if player.activePlayer:
                return player

    # Check if a move is valid
    def is_valid_move(self, game, piece, *args, ignoreTurn=False, **kwargs):
        # Check if the game is running
        if self.gameOver:
            return False

        # Check if the recorder is online_recorder or pgn_recorder
        if game.onlineGame:
            # Check if it's our move
            if game.recorder.nextPlayer != game.recorder.player:
                return False

            # Check that the piece is the correct colour
            if piece.white != game.recorder.player % 2:
                return False

        else:
            if not ignoreTurn:
                # Check if the next move needs to be a promotion
                if self.nextMovePromotion and piece.promotion is None:
                    return False
                
                # Check if it's the same colour as the current player
                if piece.white != self.get_active_player().playerNumber:
                    return False
        
        # If it is the same colour, run the piece's is_valid_move function
        return piece.is_valid_move(*args, **kwargs)

    def highlight_moves(self, game, piece, *args, **kwargs):
        # Highlight valid moves
        # If we're in an online game, check against the recorder for which player should move, otherwise check against the players
        if game.onlineGame:
            if game.recorder.result != "playing":
                return False
            if piece.white != game.recorder.player % 2 or game.recorder.player != game.recorder.nextPlayer:
                return False
        else:
            if piece.white != self.get_active_player().playerNumber:
                return False
        # Check if the next move needs to be a promotion
        if self.nextMovePromotion and piece.promotion is None:
            return False
        # If they're the same colour, run the pieces' function and return the result
        return piece.highlight_moves(*args, **kwargs)

    def move(self, piece, recorder, board, *args, **kwargs):
        # Record the move, check that the move is approved by the server
        if not recorder.record_move(piece, (args[0], args[1]), args[2], board):
            return
        # Clear that the next move needs to be a promotion
        self.nextMovePromotion = False
        if piece.move(*args, **kwargs):
            # Move to a square, switch active players if the move is final
            self.toggle_activations()
        else:
            # If the move is not final, require piece that's moving next to have a promotion square set
            self.nextMovePromotion = True
            recorder.promotion = True
        if kwargs["countMovement"]:
            # If we're counting the movement, clear all justMoved flags except for the one we just moved
            for sprite in args[2]:
                if sprite is piece:
                    continue
                sprite.hasMoved |= sprite.justMoved
                sprite.justMoved = False
            

    def toggle_activations(self):
        for player in self.players:
            player.toggle_active()
        

    def draw(self, screen, game):
        # Draw each player's information, if we're in a single-player game
        if not game.onlineGame:
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
            
                        
        
        
