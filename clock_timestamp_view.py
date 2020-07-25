import tkinter as tk
from tkinter import ttk
from clock_on_page import ClockOn
from timesheet_page import TimeSheet

class MainView:

    def __init__(self, parent):
        self.parent = parent
        self.nb = tk.ttk.Notebook(self.parent, width=300, height=300)
        self.nb.grid()


        # The frame which will contain the clock on app
        self.clock_on_frame = tk.Frame(self.nb)
        self.nb.add(self.clock_on_frame, text='Clock On')
        self.clock_on_app = ClockOn(self.clock_on_frame, 'Clock on working')

        # The frame which will contain the time sheet app
        self.timesheet_app = tk.Frame(self.nb)
        self.nb.add(self.timesheet_app, text='Time Sheet')
        self.timesheet_app = TimeSheet(self.timesheet_app, 'Time sheet working')

        # The frame which will contain the alter hour app
        self.alter_hour_page = tk.Frame(self.nb)
        self.nb.add(self.alter_hour_page, text='Alter hours')
        self.alter_hour_page = ClockOn(self.alter_hour_page, 'Alter hours is working')

