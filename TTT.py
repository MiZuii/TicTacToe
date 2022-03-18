# Title: PvE Tic Tac Toe
# Description: Tic Tac Toe game with Computer engine
# Version: 1.0
# Author: Piotr Wiercigroch


from tkinter import *
import UI
import threading

# Global variables -------------------
game = UI.MainSet(True, False, True)
buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# Global variables ------------------

window = Tk()
window.title("PvE Tic Tac Toe")

x = PhotoImage(file="x.png")
o = PhotoImage(file="o.png")

label = Label(text="Elo", font=("consolas", 14))
label.pack(side="top")

buttons_frame = Frame(window)
buttons_frame.pack(side="top")

choice_button = Button(buttons_frame, image=x, command=lambda: UI.switch_change(game, choice_button, o, x))
choice_button.grid(row=1, column=1)

restart_button = Button(buttons_frame, text="Restart", font=("consolas", 18), command=lambda: UI.reset_val_change(game))
restart_button.grid(row=1, column=2)

frame = Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=("consolas", 20),
                                      width=5, height=3, command=lambda row_add=row, column_add=column: UI.button_exp(row_add, column_add, game))
        buttons[row][column].grid(row=row, column=column)

game_thread = threading.Thread(target=UI.game, args=(game, buttons, label))
game_thread.start()

window.mainloop()
game.kill = False
game_thread.join()
