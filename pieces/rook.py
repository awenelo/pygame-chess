import pygame

from .piece import Piece

class Rook(Piece):
    # Overwrite the __init__ function to pass different images without input from main.py
    def __init__(self, startingsquare):
        super().__init__("images/rook-piece.png",
                         "images/rook-piece-selected.png",
                         startingsquare)
