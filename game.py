import pieces

# Game management class - controls starting, stopping and creating games
class Game():
    def __init__(self):
        # Store if we're in a game
        self.inGame = False

        # Create a group to store game pieces
        self.gamePieces = pieces.PieceGroup()

    # Start a game, adds gamePieces to pieces
    def start_game(self):
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

