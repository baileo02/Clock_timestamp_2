import clock_timestamp_model
from clock_timestamp_model import Model
import tkinter as tk
from tkinter import ttk, messagebox
from clock_on_page import ClockOn
from timesheet_page import TimeSheet
from alter_hour_page import AlterHour
import exception_utility as excep
from datetime_utility import week_dates
from generic_templates import MessageWindow



class Controller:

    def __init__(self):
        # INITIALIZE TK INTERFACE
        self.root = tk.Tk()
        self.root.title('Time System')
        self.root.geometry('300x300')
        # INITIALIZE MODEL
        self.model = Model()

        # ADD NOTEBOOK WIDGET TO ROOT LAYER
        self.nb = tk.ttk.Notebook(self.root)
        self.nb.grid()

        # INITIALIZE CLOCK ON APP AND FRAME
        self.clock_on_frame = tk.Frame(self.nb)
        self.nb.add(self.clock_on_frame, text='Clock On')
        self.clock_on_app = ClockOn(self.clock_on_frame, 'Clock on working')

        # INITIALIZE TIME SHEET APP AND FRAME
        self.timesheet_frame = tk.Frame(self.nb)
        self.nb.add(self.timesheet_frame, text='Time Sheet')
        self.timesheet_app = TimeSheet(self.timesheet_frame, 'Time sheet working')

        # INITIALIZE ALTER HOUR APP AND FRAME
        self.alter_hour_frame = tk.Frame(self.nb)
        self.nb.add(self.alter_hour_frame, text='Alter hours')
        self.alter_hour_app = AlterHour(self.alter_hour_frame, 'Alter hours is working')

        # INITIALIZE BACKEND DATA, POPULATES EMP LISTS / TIMES
        self.init_app()

        # HANDLES AND REDIRECTS EVENTS FROM VIEW
        self.event_trigger()

        self.root.mainloop()

    # todo tab change height/width not working
    def _on_tab_changed(self, event):
        # gets the widget clicked and configures the height and width.
        event.widget.update_idletasks()
        tab = event.widget.nametowidget(event.widget.select())
        event.widget.configure(height=tab.winfo_reqheight(), width=tab.winfo_reqwidth())

    def init_app(self):
        self.clock_on_app.populate_emp_list(self.model.get_all_emp())
        self.display_timesheet_grid(self.model.get_current_date(), 7)
        self.alter_hour_app.populate_emp_list(self.model.get_all_emp())

    # BUNDLE OF EVENT TRIGGERS FROM THE DIFFERENT APP VIEWS.
    def event_trigger(self):
        self.clock_on_app.combobox.bind("<<ComboboxSelected>>", self.emp_select)
        self.clock_on_app.on_button.bind("<Button-1>", self.clock_on)
        self.clock_on_app.off_button.bind("<Button-1>", self.clock_off)
        self.alter_hour_app.emp_combobox.bind("<<ComboboxSelected>>", self.alter_emp_select)
        self.alter_hour_app.calendar.bind("<<DateEntrySelected>>", self.alter_date_select)
        self.alter_hour_app.on_button.bind("<Button-1>", self.alter_on)
        self.alter_hour_app.off_button.bind("<Button-1>", self.alter_off)
        self.timesheet_app.calendar.bind("<<DateEntrySelected>>", self.date_select)
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    # EMPLOYEE LIST EVENT CALL FOR WHEN AN EMPLOYEE IS SELECTED FROM THE LIST
    def alter_emp_select(self, event):
        self.alter_hour_app.on_combo_select()
        self.update_show_time()

    def alter_date_select(self, event):
        self.alter_hour_app.on_date_select()
        for time_type in ['clock_on', 'clock_off']:
            self.show_time(time_type, self.model.get_id_by_name(self.alter_hour_app.employee),
                           self.alter_hour_app.date_value)

    def alter_on(self, event):
        self.alter_time('clock_on')

    def alter_off(self, event):
        self.alter_time('clock_off')

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

    def alter_time(self, time_type):
        emp_id = self.model.get_id_by_name(self.alter_hour_app.employee)
        clock_off_time = self.model.get_time('clock_off', emp_id, self.alter_hour_app.date_value)
        clock_on_time = self.model.get_time('clock_on', emp_id, self.alter_hour_app.date_value)
        print(clock_off_time)
        print(clock_on_time)
        try:
            if self.alter_hour_app.employee:
                if self.alter_hour_app.ask_password():
                    self.alter_hour_app.alter_time()
                    if self.alter_hour_app.time_value:
                        if clock_on_time or clock_off_time:
                            if time_type == 'clock_on':
                                if clock_off_time:
                                    if self.alter_hour_app.time_value <= clock_off_time:
                                        self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                                    else:
                                        raise excep.IllogicalTime
                                else:
                                    self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                            elif time_type == 'clock_off':
                                if clock_on_time:
                                    if clock_on_time <= self.alter_hour_app.time_value:
                                        self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                                    else:
                                        raise excep.IllogicalTime
                                else:
                                    self.model.set_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                        else:
                            self.model.create_time_record(time_type, emp_id, self.alter_hour_app.date_value, self.alter_hour_app.time_value)
                        self.update_show_time()
                elif self.alter_hour_app.user_input is None:
                    pass
                else:
                    raise excep.IncorrectPassword
            else:
                raise excep.NoEmployeeSelected
        except excep.IncorrectPassword:
            messagebox.showerror('Access denied', 'Incorrect password')
        except excep.IllogicalTime:
            messagebox.showerror('Time Error', 'Clock ON time must be less than Clock OFF time')

    # DATE SELECTOR FOR TIME SHEET APP EVENT CALL
    def date_select(self, event):
        self.timesheet_app.clear_grid()
        sel_date = event.widget.get()
        days = 7
        self.display_timesheet_grid(sel_date, days)

    def display_timesheet_grid(self, selected_date, days):
        for row, emp in enumerate(self.model.get_all_emp(), 1):
            dates = []
            self.timesheet_app.init_grid_frame(row, 0, emp)
            for column, date in enumerate(week_dates(selected_date, days)):
                self.timesheet_app.init_grid_frame(0, column + 1, date)
                self.timesheet_app.init_grid_frame(row, column + 1,
                                                   self.model.get_hours_worked(self.model.get_id_by_name(emp), date))
                dates.append(date)
            self.timesheet_app.init_grid_frame(0, days + 1, 'Total')
            self.timesheet_app.init_grid_frame(row, days + 1,
                                               self.model.get_total_hours(self.model.get_id_by_name(emp), dates))

    # CLOCK ON AND OFF BUTTON EVENT CALLS
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
            print('No employee is selected!')
            print()
        except excep.RecordAlreadyExists:
            print('This employee has already clocked on today!')
            print()

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
            print('No employee is selected!')
        except excep.AlreadyClockedOff:
            print('Employee has already clocked off!')

    # EMPLOYEE LIST EVENT CALL FOR WHEN AN EMPLOYEE IS SELECTED FROM THE LIST
    def emp_select(self, event):
        self.clock_on_app.on_combo_select()
        for time_type in ['clock_on', 'clock_off']:
            self.show_clock_time(time_type, self.model.get_id_by_name(self.clock_on_app.employee),
                                 self.model.get_current_date())

    # UPDATES THE CLOCK ON APP LABEL TO REFLECT THE EMPLOYEE TIME
    def show_clock_time(self, time_type, _id, _date):
        time_value = self.model.get_time(time_type, _id, _date)
        print(f'tiem value is {time_value}')
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
