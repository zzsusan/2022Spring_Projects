import random
from random import shuffle
import copy

"""
Suzanne Wang, Keyu Han
IS 597 Final
"""

PLAYER_A = 'A'
PLAYER_B = 'B'

directions = {
    'up': [-1, 0],
    'down': [1, 0],
    'right': [0, 1],
    'left': [0, -1]
}


class Piece:
    def __init__(self, animal, belongings, status=0):
        self.animal = animal
        self.belongings = belongings
        self.status = status  # start as dark


class AnimalChess:
    def __init__(self):
        self.board = None
        self.darkPieceNum = 16
        self.mingPieces = {
            'A': [],  # [row, col, animal]
            'B': []
        }
        self.mode = 1
        self.game_end = False

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

        dark_piece = "\U0001F330"  # "\U0001F0CF"
        empty_piece = "\U00002B1C"

        # For test
        print("mingPiecesA: ", self.mingPieces['A'])
        print("mingPiecesB: ", self.mingPieces['B'])

        # For real game
        for i in range(4):
            for j in range(4):
                piece = self.board[i][j]
                if piece and piece.animal is not None:
                    if piece.status == 0:
                        print('?', dark_piece, (i, j), end=" | ")  # piece.animal, (i, j)
                    else:
                        print(piece.belongings, animalsMap[piece.animal], (i, j), end=" | ")  # piece.animal, (i, j),
                else:
                    print('_', empty_piece, (i, j), end=" | ")
            print()

    def player_input(self, player):
        """
        Let player input the choice: to flip a piece or to move a piece
        """
        print(f"\n***** {player}'s Turn *****")
        if self.darkPieceNum == 0:  # can only move
            self.move(player)
            return

        # can only flip
        if len(self.mingPieces[player]) == 0:
            self.flip_the_piece(player)
            return

        # can make choice
        valid_choice = False
        while not valid_choice:
            choice = input(f'Please enter "f" to Flip a Dark Piece or enter "m" to Move a Ming Piece: ')
            if choice == 'f':
                valid_choice = self.flip_the_piece(player)
                self.darkPieceNum -= 1
            elif choice == 'm':
                valid_choice = self.move(player)
            else:
                print('Please enter f or m to choose.')
                valid_choice = False

    def flip_the_piece(self, player):
        """
        enter the opened position
        """
        print(f'    {player} chooses to flip')
        flip_valid = False
        while not flip_valid:
            selected_piece_string = input(
                "Please input the row & col number of the chess you want to flip (Enter to exit): ")

            if not selected_piece_string:
                print("\tExit flipping.")
                return False

            selected_piece = selected_piece_string.split()
            if len(selected_piece) != 2:
                flip_valid = False
                continue

            try:
                row = int(selected_piece[0])
                col = int(selected_piece[1])
            except ValueError:
                print("\tINVALID! Please input two valid integers.")
                flip_valid = False
            else:
                flip_valid = self.is_valid_flip(row, col, True)

        # Change the status
        self.add_to_ming_pieces(row, col)
        self.print_board()

        return True

    def is_valid_flip(self, row, col, hint=False):
        if row > 3 or col > 3 or row < 0 or col < 0:
            hint and print("\tINVALID! The row or col is out of index range.")
            return False

        piece = self.board[row][col]
        if piece is None or piece.status == 1:
            hint and print("\tINVALID! This one is already flipped.")
            return False

        return True

    def is_valid_move_from(self, row, col, player):
        if row > 3 or col > 3 or row < 0 or col < 0:
            print("\tINVALID! The row or col is out of index range.")
            return False

        piece = self.board[row][col]
        if piece is None:
            print("\tINVALID! This is an empty piece. Please change to another position.")
            return False
        if piece.status == 0:
            print("\tINVALID! This piece is dark. Please flip it first. ")
            return False
        if piece.belongings != player:
            print("\tINVALID! Can not move your component' chess. Please move your chess. ")
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
            selected_piece_string = input("Please input the row & col number of the piece to move (Enter to go back): ")

            if not selected_piece_string:
                print("Back to choose Flip or Move.")
                return -1, -1, None

            selected_piece = selected_piece_string.split()
            if len(selected_piece) != 2:
                valid_select = False
                print('\tINVALID! Please input two valid integers.')
                continue

            try:
                row = int(selected_piece[0])
                col = int(selected_piece[1])
            except ValueError:
                print("\tINVALID! Please input two valid integers.")
                valid_select = False
            else:
                valid_select = self.is_valid_move_from(row, col, player)
        return row, col, self.board[row][col]

    def is_valid_move_to(self, row, col, player, hint=True):
        if row > 3 or col > 3 or row < 0 or col < 0:
            # hint and print("\tINVALID! The row or col is out of index range.")
            return False

        if self.board[row][col] is None:
            # Empty position
            return True
        elif self.board[row][col].belongings == player:
            # hint and print("ERROR: Can not move to where your chess is. Please select another position!")
            return False
        elif self.board[row][col].status == 0:
            # hint and print("ERROR: Can NOT move to this position. Please flip this position first!")
            return False
        return True

    def input_move_to(self, row, col, player):
        """
        Let player input the available move direction (go up, go down, go left, go right)
        :param row: the row index of the initial (move-from) position
        :param col: the col index of the initial (move-from) position
        :param player: current player
        :return: the row index, col index and the animal at move-to position
        """
        valid_directions = self.get_valid_move_direction(row, col, player)

        if not valid_directions:
            # no valid move for this piece
            # TODO1
            print("\tNOTICE! There are no valid move possibilities for this piece. Please re-input a position!")
            return -1, -1, None

        is_valid_choice = False
        while not is_valid_choice:
            move_choice = input(f"Please input your move direction from {valid_directions}: ")
            if move_choice in valid_directions:
                is_valid_choice = True
            else:
                print("\tINVALID!")

        move_to_row, move_to_col = row + directions[move_choice][0], col + directions[move_choice][1]
        # print(move_to_row, move_to_col)
        return move_to_row, move_to_col, self.board[move_to_row][move_to_col]

    def get_valid_move_direction(self, row, col, player):
        """
        :param row: the row index of the initial (move-from) position
        :param col: the col index of the initial (move-from) position
        :param player: current player
        :return: a list of all valid move directions
        """
        # U, D, L, R
        valid_directions = []
        if self.is_valid_move_to(row - 1, col, player, False):
            valid_directions.append('up')
        if self.is_valid_move_to(row + 1, col, player, False):
            valid_directions.append('down')
        if self.is_valid_move_to(row, col + 1, player, False):
            valid_directions.append('right')
        if self.is_valid_move_to(row, col - 1, player, False):
            valid_directions.append('left')

        return valid_directions

    def player_input_move(self, player):
        valid_input = False
        while not valid_input:
            row, col, this_piece = self.input_move_from(player)
            if this_piece is None:  # go back to choose Flip or Move
                return None, None
            moveto_row, moveto_col, moveto_piece = self.input_move_to(row, col, player)
            if moveto_row == -1:  # this piece has no valid move_to options
                valid_input = False
            else:
                valid_input = True

        return [row, col, this_piece], [moveto_row, moveto_col, moveto_piece]

    def move(self, player):
        """
        validate the input of select & moveto
        move to empty / eat the piece
        change the Minglist of players
        decide the winner
        """
        # Input move from and move to position
        if player == PLAYER_A:
            opponent = PLAYER_B
        else:
            opponent = PLAYER_A

        if self.mode == 1 or player == PLAYER_A:
            # user input
            move_from_info, move_to_info = self.player_input_move(player)
        else:
            # computer generate
            move_from_info, move_to_info = self.computer_generate_move_info(player)

        if move_from_info is None or move_to_info is None:
            return False

        [row, col, this_piece] = move_from_info
        [moveto_row, moveto_col, moveto_piece] = move_to_info

        print(f'    {player} chooses to move')

        this_piece_copied = copy.deepcopy(this_piece)
        moveto_piece_copied = copy.deepcopy(moveto_piece)

        if moveto_piece is None:  # direct move!
            self.board[row][col] = None
            self.board[moveto_row][moveto_col] = copy.deepcopy(this_piece)

            self.mingPieces[player].remove([row, col, this_piece_copied.animal])
            self.mingPieces[player].append([moveto_row, moveto_col, this_piece_copied.animal])
            self.print_board()
            print(f"     {player} makes a direct Move")
            return True

        # same animal, remove together
        if moveto_piece.animal == this_piece.animal:
            self.board[row][col] = None
            self.board[moveto_row][moveto_col] = None
            # self.darkPieceNum -= 2

            self.mingPieces[player].remove([row, col, this_piece_copied.animal])
            self.mingPieces[opponent].remove([moveto_row, moveto_col, moveto_piece_copied.animal])
            self.print_board()
            print("\tTwo pieces perish together.")
            return True

        # This piece eats opponent, mouse can eat elephant, elephant can not eat mouse
        animal_dif = this_piece_copied.animal - moveto_piece_copied.animal
        if 1 <= animal_dif < 7 or animal_dif == -7:
            self.board[row][col] = None
            # self.darkPieceNum -= 1
            self.board[moveto_row][moveto_col] = copy.deepcopy(this_piece)

            # print("moveto_row, moveto_col", moveto_row, moveto_col)
            self.mingPieces[player].remove([row, col, this_piece_copied.animal])
            self.mingPieces[player].append([moveto_row, moveto_col, this_piece_copied.animal])
            self.mingPieces[opponent].remove([moveto_row, moveto_col, moveto_piece_copied.animal])

            self.print_board()
            print(f"     {player} eat the opponent's chess.")
            return True

        # this_piece is eaten by the opponent
        if -7 < animal_dif < 1 or animal_dif == 7:
            self.mingPieces[player].remove([row, col, this_piece_copied.animal])
            self.mingPieces[opponent].remove([moveto_row, moveto_col, moveto_piece_copied.animal])
            self.mingPieces[opponent].append([row, col, moveto_piece_copied.animal])

            self.board[row][col] = None
            self.print_board()
            print(f"     {player}'s piece was eaten by the opponent.")
            return True

        self.print_board()
        return False

    def play_the_game(self):
        """
        change the player to play the game
        """
        mode_valid = False
        while not mode_valid:
            mode_str = input(
                "Please select the game mode (1: play with your friend, 2: play with computer) (Enter to exit): ")
            if not mode_str:
                print("\tGame Exit.")
                exit(0)
            try:
                mode = int(mode_str)
            except ValueError:
                print("\tINVALID! Please input 1 or 2.")
                mode_valid = False
            else:
                if mode == 1:
                    mode_valid = True
                    print(f"\tYou choose to play with your friend!")
                elif mode == 2:
                    mode_valid = True
                    print(f"\tYou choose to play with the computer!")
                else:
                    mode_valid = False
                    print("\tINVALID! Please input 1 or 2.")

        self.mode = mode
        self.print_board()
        round = 1
        game_end = False
        while not game_end:
            print(f"\n#### Round {round} #####")

            self.player_input(PLAYER_A)
            # print("darkpiece: ", self.darkPieceNum)
            game_end = self.determine_end(PLAYER_A)
            if game_end:
                break

            if self.mode == 1:
                self.player_input(PLAYER_B)
            else:
                self.computer_turn(PLAYER_B)

            # print("darkpiece: ", self.darkPieceNum)
            game_end = self.determine_end(PLAYER_B)
            round += 1

        print("***** GAME END *****")

    def determine_end(self, player):
        """
        To determine if the game ends
        """
        if self.darkPieceNum > 0:
            # can not determine the winner when there are dark pieces
            return False
        winner = self.decide_the_winner(player)
        if winner is not None:
            print(f"\t{winner.upper()} WINS!!!!")
            self.game_end = True
            return True
        return False

    def decide_the_winner(self, player):
        """
        run after each eat step when all pieces are Open
        winner: the greatest piece of A is greater than the greatest piece of B, then A wins
        :return: the winner player or None
        """

        if not self.mingPieces[PLAYER_A] and not self.mingPieces[PLAYER_B]:
            return player

        if not self.mingPieces[PLAYER_A]:
            return PLAYER_B

        if not self.mingPieces[PLAYER_B]:
            return PLAYER_A

        greatest_A = self.sort_open_animals(PLAYER_A)[0][2]
        greatest_B = self.sort_open_animals(PLAYER_B)[0][2]

        # print("A max, B max", greatest_A, greatest_B)
        # No End when greatest_A > greatest_B but B has mouse and A has elephant

        if greatest_A > greatest_B:
            if greatest_A == 7 and greatest_B == 0:
                return PLAYER_B
            elif greatest_A == 7 and 0 in self.mingPieces[PLAYER_B]:
                return None
            else:
                return PLAYER_A
        elif greatest_B > greatest_A:
            if greatest_B == 7 and greatest_A == 0:
                return PLAYER_A
            elif greatest_A == 7 and 0 in self.mingPieces[PLAYER_B]:
                return None
            else:
                return PLAYER_A
        elif greatest_A == greatest_B:
            return None

    def sort_open_animals(self, player):
        """
        for computer movement selection
        :return:
        """
        openList = self.mingPieces[player]  # exp [[0, 0, 5], [2, 3, 3], [3, 0, 1], [3, 2, 2]]
        openList.sort(key=lambda x: x[2], reverse=True)
        return openList

    def computer_generate_move_info(self, player):
        valid_move = False
        sorted_ming = self.sort_open_animals(player)
        biggest_animal_index = 0
        while biggest_animal_index < len(sorted_ming) and not valid_move:
            # move_piece = random.choice(self.mingPieces[player])
            move_piece = sorted_ming[biggest_animal_index]
            [row, col, animal] = move_piece

            # look up 4 directions
            directs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            max_set = {'row': -1, 'col': -1, 'animal': -1}
            for direct in directs:
                new_row, new_col = row + direct[0], col + direct[1]
                if new_row > 3 or new_col > 3 or new_row < 0 or new_col < 0:
                    continue

                check_piece = self.board[new_row][new_col]
                if check_piece is None or check_piece.status == 0 or check_piece.belongings == player:
                    continue
                # special case: biggest_animal_index == 0 or 7
                if animal == 0:
                    if check_piece.animal == 7:
                        max_set = {'row': new_row, 'col': new_col, 'animal': 7}
                        break
                else:
                    if animal > check_piece.animal > max_set['animal']:
                        max_set = {'row': new_row, 'col': new_col, 'animal': check_piece.animal}

            if max_set['row'] == -1:
                biggest_animal_index += 1
            else:
                if animal == 7 and max_set['animal'] == 0:
                    biggest_animal_index += 1
                else:
                    move_to_row, move_to_col = max_set['row'], max_set['col']
                    valid_move = True

        if not valid_move:
            # no valid move possibilities, should go back to flip
            return None, None
            
        print(
            f"    Computer(B) moves from ({row}, {col}) to ({move_to_row}, {move_to_col})")
        return [row, col, self.board[row][col]], [move_to_row, move_to_col, self.board[move_to_row][move_to_col]]

    def rat_strategy(self):
        """
        If the opponent has a rat, the computer will give priority to turning over the chess card next to the rat
        If the opponent has a rat, eat the opponent's rat first:
             See if there is any next to the rat that can eat rat in 1 move
                 If not: flip the piece next to the  rat

        If our rat appears, flip to avoid the rat next to it
        :return: the computer choice
        """
        def check_valid_move_or_flip(row, col):
            flip_list = []
            directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            for direct in directions:
                movefrom_row, movefrom_col = row + direct[0], col + direct[1]

                if movefrom_row > 3 or movefrom_col > 3 or movefrom_row < 0 or movefrom_col < 0:
                    continue
                moveto_piece = self.board[movefrom_row][movefrom_col]
                if moveto_piece is None:
                    continue

                if moveto_piece.status == 1 and moveto_piece.belongings == PLAYER_B and moveto_piece.animal != 7:
                    return True, (movefrom_row, movefrom_col)
                if moveto_piece.status == 0:
                    flip_list.append((movefrom_row, movefrom_col))

            if flip_list is None:
                # no rat
                return False, None
            else:
                return False, flip_list[0]

        def rat_move(row, col, movefrom_row, movefrom_col):
            self.mingPieces[PLAYER_B].append([row, col, self.board[movefrom_row][movefrom_col].animal])
            self.mingPieces[PLAYER_A].remove([row, col, self.board[row][col].animal])
            self.mingPieces[PLAYER_B].remove([movefrom_row, movefrom_col, self.board[movefrom_row][movefrom_col].animal])

            self.board[row][col] = self.board[movefrom_row][movefrom_col]
            self.board[movefrom_row][movefrom_col] = None

            self.darkPieceNum -= 1
            print("Rat First --- finish rat move")
            self.print_board()

        def rat_flip(flip_row, flip_col):
            self.board[flip_row][flip_col].status = 1
            self.add_to_ming_pieces(flip_row, flip_col)
            print("Rat First --- finish rat flip")
            self.print_board()

        idx = 0
        human_ming_piece = self.mingPieces[PLAYER_A] # [[0, 0, 5], [0, 2, 6], [2, 0, 4], [2, 1, 7], [2, 3, 3], [3, 0, 1], [3, 2, 2]]
        while idx < len(human_ming_piece):
            if human_ming_piece[idx][2] == 0:
                row = human_ming_piece[idx][0]
                col = human_ming_piece[idx][1]
                is_move, position = check_valid_move_or_flip(row, col)
                if is_move: # haven't moved
                    rat_move(row, col, position[0], position[1])
                    return True
                else:
                    if position:
                        rat_flip(position[0], position[1])
                        return True
                    else:
                        return False
            idx += 1
        else:
            return False

    def computer_turn(self, player):
        """
        also need to find a smarter player
        :param player:
        :return:
        """
        print("\n***** Computer's Turn *****")

        if self.darkPieceNum == 0:  # had no darkPiece
            self.move(player)
        elif len(self.mingPieces[PLAYER_B]) == 0: # darkPiece != 0, mingB = 0, can only flip
            self.computer_generate_flip(player)
        else:
            # had darkPiece, had mingB, can both F or M
            # rat first
            if not self.rat_strategy():
                if random.choice(['F', 'M']) == 'F':
                    self.computer_generate_flip(player)
                else:
                    self.move(player)

    def add_to_ming_pieces(self, row, col):
        self.board[row][col].status = 1
        belonging = self.board[row][col].belongings
        self.mingPieces[belonging].append([row, col, self.board[row][col].animal])

    def computer_generate_flip(self, player):
        print("\tComputer chooses to flip")
        flip_valid = False
        while not flip_valid:
            row = random.randrange(4)
            col = random.randrange(4)
            flip_valid = self.is_valid_flip(row, col, False)

        print(f"\tComputer flips the piece at ({row}, {col})")
        # Change the status
        self.add_to_ming_pieces(row, col)

        self.print_board()

        return True

    def demo_chess(self):
        demo = [
            [5, 1, 6, 5],
            [4, 7, 0, 3],
            [4, 7, 2, 3],
            [1, 0, 2, 6]
        ]

        belong = [
            ["A", "B", "B", "A"],
            ["B", "B", "A", "B"],
            ["A", "A", "B", "A"],
            ["A", "B", "A", "B"]
        ]

        status = [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ]

        self.board = [[None for i in range(4)] for i in range(4)]

        # Test 1
        # self.darkPieceNum = 0
        # self.board[0][0] = Piece(7, 'B', 1)
        # self.board[0][1] = Piece(0, 'A', 1)
        # self.board[1][1] = Piece(7, 'A', 1)
        # self.mingPieces['A'].append([0, 1, 0])
        # self.mingPieces['B'].append([0, 0, 7])
        # self.mingPieces['A'].append([1, 1, 7])

        for i in range(4):
            for j in range(4):
                # piece = Piece(demo[i][j], belong[i][j], 1)  # test the computer move, set all the status = 1
                # piece = Piece(demo[i][j], belong[i][j])  # test the flip
                piece = Piece(demo[i][j], belong[i][j], status[i][j])  # test the rat_first
                # self.mingPieces[belong[i][j]].append([i, j, demo[i][j]])
                if status[i][j] == 1:
                    self.mingPieces[belong[i][j]].append([i, j, demo[i][j]])
                self.board[i][j] = piece


if __name__ == "__main__":
    animalChess = AnimalChess()
    # animalChess.generate_puzzle()
    animalChess.demo_chess()
    # animalChess.print_board()
    animalChess.play_the_game()
