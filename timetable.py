#!/usr/bin/python3
from clock_timestamp_model import Model
import tkinter as tk
from tkinter import ttk, messagebox
from timesheet_page import TimeSheet
from alter_hour_page import AlterHour
import exception_utility as excep
from datetime_utility import week_date, week_dates
from datetime_utility import convert_min_overflow, ex_break_time
import settings
import numpy as np
from datetime import datetime
from datetime import timedelta

class Controller:

    def __init__(self):
        # INITIALIZE TK INTERFACE
        self.root = tk.Tk()
        self.root.title('Time System')
        self.root.resizable(False, False)
        # INITIALIZE MODEL
        self.model = Model()

        # ADD NOTEBOOK WIDGET TO ROOT LAYER
        self.nb = tk.ttk.Notebook(self.root)
        self.nb.grid(sticky='nsew')

        # INITIALIZE TIME SHEET APP AND FRAME
        self.timesheet_frame = tk.Frame(self.nb)
        self.nb.add(self.timesheet_frame, text='Time Sheet')
        self.timesheet_app = TimeSheet(self.timesheet_frame, 'HR MIN format, Break time 30Mins')

        # INITIALIZE ALTER HOUR APP AND FRAME
        self.alter_hour_frame = tk.Frame(self.nb)
        self.nb.add(self.alter_hour_frame, text='Admin')
        self.alter_hour_app = AlterHour(self.alter_hour_frame)

        # INITIALIZE BACKEND DATA, POPULATES EMP LISTS / TIMES
        self.init_app()

        self.event_trigger()

        self.root.mainloop()

    # EVENT TRIGGER TO UPDATE WINDOW SIZE FOR EACH NOTEBOOK APP
    def _on_tab_changed(self, event):
        # gets the widget clicked and configures the height and width.
        event.widget.update_idletasks()
        tab = event.widget.nametowidget(event.widget.select())

        event.widget.configure(height=tab.winfo_reqheight(), width=tab.winfo_reqwidth()+30)
        # UPDATES EACH TAB'S CONTENT WHEN CLICKED ON
        selected_tab = event.widget.tab(event.widget.select(), 'text')
        # if selected_tab == 'Time Sheet':
        #     self.display_timesheet_grid(self.timesheet_app.calendar.get(), week_date(self.timesheet_app.calendar.get(),7))
        if selected_tab == 'Alter hours':
            if self.alter_hour_app.employee:
                self.update_show_time()


    # BUNDLE OF EVENT TRIGGERS FROM THE DIFFERENT APP VIEWS.
    def event_trigger(self):
        # NOTEBOOK EVENTS
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        # ADMIN APP EVENTS
        self.alter_hour_app.emp_combobox.bind("<<ComboboxSelected>>", self.alter_emp_select)
        self.alter_hour_app.calendar.bind("<<DateEntrySelected>>", self.alter_date_select)
        self.alter_hour_app.on_button.bind("<ButtonRelease-1>", self.alter_on)
        self.alter_hour_app.off_button.bind("<ButtonRelease-1>", self.alter_off)
        self.alter_hour_app.create_emp_button.bind("<ButtonRelease-1>", self.create_emp)
        # TIME SHEET EVENTS
        self.timesheet_app.calendar.bind("<<DateEntrySelected>>", self.date_select)
        # self.timesheet_app.break_time_entry.bind("<<ComboboxSelected>>", self.break_time_select)

    def init_app(self):
        self.display_timesheet_grid(self.model.get_current_date(), week_date(self.model.get_current_date(), 6))
        self.alter_hour_app.populate_emp_list(self.model.get_all_emp())

        # CREATE EMPLOYEE
    def create_emp(self, event):
        if self.alter_hour_app.ask_password():
            new_emp = self.alter_hour_app.new_employee()
            if new_emp:
                self.model.create_new_emp(new_emp)
                messagebox.showinfo('Success', f'{new_emp} added!')
                self.alter_hour_app.populate_emp_list(self.model.get_all_emp())
                # self.display_timesheet_grid(self.model.get_current_date(), 7)
        return 'break'

    # EMPLOYEE LIST EVENT CALL FOR WHEN AN EMPLOYEE IS SELECTED FROM THE LIST
    def alter_emp_select(self, event):
        self.alter_hour_app.on_combo_select()
        self.update_show_time()

        # EVENT CALL FOR WHEN A DATE IS SELECTED IN THE ALTER HOUR APP
    def alter_date_select(self, event):
        self.alter_hour_app.on_date_select()
        for time_type in ['clock_on', 'clock_off']:
            self.show_time(time_type, self.model.get_id_by_name(self.alter_hour_app.employee),
                           self.alter_hour_app.date_value)


    def alter_on(self, event):
        self.alter_time('clock_on')
        return 'break'

    def alter_off(self, event):
        self.alter_time('clock_off')
        return 'break'

    # UPDATES BOTH TIME TYPES
    def update_show_time(self):
        for time_type in ['clock_on', 'clock_off']:
            self.show_time(time_type, self.model.get_id_by_name(self.alter_hour_app.employee),
                           self.alter_hour_app.date_value)


    # UPDATE ALTER TIMES FOR GIVEN TIME TYPE
    def show_time(self, time_type, _id, _date):
        time_value = self.model.get_time(time_type, _id, _date)
        if time_value:
            if time_type == 'clock_on':
                self.alter_hour_app.on_button['text'] = time_value
            elif time_type == 'clock_off':
                self.alter_hour_app.off_button['text'] = time_value
        else:
            if time_type == 'clock_on':
                self.alter_hour_app.on_button['text'] = 'None'
            elif time_type == 'clock_off':
                self.alter_hour_app.off_button['text'] = 'None'

    # SET ALTERED TIME RECORD
    def alter_time(self, time_type):
        emp_id = self.model.get_id_by_name(self.alter_hour_app.employee)
        clock_off_time = self.model.get_time('clock_off', emp_id, self.alter_hour_app.date_value)
        clock_on_time = self.model.get_time('clock_on', emp_id, self.alter_hour_app.date_value)
        try:
            # Throw error if user not selected
            if not self.alter_hour_app.employee:
                raise excep.NoEmployeeSelected
            # Throw error if password is incorrect
            if not self.alter_hour_app.ask_password():
                raise excep.IncorrectPassword
            # Launch alter time dialog if no errors
            self.alter_hour_app.alter_time()
            # Continue if cancel is not clicked
            if self.alter_hour_app.time_value:
                # Run if either clock on/off time exists
                if clock_on_time or clock_off_time:
                    # If the user selects clock on time to be altered
                    if time_type == 'clock_on':
                        # Checks if clock off time exists
                        if clock_off_time:
                            # If clock off exists, check if the time selected (clock on) is less than clock off
                            if self.alter_hour_app.time_value <= clock_off_time:
                                self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                            else:
                                raise excep.IllogicalTime
                        # If clock off time does not exist, no need to validate.
                        else:
                            self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                    # Handles clock off selection.
                    elif time_type == 'clock_off':
                        if clock_on_time:
                            if clock_on_time <= self.alter_hour_app.time_value:
                                self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                            else:
                                raise excep.IllogicalTime
                        else:
                            self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                # If both clock on and clock off time does not exist, allow admin to immediately create record.
                else:
                    self.model.create_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                # Update the labels accordingly.
                self.update_show_time()

        except excep.IncorrectPassword:
            messagebox.showerror('Access denied', 'Incorrect password')
            return 'break'

        except excep.IllogicalTime:
            messagebox.showinfo('Attention', 'Clock ON time must be less than Clock OFF time')
            return 'break'

        except excep.NoEmployeeSelected:
            messagebox.showinfo('Attention', 'No Employee seleceted')
            return 'break'

    # DATE SELECTOR FOR TIME SHEET APP EVENT CALL
    def date_select(self, event):
        self.timesheet_app.clear_grid()
        selected_date = event.widget.get()

        self.display_timesheet_grid(selected_date, week_date(selected_date, 6))
        event.widget.update_idletasks()
        self.nb.configure(height=self.timesheet_frame.winfo_reqheight(),
                          width=self.timesheet_frame.winfo_reqwidth()+30)

    #
    # def break_time_select(self, event):
    #     self.timesheet_app.clear_grid()
    #     self.display_timesheet_grid(self.timesheet_app.calendar.get(), week_date(self.timesheet_app.calendar.get(),7))

    def display_timesheet_grid(self, start_date, end_date):
        data = self.model.joined_date_table(start_date, end_date)
        emp_set = {record[1] for record in data}
        date_headers = week_dates(start_date, 7)

        for row, emp in enumerate(emp_set, 1):
            self.timesheet_app.init_grid_frame(row, 0, emp)
            emp_records = []
            total_hours = 0
            for records in data:     # Loop through the joined data table
                if records[1] == emp:    # For each employee
                    emp_records.append((emp, records[2], records[3]))   # Append work date and hours to emp_records

            for column, date in enumerate(date_headers):
                self.timesheet_app.init_grid_frame(0, column+1, date)  # Create the column headers
                self.timesheet_app.init_grid_frame(row, column+1)   # Create timetable layout (grids)

            for record in emp_records:
                date_column = record[1].day - datetime.strptime(start_date, '%Y-%m-%d').day     # Calculate column index
                hours_worked = record[2].seconds//60    # Get hours worked
                total_hours += hours_worked
                self.timesheet_app.init_grid_frame(row, date_column+1, hours_worked)    # Populate it according to column and row index

            self.timesheet_app.init_grid_frame(0, len(date_headers)+1, 'Total Hours')   # Create Total hour header
            self.timesheet_app.init_grid_frame(row, len(date_headers)+1, total_hours)   # Populate total hours



if __name__ == '__main__':
    c = Controller()
