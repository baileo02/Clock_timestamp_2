#!/usr/bin/python3
from clock_timestamp_model import Model
import tkinter as tk
from tkinter import ttk, messagebox
from clock_on_page import ClockOn
from timesheet_page import TimeSheet
from alter_hour_page import AlterHour
import exception_utility as excep
from datetime_utility import week_dates
from datetime_utility import convert_min_overflow, ex_break_time
import settings


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

        # INITIALIZE CLOCK ON APP AND FRAME
        self.clock_on_frame = tk.Frame(self.nb)
        self.nb.add(self.clock_on_frame, text='Clock On')
        self.clock_on_app = ClockOn(self.clock_on_frame)

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

        # HANDLES AND REDIRECTS EVENTS FROM VIEW
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
        if selected_tab == 'Clock On':
            if self.clock_on_app.employee:
                self.update_clock_time()
        if selected_tab == 'Time Sheet':
            self.display_timesheet_grid(self.timesheet_app.calendar.get(), 7)
        if selected_tab == 'Alter hours':
            if self.alter_hour_app.employee:
                self.update_show_time()

    def init_app(self):
        self.clock_on_app.populate_emp_list(self.model.get_all_emp())
        self.display_timesheet_grid(self.model.get_current_date(), 7)
        self.alter_hour_app.populate_emp_list(self.model.get_all_emp())

    # BUNDLE OF EVENT TRIGGERS FROM THE DIFFERENT APP VIEWS.
    def event_trigger(self):
        # NOTEBOOK EVENTS
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        # CLOCK APP EVENTS
        self.clock_on_app.combobox.bind("<<ComboboxSelected>>", self.emp_select)
        self.clock_on_app.on_button.bind("<ButtonRelease-1>", self.clock_on)
        self.clock_on_app.off_button.bind("<ButtonRelease-1>", self.clock_off)
        # ADMIN APP EVENTS
        self.alter_hour_app.emp_combobox.bind("<<ComboboxSelected>>", self.alter_emp_select)
        self.alter_hour_app.calendar.bind("<<DateEntrySelected>>", self.alter_date_select)
        self.alter_hour_app.on_button.bind("<ButtonRelease-1>", self.alter_on)
        self.alter_hour_app.off_button.bind("<ButtonRelease-1>", self.alter_off)
        self.alter_hour_app.create_emp_button.bind("<ButtonRelease-1>", self.create_emp)
        # TIME SHEET EVENTS
        self.timesheet_app.calendar.bind("<<DateEntrySelected>>", self.date_select)
        self.timesheet_app.break_time_entry.bind("<<ComboboxSelected>>", self.break_time_select)

    # CREATE EMPLOYEE
    def create_emp(self, event):
        if self.alter_hour_app.ask_password():
            new_emp = self.alter_hour_app.new_employee()
            if new_emp:
                self.model.create_new_emp(new_emp)
                messagebox.showinfo('Success', f'{new_emp} added!')
                self.clock_on_app.populate_emp_list(self.model.get_all_emp())
                self.alter_hour_app.populate_emp_list(self.model.get_all_emp())
                self.display_timesheet_grid(self.model.get_current_date(), 7)
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
        self.display_timesheet_grid(selected_date, 7)

    def break_time_select(self, event):
        self.timesheet_app.clear_grid()
        self.display_timesheet_grid(self.timesheet_app.calendar.get(), 7)

    def display_timesheet_grid(self, selected_date, days):
        for row, emp in enumerate(self.model.get_all_emp(), 1):
            emp_id = self.model.get_id_by_name(emp)
            dates = []
            self.timesheet_app.init_grid_frame(row, 0, emp)
            for column, date in enumerate(week_dates(selected_date, days)):
                self.timesheet_app.init_grid_frame(0, column + 1, date)
                self.timesheet_app.init_grid_frame(row, column + 1,
                                                   self.model.get_hours_worked(emp_id, date))
                dates.append(date)
            self.timesheet_app.init_grid_frame(0, days + 1, 'Total')
            self.timesheet_app.init_grid_frame(0, days + 2, 'Break Total')
            self.timesheet_app.init_grid_frame(row, days + 1,
                                               self.model.get_total_hours(emp_id, dates))
            if self.model.get_num_days_worked(dates, emp_id) > 0:
                break_time = self.model.get_num_days_worked(dates, emp_id) * self.timesheet_app.break_time_entry.get()
                self.timesheet_app.init_grid_frame(row, days + 2,
                                                   ex_break_time(self.model.get_total_hours(emp_id, dates), convert_min_overflow([0, int(break_time)])))

    def clock_on(self, event):
        try:
            if self.clock_on_app.employee:
                self.clock_on_app.click_on()
                self.model.create_time_record(self.clock_on_app.time_type,
                                              self.model.get_id_by_name(self.clock_on_app.employee),
                                              self.model.get_current_date(), self.model.get_current_time())
                self.show_clock_time('clock_on', self.model.get_id_by_name(self.clock_on_app.employee),
                                     self.model.get_current_date())
            else:
                raise excep.NoEmployeeSelected
        except excep.NoEmployeeSelected:
            messagebox.showinfo('Attention', 'No employee selected')
            return 'break'
        except excep.RecordAlreadyExists:
            messagebox.showinfo('Attention', 'Employee has already clocked on today')
            return 'break'
    # CLOCK ON AND OFF BUTTON EVENT CALLS

    def clock_off(self, event):
        try:
            if self.clock_on_app.employee:
                self.clock_on_app.click_off()
                emp_id = self.model.get_id_by_name(self.clock_on_app.employee)
                # CHECK IF CLOCK OFF TIME ALREADY EXISTS.
                if not self.model.get_time(self.clock_on_app.time_type, emp_id, self.model.get_current_date()):
                    self.model.set_time_record(self.clock_on_app.time_type, emp_id,
                                               self.model.get_current_date(), self.model.get_current_time())
                else:
                    raise excep.AlreadyClockedOff
                self.show_clock_time('clock_off', emp_id, self.model.get_current_date())
            else:
                raise excep.NoEmployeeSelected
        except excep.NoEmployeeSelected:
            messagebox.showinfo('Attention', 'No employee is selected!')
            return 'break'
        except excep.AlreadyClockedOff:
            messagebox.showinfo('Attention', 'Employee has already clocked off!')
            return 'break'


    # EMPLOYEE LIST EVENT CALL FOR WHEN AN EMPLOYEE IS SELECTED FROM THE LIST
    def emp_select(self, event):
        self.clock_on_app.on_combo_select()
        self.update_clock_time()

    def update_clock_time(self):
        for time_type in ['clock_on', 'clock_off']:
            self.show_clock_time(time_type, self.model.get_id_by_name(self.clock_on_app.employee),
                                 self.model.get_current_date())

    # UPDATES THE CLOCK ON APP LABEL TO REFLECT THE EMPLOYEE TIME
    def show_clock_time(self, time_type, _id, _date):
        time_value = self.model.get_time(time_type, _id, _date)
        if time_value:
            if time_type == 'clock_on':
                self.clock_on_app.on_label['text'] = time_value
            elif time_type == 'clock_off':
                self.clock_on_app.off_label['text'] = time_value
        else:
            if time_type == 'clock_on':
                self.clock_on_app.on_label['text'] = 'None'
            elif time_type == 'clock_off':
                self.clock_on_app.off_label['text'] = 'None'


if __name__ == '__main__':
    c = Controller()
