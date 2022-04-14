from random import shuffle

"""
Suzanne Wang, Keyu Han
"""


class Piece:
    def __init__(self, animal, belongings):
        self.animal = animal
        self.belongings = belongings
        self.status = 0  # start as dark


class AnimalChess:
    def __init__(self):
        self.board = None
        self.darkPieces = []
        self.mingPiecesA = []
        self.mingPiecesB = []

    def generate_puzzle(self):
        """
        1. Generate a 4*4 puzzle of pieces
        [
          [[animal, belongings, status]]
        ]
        """
        self.board = [[None for i in range(4)] for i in range(4)]
        # generate pieces
        pieces_list = []
        for belonging in range(2):
            for animal in range(8):
                piece = Piece(animal, belonging)
                pieces_list.append(piece)

        shuffle(pieces_list)
        piece_idx = 0
        for i in range(4):
            for j in range(4):
                self.board[i][j] = pieces_list[piece_idx]
                piece_idx += 1

    def print_board(self):
        for i in range(4):
            for j in range(4):
                piece = self.board[i][j]
                print(piece.animal, piece.belongings, end="|")
            print()

    def decide_the_winner(self):
        """

        """


    def flip_the_piece(self):
        """
        enter the opened position
        """


    def move(self):
        """

        """


    def eat_the_piece(self):
        """
        """


    def player_input(self):
        """
        this function is used to select if the next step is to make the move or eat the piece
        player's input
        """


if __name__ == "__main__":
    animalChess = AnimalChess()
    animalChess.generate_puzzle()
    animalChess.print_board()
