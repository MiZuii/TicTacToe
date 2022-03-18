# Tic Tac Toe Game engine
# Version: 1.5
# Author: Piotr Wiercigroch
import random


class EngineSquareObj:

    def __init__(self, field, char, depth):
        self.square = field                         # square number
        self.char = char                            # what character is on the square
        self.depth = depth                      # move depth


class EngineBoardObj:

    def __init__(self, board):
        for i in range(1, 10):
            name = "s" + str(i)
            setattr(self, name, EngineSquareObj(i, board[i], 0))

    def possible_moves(self):
        moves_list = []
        # forced moves

        cond = [[1, 2, 3], [2, 3, 1], [1, 3, 2], [4, 5, 6], [5, 6, 4], [4, 6, 5], [7, 8, 9], [8, 9, 7], [7, 9, 8],
                [1, 4, 7], [4, 7, 1], [1, 7, 4], [2, 5, 8], [5, 8, 2], [2, 8, 5], [3, 6, 9], [6, 9, 3], [3, 9, 6],
                [1, 5, 9], [5, 9, 1], [1, 9, 5], [7, 5, 3], [5, 3, 7], [3, 7, 5]]

        for i in cond:
            if self.__getattribute__("s" + str(i[0])).char == 1 and\
                    self.__getattribute__("s" + str(i[1])).char == 1 or\
                    self.__getattribute__("s" + str(i[0])).char == 2 and\
                    self.__getattribute__("s" + str(i[1])).char == 2:
                if not self.__getattribute__("s" + str(i[2])).char:
                    moves_list.append(i[2])

        if moves_list:
            return moves_list

        # normal moves

        for i in self.__dict__.keys():
            if self.__getattribute__(i).char == 0:
                moves_list.append(self.__getattribute__(i).square)

        random.shuffle(moves_list)
        return moves_list

    def x_turn(self):

        x_count = 0
        o_count = 0

        for i in self.__dict__.keys():
            if self.__getattribute__(i).char == 1:
                x_count += 1
            elif self.__getattribute__(i).char == 2:
                o_count += 1

        if x_count == o_count:
            return True
        else:
            return False

    def current_depth(self):

        depth = 0

        for i in self.__dict__.keys():
            if self.__getattribute__(i).depth > depth:
                depth = self.__getattribute__(i).depth

        return depth

    def win_check(self):

        cond = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [7, 5, 3], ]

        for i in cond:
            if self.__getattribute__("s" + str(i[0])).char == 1 and self.__getattribute__("s" + str(i[1])).char == 1\
                    and self.__getattribute__("s" + str(i[2])).char == 1:
                return 1
            elif self.__getattribute__("s" + str(i[0])).char == 2 and self.__getattribute__("s" + str(i[1])).char == 2\
                    and self.__getattribute__("s" + str(i[2])).char == 2:
                return 2
        return 0


def is_first_run(board):
    if type(board) is EngineBoardObj:
        return False
    elif type(board) is dict:
        return True


def val_sum(vals):
    sum_list = [0, 0]
    for i in vals:
        sum_list[0] += i[0]
        sum_list[1] += i[1]
    return sum_list


def final_move(possible_moves, vals, char):
    x_val, o_val, x_max, o_max = [], [], [], []

    for i in vals:
        x_val.append(i[0])
        o_val.append(i[1])

    if char:
        x_val.sort()
        for i in vals:
            if i[0] == x_val[0]:
                o_max.append(i[1])
        o_max.sort(reverse=True)
        return possible_moves[vals.index([x_val[0], o_max[0]])]
    else:
        o_val.sort()
        for i in vals:
            if i[1] == o_val[0]:
                x_max.append(i[0])
        x_max.sort(reverse=True)
        return possible_moves[vals.index([x_max[0], o_val[0]])]


def depth_exponent(depth):

    for i in range(1, 10):
        if depth == i:
            return pow(10, 9 - i)


def move(board_pass, char):

    board = board_pass

    if is_first_run(board_pass):
        board = EngineBoardObj(board_pass)

    current_depth = board.current_depth()
    winner = board.win_check()
    depth_ex = depth_exponent(current_depth)
    if winner:
        if current_depth > 0:
            if winner == 1:
                return [depth_ex, 0]
            else:
                return [0, depth_ex]
        else:
            return 1

    x_turn = board.x_turn()
    poss_moves = board.possible_moves()
    returned_values = []
    if poss_moves:
        for i in poss_moves:
            temp_name = "s" + str(i)

            if x_turn:
                board.__getattribute__(temp_name).char = 1
                board.__getattribute__(temp_name).depth = current_depth + 1
            else:
                board.__getattribute__(temp_name).char = 2
                board.__getattribute__(temp_name).depth = current_depth + 1

            returned_values.append(move(board, char))

            board.__getattribute__(temp_name).char = 0
            board.__getattribute__(temp_name).depth = 0
        if current_depth > 0:
            return val_sum(returned_values)
        else:
            return final_move(poss_moves, returned_values, char)
    else:
        return [0, 0]
