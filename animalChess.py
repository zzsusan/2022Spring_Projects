import random

"""
Suzanne Wang, Keyu Han
"""


class AnimalChess:
    class Piece:
        def __init__(self, animal, belongings, status):
            self.animal = animal
            self.belongings = belongings
            self.status = status

    darkPieces = []
    mingPiecesA = []
    mingPiecesB = []

    def generate_the_puzzle(self, row, col):
        """
        1. Generate a 4*4 puzzle of pieces
        [
          [[animal, belongings, status]]
        ]
        """
        board = [[None for i in range(col)] for i in range(row)]

        for i in range(row):
            for j in range(col):
                cheese = AnimalChess.Piece(random.choice(range(9)), random.choice(range(2)), random.choice(range(2)))
                board[i][j] = cheese

        # print(board)

        return board


animalChess = AnimalChess()
animalChess.generate_the_puzzle(4, 4)


def decide_the_winner():
    """

    """


def flip_the_piece():
    """
    enter the opened position
    """


def move():
    """

    """


def eat_the_piece():
    """
    """


def player_input():
    """
    this function is used to select if the next step is to make the move or eat the piece
    player's input
    """
