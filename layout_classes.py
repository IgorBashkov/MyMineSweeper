import tkinter as tk
from tkinter import ttk
from logic_classes import Field
from elements import AddMenu, Cell, DialogWindow
import threading
import time


class GameField(ttk.Frame):
    def __init__(self, root, mines=1,  field_size=(1, 1)):
        super().__init__(master=root, height=200, width=200)
        self.game_type = 2
        self.field_size = field_size
        self.field = Field(*field_size, mines)
        self.closed = field_size[0] * field_size[1] - mines
        self.cells = []
        self.pressed = False
        for i, lst in enumerate(self.field.field):
            self.cells.append([])
            for j, num in enumerate(lst):
                game_cell = Cell(self,
                                 lbl_text=str(num) if num else '',
                                 pos_x=j,
                                 pos_y=i,
                                 )
                game_cell.grid(sticky='swen', column=j, row=i)
                self.cells[i].append(game_cell)
        self.bind('<<game_over>>', self.end)
        self.bind('<<you_win!>>', self.unbind_open)

    def end(self, *args):
        for y, x in self.field.bombs:
            cell = self.grid_slaves(row=y, column=x)[0]
            cell.opened = True
            cell.btn_cell.destroy()
        self.unbind_open()

    def unbind_open(self, *args):
        for cell in self.grid_slaves():
            if not cell.opened:
                cell.btn_cell.unbind('<ButtonPress-1>')
                cell.btn_cell.unbind('<ButtonPress-3>')
                cell.btn_cell.configure(compound='text' if not args else 'image')
                cell.btn_cell.state(['disabled'])


class MainWindow:

    def __init__(self, root):

        root.title('Igor\'s minesweeper')
        AddMenu(root)
        root.configure(background='#6F6F6F')
        root.columnconfigure(0, minsize=100)
        self.root = root
        self.buttons = []
        self.bombs_num = 10
        self.remaining_mines = tk.IntVar()
        self.time = tk.IntVar()
        self.start_time = None
        self.end_time = None
        self.clock = None
        self.remaining_mines.set(self.bombs_num)
        self.field_size = (10, 10)

        self.frm_game = ttk.Frame(root, width=400, height=100)
        self.frm_game.grid(column=0, row=0, padx=5, pady=5, sticky='swen')
        self.frm_game.rowconfigure(0, weight=0, minsize=70)
        self.frm_game.columnconfigure((0, 1, 2), weight=1, minsize=93)

        self.lbl_clock = ttk.Label(self.frm_game, textvariable=self.time)

        self.lbl_clock.grid(column=0, row=0, padx=5, pady=5)

        self.btn_start = ttk.Button(self.frm_game, text='Wait\nfor\nmove', command=self.restart)
        self.btn_start.grid(column=1, row=0, padx=5, pady=5, sticky='sn')

        self.lbl_remaining_mines = ttk.Label(self.frm_game,
                                             textvariable=self.remaining_mines
                                             )
        self.lbl_remaining_mines.grid(column=2, row=0, padx=5, pady=5)

        self.frm_field = GameField(root,
                                   mines=self.bombs_num,
                                   field_size=self.field_size,
                                   )
        self.frm_field.grid(column=0, row=1, padx=5, pady=5, sticky='swen')

        self.root.bind('<<game_over>>', self.end)
        self.root.bind('<<mark_added>>', self.mines_decrease)
        self.root.bind('<<mark_deleted>>', self.mines_increase)
        self.root.bind('<<you_win!>>', self.win)
        self.root.bind('<<game_started>>', self.start)

        self.root.bind('<<Easy>>', lambda e: self.options((10, 10, 10)))
        self.root.bind('<<Medium>>', lambda e: self.options((15, 20, 40)))
        self.root.bind('<<Hard>>', lambda e: self.options((30, 20, 100)))
        self.root.bind('<<Custom>>', self.custom)

        root.rowconfigure(2, weight=1)

    def options(self, opt=(10, 10, 10), *args):
        self.field_size = opt[:-1]
        self.bombs_num = opt[-1]
        self.restart()

    def mines_decrease(self, *args):
        self.remaining_mines.set(self.remaining_mines.get() - 1)

    def mines_increase(self, *args):
        self.remaining_mines.set(self.remaining_mines.get() + 1)

    def restart(self):
        self.frm_field.destroy()
        self.frm_field.__init__(self.root,
                                mines=self.bombs_num,
                                field_size=self.field_size)
        self.frm_field.grid(column=0, row=1, padx=5, pady=5, sticky='swen')
        self.remaining_mines.set(self.bombs_num)
        self.root.bind('<<game_started>>', self.start)
        self.time.set(0)
        self.btn_start.configure(text='Have\nFun!')

    def end(self, *args):
        self.clock.cancel()
        self.btn_start.configure(text='Game\nOver!!!\nAgain?')
        self.lbl_clock.unbind('<<Rise_time>>')
        print('Over')

    def win(self, *args):
        self.clock.cancel()
        self.btn_start.configure(text='You\nWin!!!\nAgain?')
        self.lbl_clock.unbind('<<Rise_time>>')
        self.end_time = time.time() - self.start_time
        print(f'Over by {self.end_time}')

    def start(self, *args):
        self.tik_tak()
        self.start_time = time.time()
        self.lbl_clock.bind('<<Rise_time>>',
                            lambda e: self.time.set(self.time.get() + 1))
        self.root.unbind('<<game_started>>')
        print('GoGoGo!')

    def tik_tak(self):
        self.clock = threading.Timer(1, self.tik_tak)
        self.clock.daemon = True
        self.lbl_clock.event_generate('<<Rise_time>>')
        self.clock.start()

    def custom(self, event):
        DialogWindow(self.root, first_text='Mines', second_text='Field')


