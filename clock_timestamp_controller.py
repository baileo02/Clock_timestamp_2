import clock_timestamp_model
from clock_timestamp_model import Model
import clock_timestamp_view
import tkinter as tk
from tkinter import ttk
from clock_on_page import ClockOn
from timesheet_page import TimeSheet
from alter_hour_page import AlterHour
import exception_utility as excep

class Controller:

    def __init__(self):
        # INITIALIZE TK INTERFACE
        self.root = tk.Tk()
        self.root.title('Time System')
        self.root.geometry('300x300')
        # INITIALIZE MODEL
        self.model = Model()
        self._cur_date = self.model.get_current_date()
        self._cur_time = self.model.get_current_time()
        # ADD NOTEBOOK WIDGET TO ROOT LAYER
        self.nb = tk.ttk.Notebook(self.root, width=300, height=300)
        self.nb.grid()

        # INITIALIZE CLOCK ON APP AND FRAME
        self.clock_on_frame = tk.Frame(self.nb)
        self.nb.add(self.clock_on_frame, text='Clock On')
        self.clock_on_app = ClockOn(self.clock_on_frame, 'Clock on working')

        # INITIALIZE TIME SHEET APP AND FRAME
        self.timesheet_app = tk.Frame(self.nb)
        self.nb.add(self.timesheet_app, text='Time Sheet')
        self.timesheet_app = TimeSheet(self.timesheet_app, 'Time sheet working')

        # INITIALIZE ALTER HOUR APP AND FRAME
        self.alter_hour_page = tk.Frame(self.nb)
        self.nb.add(self.alter_hour_page, text='Alter hours')
        self.alter_hour_page = AlterHour(self.alter_hour_page, 'Alter hours is working')

        # INITIALIZE BACKEND DATA, POPULATES EMP LISTS / TIMES
        self.init_data()

        # HANDLES AND REDIRECTS EVENTS FROM VIEW
        self.event_trigger()


        self.root.mainloop()

    def init_data(self):
        self.clock_on_app.populate_emp_list(self.model.get_all_emp())

    # BUNDLE OF EVENT TRIGGERS FROM THE DIFFERENT APP VIEWS.
    def event_trigger(self):
        self.clock_on_app.combobox.bind("<<ComboboxSelected>>", self.emp_select)
        self.clock_on_app.on_button.bind("<Button-1>", self.clock_on)
        self.clock_on_app.off_button.bind("<Button-1>", self.clock_off)

    # CLOCK ON AND OFF BUTTON EVENT CALLS
    def clock_on(self, event):
        try:
            if self.clock_on_app.employee:
                self.clock_on_app.click_on()
                self.model.create_time_record(self.clock_on_app.time_type, self.model.get_id_by_name(self.clock_on_app.employee),
                                              self._cur_date, self._cur_time)
                self.show_clock_time('clock_on', self.model.get_id_by_name(self.clock_on_app.employee), self._cur_date)

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
                if not self.model.get_time(self.clock_on_app.time_type, emp_id, self._cur_date):
                    self.model.set_time_record(self.clock_on_app.time_type, emp_id,
                                               self._cur_date, self._cur_time)
                else:
                    raise excep.AlreadyClockedOff
                self.show_clock_time('clock_off', emp_id, self._cur_date)
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
            self.show_clock_time(time_type, self.model.get_id_by_name(self.clock_on_app.employee), self._cur_date)

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
                self.clock_on_app.on_label['text'] = 'NOT CLOCKED ON'
            elif time_type == 'clock_off':
                self.clock_on_app.off_label['text'] = 'NOT CLOCKED OFF'


    # def record_clock_in(self):
    #     self.model.create_time_record(self.clock_on_app.time_type, 1, )
    #     print(f'Recording employee {self.view.button_clicked()} time')

    # # Employee Clocking in
    # def emp_clock_in(self, _id, _date):
    #     self.model.create_time_record('clock_on', _id, _date, self.model.get_current_time())
    #
    # # Adding new employee to the database
    # def add_new_emp(self, name):
    #     self.model.create_new_emp(name)
    #
    # # Show clock on/off times
    # def display_time(self, time_type, _id, _date):
    #     return self.model.get_time(time_type, _id, _date)
    #
    # # Calculate hours worked for given date and emp_id
    # def display_hours_worked(self, _id, _date):
    #     print(self.model.get_hours_worked(_id, _date))
    #
    # def display_all_emp(self):
    #     return self.model.get_all_emp()
    #
    # def total_hours_worked(self, _id, dates):
    #     return self.model.get_total_hours(_id, dates)
    #
    # def change_clock_time(self, time_type, _id, _date, time_value):
    #     self.model.set_time_record(time_type, _id, _date, time_value)

if __name__ == '__main__':

    c = Controller()
