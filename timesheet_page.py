import tkinter as tk
from tkinter import ttk
from generic_templates import FrameTemplate
import tkcalendar

class TimeSheet(FrameTemplate):

    def __init__(self, parent_frame, label, ):
        super().__init__(parent_frame)
        self.parent_frame = parent_frame
        self.label = label
        # INITIALIZE TOP AND BOTTOM FRAMES AS CONTAINERS
        self.option_frame = tk.Frame(self.parent_frame)
        self.option_frame.grid(row=1, sticky='w')
        self.time_grid_frame = tk.Frame(self.parent_frame)
        self.time_grid_frame.grid(row=2)

        # DATE AND BREAK TIME SELECT
        date_label = tk.Label(self.option_frame, text='Start Date')
        date_label.grid(row=0, column=0)
        self.calendar = tkcalendar.DateEntry(self.option_frame, date_pattern='y-mm-dd', state='readonly')
        self.calendar.grid(row=1, column=0)
        break_label = tk.Label(self.option_frame, text='Break time each day (minutes)')
        break_label.grid(row=0, column=1)
        self.break_time_entry = ttk.Combobox(self.option_frame, values=tuple(range(0, 61)), state='readonly')
        self.break_time_entry.grid(row=1, column=1)
        self.break_time_entry.set(30)

        # INITIALIZE GRID-CELL FRAMES
    def init_grid_frame(self, row, column, cell_data):
        frame = tk.Frame(self.time_grid_frame, borderwidth=1, relief='solid')
        frame.grid(row=row, column=column, sticky='nsew')
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
