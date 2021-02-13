import tkinter as tk
from tkinter import ttk
from tkinter import font


class DialogWindow:

    def __init__(self, root, **kwargs):
        self.window_type = {
            'custom_window': self.custom_window,
            'record_window': self.record_window,
        }
        print(kwargs['title'])
        self.root = root
        self.kwargs = kwargs
        self.dialog = tk.Toplevel(root)
        self.dialog.resizable(False, False)
        self.dialog.title(kwargs['title'])
        self.dialog.geometry('+800+500')
        self.text_variables = {}
        self.values = []
        self.parent = kwargs['parent']
        self.type = kwargs['target']
        self.window_type[kwargs['target']]()
        self.file = FileHandler(game_type=kwargs['game_type'])

        self.buttons_frm = ttk.Frame(self.dialog)
        self.buttons_frm.grid(row=2, column=0, columnspan=3, pady=4, padx=2)
        self.ok_btn = ttk.Button(self.buttons_frm, text='OK', command=self.ok)
        self.ok_btn.grid(row=0, column=0)
        self.cancel_btn = ttk.Button(self.buttons_frm, text='Cancel', command=self.cancel)
        self.cancel_btn.grid(row=0, column=1)

        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        self.dialog.transient(self.root)
        self.dialog.wait_visibility()
        self.dialog.grab_set()
        self.dialog.wait_window()

    def ok(self):
        self.dialog.grab_release()
        self.dialog.destroy()
        self.values = [i.get() for i in self.text_variables.values()]
        print(self.values)
        if self.type == 'custom_window' and self.values[0] * self.values[1] >= self.values[2]:
            self.parent.options(self.values)
        if self.type == 'record_window':
            # self.file.read()
            self.file.update(name=self.text_variables['name'].get(), time=self.kwargs['time'])

    def cancel(self):
        self.dialog.grab_release()
        self.dialog.destroy()

    def custom_window(self):
        for i, text in enumerate(self.kwargs['labels']):
            self.text_variables[text] = tk.IntVar()
            ttk.Label(self.dialog, text=text).grid(row=0, column=i)
            ttk.Entry(self.dialog,
                      width=6,
                      textvariable=self.text_variables[text]).grid(row=1, column=i)
            self.text_variables[text].set(8)

    def record_window(self):
        for i, text in enumerate(self.kwargs['labels']):
            ttk.Label(self.dialog, text=text).grid(row=0, column=i)
        name = tk.StringVar()
        name.set('Input name')
        ttk.Entry(self.dialog, textvariable=name, width=11).grid(row=1, column=0)
        ttk.Label(self.dialog, text=self.kwargs['time']).grid(row=1, column=1)
        self.text_variables['name'] = name


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
            print(dif)
            menu_results.add_command(
                label=dif,
                # variable=hardness,
                # value=dif,
                command=lambda: self.in_print(f'<<{dif}>>'),
            )

    @staticmethod
    def in_print(value):
        print(value)


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
        self.lbl_cell.bind('<ButtonPress-1><ButtonPress-3>', self.aim_area)
        self.btn_cell.bind('<ButtonPress-3>', self.mark)

    def open(self, *args):
        if not self.mark_bomb and not self.opened:
            self.event_generate('<<game_started>>')
            self.opened = True
            self.root.closed -= 1
            self.btn_cell.destroy()
            # y, x = int(self.grid_info()['column']), int(self.grid_info()['row'])
            if not self.text:
                for i, j in self.area:
                    self.root.cells[i][j].open()
            if self.text == '9':
                self.lbl_cell.configure(background='red')
                self.root.event_generate('<<game_over>>')
            if not self.root.closed:
                self.root.event_generate('<<you_win!>>')

    def mark(self, *args):
        self.mark_bomb = not self.mark_bomb
        if self.mark_bomb:
            self.root.event_generate('<<mark_added>>')
        else:
            self.root.event_generate('<<mark_deleted>>')
        self.btn_cell.configure(compound='image' if self.mark_bomb else 'text')

    def combo(self, *args):
        self.unpressed()
        marks = sum(self.root.cells[x][y].mark_bomb for x, y in self.area)
        if self.lbl_cell['text'] and marks == int(self.lbl_cell['text']):
            for x, y in self.area:
                if not self.root.cells[x][y].opened:
                    self.root.cells[x][y].open()

    def aim_area(self, args):
        print(args.type)
        if 'ButtonPress' in args.type:
            self.root.event_generate('<<show_aim>>')

        for x, y in self.area:
            if not self.root.cells[x][y].opened and not self.root.cells[x][y].mark_bomb:
                self.root.cells[x][y].btn_cell.state(['pressed'])

    def unpressed(self, *args):

        if not args:
            self.root.event_generate('<<hide_aim>>')
        for x, y in self.area:
            if not self.root.cells[x][y].opened and not self.root.cells[x][y].mark_bomb:
                self.root.cells[x][y].btn_cell.state(['!pressed'])


class FileHandler:
    def __init__(self, **kwargs):
        self.content = {}
        self.kwargs = kwargs
        self.file_name = f"saves/{self.kwargs['game_type']}.txt"
        try:
            self.read()
        except FileNotFoundError:
            self.create()

    def read(self):
        with open(self.file_name) as file:
            for line in file:
                key_value = line.strip().split('&|&')
                self.content[key_value[0]] = key_value[1]

    def update(self, **kwargs):
        self.content[kwargs['name']] = kwargs['time']
        with open(self.file_name, 'w') as file:
            for key, value in sorted(self.content.items(), key=lambda e: float(e[1])):
                file.write(f'{key}&|&{value}\n')

    def create(self):
        with open(self.file_name, 'w') as file:
            pass
