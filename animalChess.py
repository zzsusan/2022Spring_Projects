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
        self.isGameEnd = False

    def generate_board(self):
        """
        1. Generate a 4*4 puzzle of pieces
        [
          [[animal, belongings, status]]
        ]
        """
        self.board = [[None for i in range(4)] for i in range(4)]
        # generate pieces
        pieces_list = []
        for belonging in ['A', 'B']:
            for animal in range(8):
                piece = Piece(animal, belonging)
                pieces_list.append(piece)

        # shuffle the pieces list and assign them to board
        shuffle(pieces_list)
        piece_idx = 0
        for i in range(4):
            for j in range(4):
                self.board[i][j] = pieces_list[piece_idx]
                piece_idx += 1

    def print_board(self):

        # animalList : [0, 1, 2, 3, 4, 5, 6, 7] # Elephant > Lion > Tiger > Leopard > Dog > Woof > Cat > Rat | ADD # 0 can eat 7
        # animalsMap = {0: "Rat", 1: "Cat", 2:"Woof", 3: "Dog", 4: "Leopard", 5: "Tiger", 6: "Lion", 7: "Elephant"}

        animalsMap = {
            0: "\U0001F401",
            1: "\U0001F408",
            2: "\U0001F43A",
            3: "\U0001F436",
            4: "\U0001F406",
            5: "\U0001F42F",
            6: "\U0001F981",
            7: "\U0001F418"}

        # belongingsMap = {0: "A", 1: "B"}

        for i in range(4):
            for j in range(4):
                piece = self.board[i][j]
                print(animalsMap[piece.animal], piece.belongings, (i, j), end=" | ")
            print()

    def run_game(self):
        self.player_input('A')
        self.player_input('B')

    def player_input(self, player):
        """
        this function is used to select if the next step is to make the move or eat the piece
        player's input
        """
        valid_choice = False
        while not valid_choice:
            choice = input(f'Player {player}, please enter "F" to Flip a Dark Piece or enter "M" to Move a Ming Piece: ')
            if choice == 'F':
                self.flip_the_piece(player)
                valid_choice = True
            elif choice == 'M':
                self.move(player)
                valid_choice = True
            else:
                print('Please enter F or M to choose.')
                valid_choice = False

    def flip_the_piece(self, player):
        """
        enter the opened position
        """
        print(f'{player} chooses to flip.')

    def move(self, player):
        """
        """
        print(f'{player} chooses to move.')

    def eat_the_piece(self, player):
        """
        """
        pass

    def decide_the_winner(self):
        """

        """
        pass


# class Player:
#     def __init__(self, name, board):
#         self.name = name
#         self.board = board


if __name__ == "__main__":
    animalChess = AnimalChess()
    animalChess.generate_board()
    animalChess.print_board()
    animalChess.run_game()
