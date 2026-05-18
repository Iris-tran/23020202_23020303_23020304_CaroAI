# main.py
import tkinter as tk
from gui import GameBoard

if __name__ == "__main__":
    root = tk.Tk()
    app = GameBoard(root)
    root.mainloop()