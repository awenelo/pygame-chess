import pieces
import player
from PGN_recorder import Recorder
from online_recorder import Recorder as OnlineRecorder

# Game management class - controls starting, stopping and creating games
class Game():
    def __init__(self, menu):
        # Store if we're in a game
        self.inGame = False

        # Create a group to store game pieces
        self.gamePieces = pieces.PieceGroup()

        # Create a group to store the players
        self.players = player.Players()

        # Create a variable to store our recorder
        self.recorder = None

        # Store if we're in an online game, and which side we are: 0 - black, 1 - white
        self.onlineGame = False
        self.onlineSide = 1

        # Store the menu
        self.menu = menu

        # Give the menu ourselves
        self.menu.game = self

    # Start a game, adds gamePieces to pieces
    def start_game(self, online=False):
        if not self.inGame:
            self.inGame = True
            # Create game pieces
            self.gamePieces.add(pieces.Rook((1,1), False))
            self.gamePieces.add(pieces.Rook((8,1), False))
            self.gamePieces.add(pieces.Rook((1,8), True))
            self.gamePieces.add(pieces.Rook((8,8), True))
            self.gamePieces.add(pieces.Bishop((3,1), False))
            self.gamePieces.add(pieces.Bishop((6,1), False))
            self.gamePieces.add(pieces.Bishop((3,8), True))
            self.gamePieces.add(pieces.Bishop((6,8), True))
            self.gamePieces.add(pieces.Queen((4,1), False))
            self.gamePieces.add(pieces.Queen((4,8), True))
            self.gamePieces.add(pieces.King((5,1), False))
            self.gamePieces.add(pieces.King((5,8), True))
            self.gamePieces.add(pieces.Knight((2,1), False))
            self.gamePieces.add(pieces.Knight((7,1), False))
            self.gamePieces.add(pieces.Knight((2,8), True))
            self.gamePieces.add(pieces.Knight((7,8), True))
            for position in range(1,9):
                self.gamePieces.add(pieces.Pawn((position, 2), False))
                self.gamePieces.add(pieces.Pawn((position, 7), True))
                
            # Add players
            self.players.add(player.Player(1))
            self.players.add(player.Player(0))
            # Create a new Recorder object, if there was one previously, throw it out
            if not online:
                self.recorder = Recorder()
                self.onlineGame = False

    # Create a new online recorder object
    def setup_game(self, onlineGameKey, talkToServer=True):
        self.recorder = OnlineRecorder(onlineGameKey, False, talkToServer=talkToServer)
        self.onlineGame = True

    # Stop a game, clear gamePieces and players
    def end_game(self):
        self.inGame = False
        self.gamePieces.empty()
        self.players.empty()
        self.recorder = None
        self.onlineGame = False

    # Update the recorder object, if we're online
    def update(self):
        if self.onlineGame:
            self.recorder.update(self, self.menu)

    # Draw the recorder object, if there's anything to draw
    def draw(self, screen):
        if self.onlineGame:
            self.recorder.draw(screen)
