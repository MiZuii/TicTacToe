import Engine


class MainSet:

    kill = True
    input_buf = []
    board = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    def __init__(self, switch, reset, game_state):
        self.switch_val = switch
        self.reset_val = reset
        self.game_state = game_state

    def reset_board(self, buttons):
        self.board = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        for i in range(3):
            for j in range(3):
                buttons[i][j].config(text="")

    def get(self):
        try:
            temp = self.input_buf[0]
            self.input_buf.pop()
            return temp
        except IndexError:
            pass

    def add(self, arg):
        self.input_buf.append(arg)

    def empty(self):
        try:
            temp = self.input_buf[0]
            return False
        except IndexError:
            return True

    def clear(self):
        try:
            temp = self.input_buf[0]
            self.input_buf.pop()
        except IndexError:
            pass


def button_exp(row_exp, column_exp, obj):
    if obj.empty():
        if row_exp == 0:
            if column_exp == 0:
                obj.add(1)
            elif column_exp == 1:
                obj.add(2)
            elif column_exp == 2:
                obj.add(3)
        elif row_exp == 1:
            if column_exp == 0:
                obj.add(4)
            elif column_exp == 1:
                obj.add(5)
            elif column_exp == 2:
                obj.add(6)
        elif row_exp == 2:
            if column_exp == 0:
                obj.add(7)
            elif column_exp == 1:
                obj.add(8)
            elif column_exp == 2:
                obj.add(9)


def reset_val_change(game_prop):
    game_prop.reset_val = True


def switch_change(switch_obj, button, o, x):

    if switch_obj.switch_val:
        button.config(image=o)
        switch_obj.switch_val = False
    else:
        button.config(image=x)
        switch_obj.switch_val = True


def win_check(board):

    cond = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [7, 5, 3]]

    for i in cond:
        if board[i[0]] == 1 and board[i[1]] == 1 and board[i[2]] == 1:
            return 1
        elif board[i[0]] == 2 and board[i[1]] == 2 and board[i[2]] == 2:
            return 2
        else:
            pass

    o_count = 0
    for key in board:
        if board[key] == 0:
            o_count += 1
    if o_count == 0:
        return 3
    else:
        return False


def game(game_prop, buttons, label):

    player_char = True      # True = x, False = o
    player_move = player_char
    buttons_num = [[1, 0, 0], [2, 0, 1], [3, 0, 2], [4, 1, 0], [5, 1, 1], [6, 1, 2], [7, 2, 0], [8, 2, 1], [9, 2, 2]]
    cor_1 = 0
    cor_2 = 0
    label.config(text="PvE Game, Player as x")

    while game_prop.kill:

        while game_prop.reset_val is False and game_prop.game_state is True and game_prop.kill is True:

            if player_move:

                game_prop.clear()
                field = None
                j = True
                while j is True and game_prop.reset_val is False and game_prop.kill is True:
                    if game_prop.empty() is False:
                        field = game_prop.get()
                        if game_prop.board[field] == 0:
                            j = False
                        else:
                            j = True
                for key in game_prop.board:
                    if key == field and game_prop.board[key] == 0:
                        for i in buttons_num:
                            if i[0] == field:
                                cor_1 = i[1]
                                cor_2 = i[2]
                        if player_char:
                            buttons[cor_1][cor_2].config(text="x")
                            game_prop.board[field] = 1
                        else:
                            buttons[cor_1][cor_2].config(text="o")
                            game_prop.board[field] = 2
                winner = win_check(game_prop.board)
                if winner == 1:
                    game_prop.game_state = False
                    label.config(text="Game Over, X won")
                elif winner == 2:
                    game_prop.game_state = False
                    label.config(text="Game Over, O won")
                elif winner == 3:
                    game_prop.game_state = False
                    label.config(text="Game Over, Draw")
                player_move = False

            else:

                field = Engine.move(game_prop.board, player_char)

                for key in game_prop.board:
                    if key == field and game_prop.board[key] == 0:
                        for i in buttons_num:
                            if i[0] == field:
                                cor_1 = i[1]
                                cor_2 = i[2]
                        if player_char:
                            buttons[cor_1][cor_2].config(text="o")
                            game_prop.board[field] = 2
                        else:
                            buttons[cor_1][cor_2].config(text="x")
                            game_prop.board[field] = 1
                winner = win_check(game_prop.board)
                if winner == 1:
                    game_prop.game_state = False
                    label.config(text="Game Over, X won")
                elif winner == 2:
                    game_prop.game_state = False
                    label.config(text="Game Over, O won")
                elif winner == 3:
                    game_prop.game_state = False
                    label.config(text="Game Over, Draw")
                player_move = True

        if game_prop.reset_val:

            game_prop.reset_val = False
            game_prop.game_state = True
            player_char = game_prop.switch_val
            player_move = player_char
            game_prop.reset_board(buttons)
            game_prop.clear()
            if player_char:
                label.config(text="PvE Game, Player as x")
            else:
                label.config(text="PvE Game, Player as o")
