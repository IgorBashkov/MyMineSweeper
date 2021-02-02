import tkinter as tk
from tkinter import ttk
from logic_classes import Field
from tkinter import font


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
        hardness = tk.StringVar()
        commands = ('Easy', 'Medium', 'Hard', 'Custom')
        for dif in commands:
            menu_game.add_radiobutton(
                label=dif,
                variable=hardness,
                value=dif,
                command=lambda: root.event_generate(f'<<{hardness.get()}>>'),
            )
            menu_results.add_command(label=dif, command=lambda: True)


class Cell(ttk.Frame):
    text_color = {'1': 'blue', '2': 'green', '3': 'red',
                  '4': 'brown', '5': 'pink', '6': 'crimson',
                  '7': 'orange', '8': 'coral', '9': 'black',
                  }

    def __init__(self, root, lbl_text='', pos_x=0, pos_y=0):
        # self.style = ttk.Style()
        # self.style.theme_use('default')
        self.flag = tk.PhotoImage(file='static/flag.gif')
        self.mine = tk.PhotoImage(file='static/mine2.gif')
        text_font = font.Font(weight='bold', size=12)
        super().__init__(master=root, width=20, height=20, borderwidth=0)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)
        # self.configure(background='#6F6F6F')
        self.root = root
        self.text = lbl_text
        self.opened = False
        self.bomb = True if lbl_text == '9' else False
        self.mark_bomb = False
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.area = self.root.field.mapper_dict[(self.pos_y, self.pos_x)]
        self.pressed = False

        self.lbl_cell = ttk.Label(self,
                                  text=lbl_text,
                                  foreground=Cell.text_color.get(lbl_text, 'black'),
                                  width=3,
                                  anchor='center',
                                  font=text_font,
                                  compound='image' if self.bomb else 'text',
                                  image=self.mine
                                  # relief='groove',
                                  )

        self.lbl_cell.grid(sticky='swen', column=0, row=0,
                           ipady=0 if self.bomb else 6,
                           ipadx=0 if self.bomb else 2)

        self.btn_cell = ttk.Button(self,
                                   width=3,
                                   command=self.open,
                                   image=self.flag,
                                   compound='text',
                                   )
        self.btn_cell.grid(sticky='swen', column=0, row=0)

        self.lbl_cell.bind('<ButtonRelease-1><ButtonRelease-3>', self.combo)
        # self.bind('<ButtonRelease-1><ButtonRelease-3>', self.unpressed)
        self.lbl_cell.bind('<ButtonPress-1><ButtonPress-3>', self.aim_area)
        self.lbl_cell.bind('<Leave>', self.unpressed)
        self.lbl_cell.bind('<Enter><ButtonPress-1><ButtonPress-3>', self.aim_area)
        self.btn_cell.bind('<Leave>', self.unpressed)
        self.btn_cell.bind('<Enter><ButtonPress-1><ButtonPress-3>', self.aim_area)
        self.btn_cell.bind('<ButtonPress-3>', self.mark)

    def open(self, *args):
        if not self.mark_bomb and not self.opened:
            self.event_generate('<<game_started>>')
            self.opened = True
            self.root.closed -= 1
            self.btn_cell.destroy()
            y, x = int(self.grid_info()['column']), int(self.grid_info()['row'])
            if not self.text:
                for i, j in self.area:
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
        self.btn_cell.configure(compound='image' if self.mark_bomb else 'text')

    def combo(self, *args):
        self.unpressed()
        self.pressed = False
        marks = sum(self.root.cells[x][y].mark_bomb for x, y in self.area)
        if marks == int(self.lbl_cell['text']):
            for x, y in self.area:
                if not self.root.cells[x][y].opened:
                    self.root.cells[x][y].open()

    def aim_area(self, *args):
        for x, y in self.area:
            if not self.root.cells[x][y].opened and not self.root.cells[x][y].mark_bomb:
                self.root.cells[x][y].btn_cell.state(['pressed'])

    def unpressed(self, *args):
        for x, y in self.area:
            if not self.root.cells[x][y].opened and not self.root.cells[x][y].mark_bomb:
                self.root.cells[x][y].btn_cell.state(['!pressed'])


class GameField(ttk.Frame):
    def __init__(self, root, mines=1,  field_size=(1, 1)):
        super().__init__(master=root, height=200, width=200)
        self.game_type = 2
        self.field_size = field_size
        self.field = Field(*field_size, mines)
        self.closed = field_size[0] * field_size[1] - mines
        self.cells = []
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
            # cell.lbl_cell.configure(background='red')
        self.unbind_open()

    def unbind_open(self, *args):
        print(args)
        for cell in self.grid_slaves():
            if not cell.opened:

                cell.btn_cell.unbind('<ButtonPress-1>')
                cell.btn_cell.unbind('<ButtonPress-3>')

                # cell.event_generate('<<mark_added>>') if not args else None
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
        self.root.bind('<<game_started>>', self.start)

        self.root.bind('<<Easy>>', lambda e: self.options((10, 10, 10)))
        self.root.bind('<<Medium>>', lambda e: self.options((15, 20, 40)))
        self.root.bind('<<Hard>>', lambda e: self.options((30, 20, 100)))
        self.root.bind('<<Custom>>', lambda e: self.options((10, 10, 10)))
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
        self.lbl_clock.configure(text='Time\nWill be\nhere')
        self.root.bind('<<game_started>>', self.start)
        self.btn_start.configure(text='Have\nFun!')

    def end(self, *args):
        self.btn_start.configure(text='Game\nOver!!!\nAgain?')
        self.lbl_clock.configure(text='End')
        print('Over')

    def win(self, *args):
        self.btn_start.configure(text='You\nWin!!!\nAgain?')
        self.lbl_clock.configure(text='End')
        print('Over')

    def start(self, *args):
        self.lbl_clock.configure(text='Tic-Tac')
        self.root.unbind('<<game_started>>')
        print('GoGoGo!')








