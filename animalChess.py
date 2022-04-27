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
                valid_choice = self.flip_the_piece(player)
                # valid_choice = True
            elif choice == 'M':
                valid_choice = self.move(player)
                # valid_choice = True
            else:
                print('Please enter F or M to choose.')
                valid_choice = False

    def flip_the_piece(self, player):
        """
        enter the opened position
        """

        def is_valid_flip(row, col):
            if self.board[row][col].status == 1:
                print("Invalid Flip! This one is already flipped")
                return False
            # change the status
            if row > 3 or col > 3 or row < 0 or col < 0:
                print("Invalid Flip! The row/ col is out of index range")
                return False

            return True

        flip_valid = False
        while not flip_valid:
            print(f'{player} chooses to flip.')
            selected_piece = input("Please inter the row&col number of the chess you want to flip : ") # 加回车，退出F/M

            try:
                row = int(selected_piece[0])
                col = int(selected_piece[1])
            except ValueError:
                print("ValueError!")
                # return False
                flip_valid = False
            else:
                flip_valid = is_valid_flip(row, col)

        self.board[row][col].status = 1
        if self.board[row][col].belongings == "A":
            self.mingPiecesA.append(self.board[row][col].animal)
        else:
            self.mingPiecesB.append(self.board[row][col].animal)

        self.print_board()
        print("this is mingPiecesA list: ", self.mingPiecesA)
        print("this is mingPiecesB list: ", self.mingPiecesB)

        return True

    def move(self, player):
        """
        validate the input of move & moveto
        move to empty / eat the piece
        change the Minglist of players
        decide the winner
        """

        # invalid: move is empty, move is closed, move.belongings != player
        def is_valid_move(row, col, player):
            if self.board[row][col].animal is None:
                print("ERROR: this is an empty piece! Please change to another position!")
                return False
            if self.board[row][col].status == 0:
                print("ERROR: This piece is closed! Please flip this position first! ")
                return False
            if self.board[row][col].belongings != player:
                print("ERROR: Can not move others chess. Please move your chess! ")
                return False
            return True

        move_valid = False
        while not move_valid:
            print(f'{player} chooses to move.')
            selected_piece = input("Please inter the row&col number of the chess to move : ")

            try:
                row = int(selected_piece[0])
                col = int(selected_piece[1])
            except ValueError:
                print("ValueError!")
                # return False
                move_valid = False
            else:
                move_valid = is_valid_move(row, col, player)

        # invalid: moveto.belongings == player, moveto.player is closed
        def reinput_moveto(moveto_row, moveto_col, player):
            if self.board[moveto_row][moveto_col].belongings == player:
                print("ERROR: Can not eat your chess. Please select another position!")
                return True
            if self.board[moveto_row][moveto_col].status == 0:
                # moveto_piece exit
                print("ERROR: Can not move to this position. Please Flip this position first!")
                return True
            return False

        moveto_valid = True
        while moveto_valid:
            moveto = input("Please select the row&col piece to eat : ")

            try:
                moveto_row = int(moveto[0])
                moveto_col = int(moveto[1])
            except ValueError:
                return False

            moveto_valid = reinput_moveto(moveto_row, moveto_col, player)

        # row, col, moveto_row, moveto_col
        this_piece = copy.deepcopy(self.board[row][col])
        moveto_piece = copy.deepcopy(self.board[moveto_row][moveto_col])

        # add an empty piece
        empty_piece = Piece(None, None, None)

        # directly move
        if moveto_piece.animal is None:  # direct move!
            print("***** Directly move *****")
            # dark & ming_player & ming_opponent no change
            self.board[moveto_row][moveto_col] = this_piece
            self.board[row][col] = empty_piece
            self.print_board()
            return

        # this_piece eat opponent
        # rules: if the 差值 of the present animal and the move-to animals == 1 / -7, eat the moveto position's animals
        if this_piece.animal - moveto_piece.animal == 1 or this_piece.animal - moveto_piece.animal == -7:
            print("***** Eat your Opponent *****")
            self.board[moveto_row][moveto_col] = this_piece

            # dark + & ming_opponent -; ming_player no change
            if this_piece.belongings == "A":
                self.mingPiecesB.remove(moveto_piece.animal)
            else:
                self.mingPiecesA.remove(moveto_piece.animal)

            self.board[row][col] = empty_piece

            print("this is mingPiecesA list: ", self.mingPiecesA)
            print("this is mingPiecesB list: ", self.mingPiecesB)

            self.print_board()
            return

        # this_piece is eaten by the opponent
        if this_piece.animal - moveto_piece.animal == -1 or this_piece.animal - moveto_piece.animal == 7:
            print("***** Your are eaten by your Opponent *****")
            # dark + & ming_player -; ming_opponent no change
            if this_piece.belongings == "A":
                self.mingPiecesA.remove(this_piece.animal)
            else:
                self.mingPiecesB.remove(this_piece.animal)

            self.board[row][col] = empty_piece

            print("this is mingPiecesA list: ", self.mingPiecesA)
            print("this is mingPiecesB list: ", self.mingPiecesB)

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
            # if self.decide_the_winner():
            #     pass
            turns -= 1

    def eat_the_piece(self, player):
        """
        """
        pass

    def decide_the_winner(self):
        """
        run after each eat step when all pieces are Open
        winner: the greatest piece of A is greater than the greatest piece of B, then A wins
        """
        # if not self.darkPieces:
        greatest_A = self.mingPiecesA.max()
        greatest_B = self.mingPiecesB.max()

        could_eaten_result = self.be_eaten(greatest_A, 'A', greatest_B, 'B')

        if could_eaten_result.len == 0 or 2:
            return None
        elif could_eaten_result.len == 1:
            left_piece = could_eaten_result[0]
            winner = left_piece.belongings
            return winner

    def be_eaten(self, animal1, belonging1, animal2, belonging2):
        """
        Detect if anyone can be eaten by the other
        :param piece1: one piece from one party
        :param piece2: one piece from the other
        :return: what's left, [piece1], [piece2], [piece1, piece2]:remain, []: empty two
        """
        # animal1, belonging1 = piece1.animal, piece1.belongings
        # animal2, belonging2 = piece2.animal, piece2.belongings
        return []

    def detect_end(self):
        """
        avoid no ending 兜圈子
        Store the moves in a stack, if the stack is full? Too much same moves
        :return:
        """


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

