import tkinter as tk
from tkinter import ttk
from logic_classes import Field


class AddMenu:

    def __init__(self, root):
        root.resizable(False, False)
        root.option_add('*tearOff', False)
        menu_bar = tk.Menu(root)
        root['menu'] = menu_bar
        menu_game = tk.Menu(menu_bar)
        menu_results = tk.Menu(menu_bar)
        menu_about = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_game, label='Game')
        menu_bar.add_cascade(menu=menu_results, label='Results')
        menu_bar.add_cascade(menu=menu_about, label='About')
        commands = ('Easy', 'Medium', 'Hard', 'Custom')
        for command in commands:
            menu_game.add_command(label=command, command=lambda: True)
            menu_results.add_command(label=command, command=lambda: True)


class Cell(ttk.Frame):

    def __init__(self, root, lbl_text='', pos_x=0, pos_y=0):
        super().__init__(master=root, width=4, height=4, borderwidth=0)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)
        self.root = root
        self.text = lbl_text
        self.opened = False
        self.bomb = True if lbl_text == '9' else False
        self.mark_bomb = False
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.lbl_cell = ttk.Label(self,
                                  text='*' if self.bomb else lbl_text,
                                  width=4,
                                  anchor='center',
                                  )
        self.lbl_cell.grid(sticky='swen', column=0, row=0, ipady=4)

        self.btn_cell = ttk.Button(self, width=3, command=self.open)
        self.btn_cell.grid(sticky='swen', column=0, row=0)
        self.btn_cell.bind('<ButtonPress-3>', self.mark)
        self.lbl_cell.bind('<ButtonRelease-1><ButtonRelease-3>', self.combo)

    def open(self, *args):
        if not self.mark_bomb and not self.opened:
            self.opened = True
            self.root.closed -= 1
            self.btn_cell.destroy()
            x, y = int(self.grid_info()['column']), int(self.grid_info()['row'])
            if not self.text:
                for i, j in Field.bomb_mapper(x, y, self.root.field_size, set()):
                    self.root.cells[i][j].open()
            if self.text == '9':
                self.lbl_cell.configure(background='red')
                self.root.event_generate('<<game_over>>')
            if not self.root.closed:
                self.root.event_generate('<<you_win!>>')
                print('Win')

    def mark(self, *args):
        self.mark_bomb = not self.mark_bomb
        if self.mark_bomb:
            self.root.event_generate('<<mark_added>>')
        else:
            self.root.event_generate('<<mark_deleted>>')
        self.btn_cell.configure(text='*' * self.mark_bomb)

    def combo(self, *args):
        area = Field.bomb_mapper(
            self.pos_x,
            self.pos_y,
            self.root.field_size,
            set()
        )
        marks = sum(self.root.cells[x][y].mark_bomb for x, y in area)
        if marks == int(self.lbl_cell['text']):
            for x, y in area:
                if not self.root.cells[x][y].opened:
                    self.root.cells[x][y].open()


class GameField(ttk.Frame):
    def __init__(self, root, mines=1,  field_size=(1, 1)):
        super().__init__(master=root, height=400, width=400)
        self.field_size = field_size
        self.field = Field(*field_size, mines)
        self.closed = field_size[0] * field_size[1] - mines
        self.cells = []
        for i, lst in enumerate(self.field.field):
            self.cells.append([])
            for j, num in enumerate(lst):
                game_cell = Cell(self,
                                 lbl_text=str(num) if num else '',
                                 pos_x=i,
                                 pos_y=j,
                                 )
                game_cell.grid(sticky='swen', column=i, row=j)
                self.cells[i].append(game_cell)
        self.bind('<<game_over>>', self.end)
        self.bind('<<you_win!>>', self.unbind_open)

    def end(self, *args):
        for x, y in self.field.bombs:
            cell = self.grid_slaves(row=y, column=x)[0]
            cell.opened = True
            cell.btn_cell.destroy()
            cell.lbl_cell.configure(background='red')
        self.unbind_open()

    def unbind_open(self, *args):
        for cell in self.grid_slaves():
            if not cell.opened:
                cell.btn_cell.unbind('<ButtonPress-1>')
                cell.btn_cell.unbind('<ButtonPress-3>')
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
        self.remaining_mines.set(self.bombs_num)
        self.field_size = (10, 10)

        self.frm_game = ttk.Frame(root, width=400, height=100)
        self.frm_game.grid(column=0, row=0, padx=5, pady=5, sticky='swen')
        self.frm_game.rowconfigure(0, weight=0, minsize=70)
        self.frm_game.columnconfigure((0, 1, 2), weight=1, minsize=93)

        self.lbl_clock = ttk.Label(self.frm_game, text='Time\nWill be\nhere')
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

        root.rowconfigure(2, weight=1)

    @staticmethod
    def options():
        pass

    def mines_decrease(self, *args):
        self.remaining_mines.set(self.remaining_mines.get() - 1)

    def mines_increase(self, *args):
        self.remaining_mines.set(self.remaining_mines.get() + 1)

    def restart(self):
        for cells in self.frm_field.cells:
            for cell in cells:
                cell.destroy()
        self.frm_field.__init__(self.root,
                                mines=self.bombs_num,
                                field_size=self.field_size)
        self.frm_field.grid(column=0, row=1, padx=5, pady=5, sticky='swen')
        self.remaining_mines.set(self.bombs_num)
        self.btn_start.configure(text='Have\nFun!')

    def end(self, *args):
        self.btn_start.configure(text='Game\nOver!!!\nAgain?')
        print('Over')

    def win(self, *args):
        self.btn_start.configure(text='You\nWin!!!\nAgain?')
        print('Over')






