import tkinter as tk
from tkinter import ttk
from random import randint
from logic_classes import Field


class Cell(ttk.Frame):

    def __init__(self, root, lbl_text=''):
        super().__init__(master=root, width=4, height=4, borderwidth=0)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)
        self.root = root
        self.text = lbl_text
        self.opened = False
        self.bomb = True if lbl_text == '9' else False
        self.mark_bomb = False

        self.lbl_cell = ttk.Label(self,
                                  text='*' if self.bomb else lbl_text,
                                  width=4,
                                  anchor='center',

                                  # relief='sunken'
                                  )
        self.lbl_cell.grid(sticky='swen', column=0, row=0, ipady=4)

        self.btn_cell = ttk.Button(self, width=3)
        self.btn_cell.grid(sticky='swen', column=0, row=0)
        self.btn_cell.bind('<ButtonPress-3>', self.mark)
        self.btn_cell.bind('<ButtonPress-1>', self.open)
        # self.bind('<<game_over>>', self.root.end)

    def open(self, *args):
        if not self.mark_bomb and not self.opened:
            self.opened = True
            self.btn_cell.destroy()
            x, y = int(self.grid_info()['column']), int(self.grid_info()['row'])
            if not self.text:
                for i, j in Field.bomb_mapper(x, y, self.root.field_size, set()):
                    self.root.cells[i][j].open()
            if self.text == '9':
                self.lbl_cell.configure(background='red')
                self.root.event_generate('<<game_over>>')

    def mark(self, *args):
        print(args)
        self.mark_bomb = not self.mark_bomb
        if self.mark_bomb:
            self.root.event_generate('<<mark_added>>')
        else:
            self.root.event_generate('<<mark_deleted>>')
        self.btn_cell.configure(text='*' * self.mark_bomb)


class GameField(ttk.Frame):
    def __init__(self, root, field=None, field_size=(1, 1)):
        super().__init__(master=root, height=400, width=400)
        self.field_size = field_size
        self.field = field
        self.cells = []
        for i, lst in enumerate(field.field):
            self.cells.append([])
            for j, num in enumerate(lst):
                game_cell = Cell(self, lbl_text=str(num) if num else '')
                game_cell.grid(sticky='swen', column=i, row=j)
                self.cells[i].append(game_cell)
        self.bind('<<game_over>>', self.end)

    def end(self, *args):
        for x, y in self.field.bombs:
            cell = self.grid_slaves(row=y, column=x)[0]
            cell.opened = True
            cell.btn_cell.destroy()
            cell.lbl_cell.configure(background='red')
        for cell in self.grid_slaves():
            if not cell.opened:
                cell.btn_cell.unbind('<ButtonPress-1>')
                cell.btn_cell.state(['disabled'])


class MainWindow:

    def __init__(self, root):

        root.title('Igor\'s minesweeper')
        root.configure(background='#6F6F6F')
        root.columnconfigure(0, minsize=100)
        root.rowconfigure(0, minsize=25)
        self.root = root
        self.buttons = []
        self.bombs_num = 10
        self.remaining_mines = tk.IntVar()
        self.remaining_mines.set(self.bombs_num)
        self.field_size = (10, 10)
        self.mapper = Field(*self.field_size, self.bombs_num)

        self.frm_menu = ttk.Frame(root, width=400, height=50)
        self.frm_menu.grid(column=0, row=0, padx=5, pady=5, sticky='swen')

        self.btn_options = ttk.Button(self.frm_menu, text='Options', command=self.options)
        self.btn_options.grid(column=0, row=0, padx=5, pady=5)

        self.frm_game = ttk.Frame(root, width=400, height=100)
        self.frm_game.grid(column=0, row=1, padx=5, pady=5, sticky='swen')
        self.frm_game.rowconfigure(0, weight=1)
        self.frm_game.columnconfigure((0, 1, 2), weight=1)

        self.lbl_clock = ttk.Label(self.frm_game, text='Time\nWill be\nhere')
        self.lbl_clock.grid(column=0, row=0, padx=5, pady=5)

        self.btn_start = ttk.Button(self.frm_game, text='RUN!\nRUN!\nRUN!', command=self.run)
        self.btn_start.grid(column=1, row=0, padx=5, pady=5)

        self.lbl_remaining_mines = ttk.Label(self.frm_game,
                                             textvariable=self.remaining_mines
                                             )
        self.lbl_remaining_mines.grid(column=2, row=0, padx=5, pady=5)

        self.frm_field = GameField(root, field=self.mapper, field_size=self.field_size)
        self.frm_field.grid(column=0, row=2, padx=5, pady=5, sticky='swen')

        self.root.bind('<<game_over>>', self.end)

        self.root.bind('<<mark_added>>', self.mines_decrease)
        self.root.bind('<<mark_deleted>>', self.mines_increase)

        root.rowconfigure(2, weight=1)

    @staticmethod
    def options():
        pass

    def mines_decrease(self, *args):
        self.remaining_mines.set(self.remaining_mines.get() - 1)

    def mines_increase(self, *args):
        self.remaining_mines.set(self.remaining_mines.get() + 1)

    def run(self):
        for cells in self.frm_field.cells:
            for cell in cells:
                cell.destroy()
        self.frm_field.__init__(self.root,
                                field=Field(*self.field_size, self.bombs_num),
                                field_size=self.field_size)
        self.frm_field.grid(column=0, row=2, padx=5, pady=5, sticky='swen')

    def end(self, *args):
        self.btn_start.configure(text='Game\nOver!!!\nAgain?')
        print('Over')






