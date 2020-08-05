import tkinter as tk
from tkinter import ttk
from generic_templates import FrameTemplate
import tkcalendar

class TimeSheet(FrameTemplate):

    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.parent_frame = parent_frame

        # INITIALIZE TOP AND BOTTOM FRAMES AS CONTAINERS
        self.label = tk.Label(self.parent_frame, text='HR MIN format, Break time 30Mins')
        self.label.grid()
        self.date_frame = tk.Frame(self.parent_frame)
        self.date_frame.grid(row=1, sticky='w')
        self.time_grid_frame = tk.Frame(self.parent_frame)
        self.time_grid_frame.grid(row=2)

        self.calendar = tkcalendar.DateEntry(self.date_frame, date_pattern='y-mm-dd', state='readonly')
        self.calendar.grid()

        # INITIALIZE GRID-CELL FRAMES
    def init_grid_frame(self, num_emp, days, cell_data):
        frame = tk.Frame(self.time_grid_frame, borderwidth=1, relief='solid')
        frame.grid(row=num_emp, column=days, sticky='nsew')
        if cell_data is None:
            label = tk.Label(frame)
        else:
            label = tk.Label(frame, text=cell_data)
        label.grid()

    def clear_grid(self):
        self.time_grid_frame.destroy()
        self.time_grid_frame = tk.Frame(self.parent_frame)
        self.time_grid_frame.grid(row=2)

    # def display_updated_timesheet(self, row, column, hours_worked):
    #         frame = tk.Frame(self.time_grid_frame, bg='blue')
    #         frame.grid(row=row, column=column)
    #         label = tk.Label(frame, text=hours_worked)
    #         label.grid()
    #



    # requires date selected
    # needs all employees
    # needs employee times based on date
    # needs hours worked
    # needs total hours
