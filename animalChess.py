from random import shuffle
import copy

"""
Suzanne Wang, Keyu Han
"""


class Piece:
    def __init__(self, animal, belongings, status=0):
        self.animal = animal
        self.belongings = belongings
        self.status = status  # start as dark


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

        for belonging in ["A", "B"]:
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
                if piece.animal != None:
                    print(animalsMap[piece.animal], piece.animal, piece.belongings, piece.status, (i, j), end=" | ")
                else:
                    print(None, (i, j), end=" | ")
            print()

    def run_game(self):
        self.player_input('A')
        self.player_input('B')

    def player_input(self, player):
        """
        this function is used to select if the next step is to make the move or eat the piece
        player's input
        while not valid_choice:

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
        # check the validation of the chess
        selected_piece = input("Please inter the row&col number of the chess you want to flip : ")

        row = int(selected_piece[0])
        col = int(selected_piece[1])

        this_piece = self.board[row][col]
        if this_piece.status == 1:
            return "Invalid Flip! This one is already flipped"
        # change the status
        else:
            self.board[row][col].status = 1
            if this_piece.belongings == "A":
                self.mingPiecesA.append(this_piece)
            else:
                self.mingPiecesB.append(this_piece)
            self.print_board()


    def move(self, player):
        """
        先选坐标，再选移动方向(移动，吃)
        belongings 可以从参数中传进来吗
        """
        # TODO1: Add re-input of Invalid move
        print(f'{player} chooses to move.')
        selected_piece = input("Please inter the row&col number of the chess you want to move : ")

        row = int(selected_piece[0])
        col = int(selected_piece[1])
        # invalid: this_piece.status == 0/ this_piece is None/ this_piece.belongings != player / moveto_piece.belongings == player (first)
        # valid: this_piece is not None and this_piece.belongings == player  moveto_piece.belongings != player /.... (else)
        # TODO2: add extra function
        if self.board[row][col].animal is None:
            print("ERROR: this is an empty piece! please select another position!")
            return
        if self.board[row][col].status == 0:
            print("ERROR: This piece is closed! Please flip this position first! ")
            return
        if self.board[row][col].belongings != player:
            print("ERROR: Can not move others chess. Please move your chess! ")
            return

        # TODO3: Add re-input of Invalid move
        moveto = input("Please select the row&col number of the chess you want to move to : ")
        moveto_row = int(moveto[0])
        moveto_col = int(moveto[1])
        # TODO4: add extra function
        if self.board[moveto_row][moveto_col].belongings == player:
            print("ERROR: Can not eat your chess. Please select another position!")
            return
        if self.board[moveto_row][moveto_col].status == 0:
            # moveto_piece exit
            print("ERROR: Can not move to this position. Please Flip this position first!")

        # row, col, moveto_row, moveto_col
        this_piece = copy.deepcopy(self.board[row][col])
        moveto_piece = copy.deepcopy(self.board[moveto_row][moveto_col])

        # add an empty piece
        empty_piece = Piece(None, None, None)

        if moveto_piece.animal is None:  # direct move!
            # directly move
            self.board[moveto_row][moveto_col] = this_piece
            self.board[row][col] = empty_piece
            print(" This is a directly move!")
            self.print_board()
            return

        # this_piece eat opponent
        # rules: if the 差值 of the present animal and the move-to animals == 1 / -7, eat the moveto position's animals
        if this_piece.animal - moveto_piece.animal == 1 or this_piece.animal - moveto_piece.animal == -7:
            print("***** Eat your Opponent *****")
            self.board[moveto_row][moveto_col] = this_piece
            self.board[row][col] = empty_piece
            print("finish eat the opponent ! ")
            print("new moveto: ", self.board[moveto_row][moveto_col].animal)
            print("new this_piece: ", self.board[row][col].animal)
            self.print_board()
            return

        # this_piece is eaten by the opponent
        if this_piece.animal - moveto_piece.animal == -1 or this_piece.animal - moveto_piece.animal == 7:
            print("***** Your are eaten by your Opponent *****")
            self.board[row][col] = empty_piece
            self.print_board()
            return

    def play_the_game(self):
        """
        change the player to play the game
        """
        # first 5 turns
        turns = 5
        while turns > 0:
            self.player_input("A")
            self.player_input("B")
            if self.decide_the_winner():
                pass
            turns -= 1

    def eat_the_piece(self, player):
        """
        """
        pass

    def decide_the_winner(self):
        """
        """
        return True

    def demo_chess(self):

        demo = [
            [5, 1, 6, 5],
            [4, 7, 0, 3],
            [4, 7, 2, 3],
            [1, 0, 2, 6]
        ]

        belong = [
            ["A", "B", "A", "B"],
            ["B", "B", "A", "B"],
            ["A", "A", "B", "A"],
            ["A", "B", "A", "B"]
        ]

        self.board = [[None for i in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                piece = Piece(demo[i][j], belong[i][j])
                self.board[i][j] = piece


# class Player:
#     def __init__(self, name, board):
#         self.name = name
#         self.board = board


if __name__ == "__main__":
    animalChess = AnimalChess()
    # animalChess.generate_puzzle()
    animalChess.demo_chess()
    animalChess.print_board()
    # animalChess.player_input("A")
    animalChess.play_the_game()

