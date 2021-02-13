import tkinter as tk
from layout_classes import MainWindow

if __name__ == '__main__':
    root = tk.Tk()
    MainWindow(root)
    root.geometry('+800+500')
    root.mainloop()
