from datetime import datetime
import configs

class Recorder():
    def __init__(self):
        # Create a new .pgn file
        time = datetime.now()
        self.filename = time.strftime("logs/%Y-%m-%d-%H-%M-%S-pygame-chess-game.pgn")
        # Open the file, exclusivley for creation, and add starting tags to it
        with open(self.filename, mode="x") as f:
            f.write("[Site \"Offline game run by pygame-chess\"]\n")
            f.write("[Date \"" + time.strftime("%Y.%m.%d") + "\"]\n")
            f.write("[Time \"" + time.strftime("%H:%M:%S") + "\"]\n")

        # Count which move we're on
        self.move = 1

        # Mark if the next move is completing a promotion
        self.promotion = False

    def record_move(self, piece, moveTo, gamePieces, board, promotion=False):
        # Figure out if the move is a capture move
        capture = False
        for sprite in gamePieces:
            if sprite.squarex == moveTo[0] and sprite.squarey == moveTo[1]:
                capture = True
                break
        # Loop through all the game pieces, check if they can move to moveTo and are the same colour, and if they can, then determine how much precision we need
        precisionXNeeded = False
        precisionYNeeded = False
        for sprite in gamePieces:
            if sprite.white != piece.white or sprite.name != piece.name or sprite is piece:
                continue
            if sprite.is_valid_move(moveTo, gamePieces, board, capture=True, ignoreCheck=True):
                precisionXNeeded = True
                if sprite.squarex == piece.squarex:
                    precisionYNeeded = True
                    # If we determine that we need complete precision, break out of the loop
                    break
        # If we're a pawn, always specify file
        if piece.name == "P":
            precisionXNeeded = True
        with open(self.filename, mode="a") as f:
            f.write(
                ((
                    "\n" # Add a new line
                    + str(self.move) # Mark which move we're on
                    + ". " # Add the dot
                ) if piece.white and not self.promotion else ("=" if self.promotion else " "))
                + piece.get_square(capture=capture,
                                   precisionXNeeded=precisionXNeeded and not self.promotion,
                                   precisionYNeeded=precisionYNeeded and not self.promotion)
                + (self.get_rank_file(moveTo) if not self.promotion else "")
                )
            # Clear if the next move is a promotion
            self.promotion = False
        if not piece.white: # If the piece is black (we just created a new line), increment our move counter by 1
            self.move += 1

    # Returns the name of the square
    def get_rank_file(self, square):
        return "abcdefgh"[square[0]-1].lower() + str(9-square[1])
        
    
