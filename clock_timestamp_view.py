import tkinter as tk
from tkinter import ttk
from clock_on_page import ClockOn

class MainView:

    def __init__(self, parent):

        self.parent = parent
        nb = tk.ttk.Notebook(self.parent)
        nb.grid()


