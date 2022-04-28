from random import shuffle
import copy

"""
Suzanne Wang, Keyu Han
"""

PLAYER_A = 'A'
PLAYER_B = 'B'

class Piece:
    def __init__(self, animal, belongings, status=0):
        self.animal = animal
        self.belongings = belongings
        self.status = status  # start as dark


class AnimalChess:
    def __init__(self):
        self.board = None
        self.darkPieces = []
        self.mingPieces = {
            'A': [],
            'B': []
        }

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

        dark_piece = "\U0001F0CF"
        empty_piece = "\U00002B1C"
        # belongingsMap = {0: "A", 1: "B"}

        for i in range(4):
            for j in range(4):
                piece = self.board[i][j]
                if piece and piece.animal is not None:
                    print(animalsMap[piece.animal], piece.animal, piece.belongings, piece.status, (i, j), end=" | ")
                else:
                    print(empty_piece, '_', '_', '_', (i, j), end=" | ")
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
            elif choice == 'M':
                valid_choice = self.move(player)
            else:
                print('Please enter F or M to choose.')
                valid_choice = False

    def flip_the_piece(self, player):
        """
        enter the opened position
        """
        print(f'{player} chooses to flip.')
        flip_valid = False
        while not flip_valid:
            selected_piece_string = input("Please input the row & col number of the chess you want to flip (Enter to exit): ")

            if not selected_piece_string:
                print("Exit flipping.")
                return False

            selected_piece = selected_piece_string.split()
            if len(selected_piece) != 2:
                flip_valid = False
                continue

            try:
                row = int(selected_piece[0])
                col = int(selected_piece[1])
            except ValueError:
                print("ValueError! Please input two valid integers.")
                flip_valid = False
            else:
                flip_valid = self.is_valid_flip(row, col)

        # Change the status
        self.board[row][col].status = 1
        belonging = self.board[row][col].belongings
        self.mingPieces[belonging].append(self.board[row][col].animal)

        self.print_board()
        print("this is mingPiecesA list: ", self.mingPieces['A'])
        print("this is mingPiecesB list: ", self.mingPieces['B'])

        return True

    def is_valid_flip(self, row, col):
        if row > 3 or col > 3 or row < 0 or col < 0:
            print("Invalid ! The row or col is out of index range")
            return False

        piece = self.board[row][col]
        if piece is None or piece.status == 1:
            print("Invalid Flip! This one is already flipped")
            return False

        return True

    def is_valid_move_from(self, row, col, player):
        if row > 3 or col > 3 or row < 0 or col < 0:
            print("Invalid Move! The row or col is out of index range")
            return False

        piece = self.board[row][col]
        if piece is None:
            print("ERROR: this is an empty piece! Please change to another position!")
            return False
        if piece.status == 0:
            print("ERROR: This piece is dark! Please flip it first! ")
            return False
        if piece.belongings != player:
            print("ERROR: Can not move your component' chess. Please move your chess! ")
            return False

        return True

    def input_move_from(self, player):
        """
        Input the row and col number of the move-from piece when choosing Move
        :return: the piece at move-from position
        """
        valid_select = False
        row, col = -1, -1
        while not valid_select:
            selected_piece_string = input("Please input the row & col number of the chess to move (Enter to go back to the last step): ")

            if not selected_piece_string:
                print("Back to choose Flip or Move.")
                return -1, -1, None

            selected_piece = selected_piece_string.split()
            if len(selected_piece) != 2:
                valid_select = False
                print('ERROR! Please input two valid integers.')
                continue

            try:
                row = int(selected_piece[0])
                col = int(selected_piece[1])
            except ValueError:
                print("ValueError! Please input two valid integers.")
                valid_select = False
            else:
                valid_select = self.is_valid_move_from(row, col, player)
        return row, col, self.board[row][col]

    def is_valid_move_to(self, row, col, player, hint=True):
        if row > 3 or col > 3 or row < 0 or col < 0:
            hint and print("Invalid Move! The row or col is out of index range")
            return False

        if self.board[row][col] is None:
            # Empty position
            return True
        elif self.board[row][col].belongings == player:
            hint and print("ERROR: Can not move to where your chess is. Please select another position!")
            return False
        elif self.board[row][col].status == 0:
            hint and print("ERROR: Can NOT move to this position. Please flip this position first!")
            return False
        return True

    def input_move_to(self, player):
        """
        Input the row and col number of the move-to piece when choosing Move
        :return: the piece at move-to position
        """
        valid_move = False
        row, col = -1, -1
        while not valid_move:
            move_to_string = input("Please input the row & col number you want to move to: ")

            # if not move_to_string:
                # print("Back to input the move-from position.")
                # return -1, -1, None

            move_to = move_to_string.split()
            if not move_to_string or len(move_to) != 2:
                valid_move = False
                print('ERROR! Please input two valid integers.')
                continue
            try:
                row = int(move_to[0])
                col = int(move_to[1])
            except ValueError:
                print("ValueError! Please input two valid integers.")
                valid_move = False
            else:
                valid_move = self.is_valid_move_to(row, col, player)
        return row, col, self.board[row][col]

    def input_move_direction(self, row, col, player):
        """
        Let player input the available move direction (go up, go down, go left, go right)
        :param row: the row index of the initial (move-from) position
        :param col: the col index of the initial (move-from) position
        :param player: current player
        :return:
        """
        # U, D, L, R
        valid_directions = []
        if self.is_valid_move_to(row, col - 1, player, False):
            valid_directions.append('up')
        if self.is_valid_move_to(row, col + 1, player, False):
            valid_directions.append('down')
        if self.is_valid_move_to(row + 1, col, player, False):
            valid_directions.append('right')
        if self.is_valid_move_to(row - 1, col, player, False):
            valid_directions.append('left')

        move_choice = input("Please ")

    def move(self, player):
        """
        validate the input of select & moveto
        move to empty / eat the piece
        change the Minglist of players
        decide the winner
        """
        # Input move from and move to position
        print(f'{player} chooses to move.')
        row, col, this_piece = self.input_move_from(player)
        if row == -1 and col == -1 and this_piece is None:
            # go back to choose Flip or Move
            return False

        moveto_row, moveto_col, moveto_piece = self.input_move_to(player)

        # print(row, col, this_piece.animal)
        # print(moveto_row, moveto_col, moveto_piece.animal)
        # if moveto_row == -1 and moveto_col == -1 and moveto_piece is None:
        #     input_finish = False
        # else:
        #     input_finish = True

        # this_piece_copied = copy.deepcopy(this_piece)
        # moveto_piece_copied = copy.deepcopy(moveto_piece)
        # empty_piece = Piece(None, None, None)

        if moveto_piece is None:  # direct move!
            print("***** Directly Move *****")
            self.board[row][col] = None
            self.board[moveto_row][moveto_col] = copy.deepcopy(this_piece)
            self.print_board()
            return True

        # This piece eats opponent
        # rules: if the dif of the present animal and the move-to animals == 1 / -7, eat the moveto position's animals
        if this_piece.animal - moveto_piece.animal >= 1 or this_piece.animal - moveto_piece.animal == -7:
            print("***** Eat the Opponent's Chess *****")
            self.board[row][col] = None
            self.board[moveto_row][moveto_col] = copy.deepcopy(this_piece)
            # dark + & ming_opponent -; ming_player no change
            self.mingPieces[moveto_piece.belongings].remove(moveto_piece.animal)

            self.print_board()
            return True

        # this_piece is eaten by the opponent
        if moveto_piece.animal - this_piece.animal >= 1 or moveto_piece.animal - this_piece.animal == -7:
            print("***** Your Piece are Eaten by Your Opponent *****")
            # dark + & ming_player -; ming_opponent no change
            self.board[row][col] = None

            self.mingPieces[player].remove(this_piece.animal)
            print("this is mingPiecesA list: ", self.mingPieces['A'])
            print("this is mingPiecesB list: ", self.mingPieces['B'])

            self.print_board()
            return True

        # same animal, remove together
        if moveto_piece.animal == this_piece.animal:
            self.board[row][col] = None
            self.board[moveto_row][moveto_col] = None

            self.mingPieces[player].remove(this_piece.animal)
            self.mingPieces[moveto_piece.belongings].remove(moveto_piece.animal)
            print("this is mingPiecesA list: ", self.mingPieces['A'])
            print("this is mingPiecesB list: ", self.mingPieces['B'])

            self.print_board()
            return True

        self.print_board()
        return False

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
        greatest_A = self.mingPieces[PLAYER_A].max()
        greatest_B = self.mingPieces[PLAYER_B].max()

        # if B has mouse and A has elephant, greatest_A > greatest_B, not end
        if greatest_A > greatest_B:
            if greatest_A == 7 and 0 in self.mingPieces[PLAYER_B]:
                return None
            else:
                return PLAYER_A
        elif greatest_A == 0 and greatest_B == 7:
            # mouse and elephant
            return PLAYER_A

        if greatest_B > greatest_A:
            if greatest_B == 7 and 0 in self.mingPieces[PLAYER_A]:
                return None
            else:
                return PLAYER_B
        elif greatest_B == 0 and greatest_A == 7:
            return PLAYER_B

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

