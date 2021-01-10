import tkinter as tk
from tkinter import ttk
from random import randint
from logic_classes import Field


class Cell(ttk.Frame):

    def __init__(self, root, lbl_text=''):
        super().__init__(master=root, width=4, height=4)
        self.root = root
        self.text = lbl_text
        self.opened = False
        self.bomb = True if lbl_text == '9' else False
        self.mark_bomb = False

        self.lbl_cell = ttk.Label(self,
                                  text='*' if self.bomb else lbl_text,
                                  width=3)
        self.lbl_cell.grid(sticky='swen', column=0, row=0)

        self.btn_cell = ttk.Button(self, text='',
                                   width=3,
                                   command=self.open)
        self.btn_cell.grid(sticky='swen', column=0, row=0)
        self.btn_cell.bind('<ButtonPress-3>', self.mark)

    def open(self, *args):
        if not self.mark_bomb and not self.opened:
            self.opened = True
            self.btn_cell.grid_remove()
            x, y = int(self.grid_info()['column']), int(self.grid_info()['row'])
            if not self.text:
                for i, j in Field.bomb_mapper(x, y, self.root.field_size, set()):
                    self.root.cells[i][j].btn_cell.invoke()

    def mark(self, *args):
        self.mark_bomb = not self.mark_bomb
        self.btn_cell.configure(text='*' * self.mark_bomb)


class GameField(ttk.Frame):
    def __init__(self, root, field=None, field_size=(1, 1)):
        super().__init__(master=root, height=400, width=400)
        # mapper = kwargs['mapper']
        self.field_size = field_size
        print(field)
        self.cells = []
        for i, lst in enumerate(field.field):
            self.cells.append([])
            for j, num in enumerate(lst):
                game_cell = Cell(self, lbl_text=str(num) if num else '')
                game_cell.grid(sticky='swen', column=i, row=j)
                self.cells[i].append(game_cell)


class MainWindow:

    def __init__(self, root):
        root.title('Igor\'s minesweeper')
        root.configure(background='#6F6F6F')
        root.columnconfigure(0, minsize=100)
        root.rowconfigure(0, minsize=100)
        self.buttons = []
        self.bombs_num = 10
        self.field_size = (10, 10)
        self.mapper = Field(10, 10, 10)
        # print(self.mapper)

        self.frm_menu = ttk.Frame(root, width=400, height=100)
        self.frm_menu.grid(column=0, row=0, padx=5, pady=5, sticky='swen')

        self.btn_options = ttk.Button(self.frm_menu, text='Options', command=self.options)
        self.btn_options.grid(column=0, row=0, padx=5, pady=5)

        self.frm_game = ttk.Frame(root, width=400, height=100)
        self.frm_game.grid(column=0, row=1, padx=5, pady=5, sticky='swen')
        self.frm_game.rowconfigure(0, weight=1)

        self.lbl_clock = ttk.Label(self.frm_game, text='Time\nWill be\nhere')
        self.lbl_clock.grid(column=0, row=0, padx=5, pady=5)

        self.btn_start = ttk.Button(self.frm_game, text='RUN!\nRUN!\nRUN!', command=self.run)
        self.btn_start.grid(column=1, row=0, padx=5, pady=5)

        self.lbl_remaining_mines = ttk.Label(self.frm_game, text='Remaining\nmines')
        self.lbl_remaining_mines.grid(column=2, row=0, padx=5, pady=5)

        self.frm_field = GameField(root, field=self.mapper, field_size=self.field_size)
        self.frm_field.grid(column=0, row=2, padx=5, pady=5, sticky='swen')
        # self.field()

        root.rowconfigure(2, weight=1)

    @staticmethod
    def options():
        pass

    @staticmethod
    def run():
        pass

    def hide_button(self, i, j):
        print(i, j)
        self.buttons[int(i)][int(j)].grid_remove()



