import clock_timestamp_model
from clock_timestamp_model import Model
import clock_timestamp_view
from clock_timestamp_view import MainView
import tkinter as tk

class Controller:

    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = MainView(self.root)
        self.root.mainloop()

    # Employee Clocking in
    def emp_clock_in(self, _id, _date):
        self.model.create_time_record('clock_on', _id, _date, self.model.get_current_time())

    # Adding new employee to the database
    def add_new_emp(self, name):
        self.model.create_new_emp(name)

    # Show clock on/off times
    def display_time(self, time_type, _id, _date):
        return self.model.get_time(time_type, _id, _date)

    # Calculate hours worked for given date and emp_id
    def display_hours_worked(self, _id, _date):
        print(self.model.get_hours_worked(_id, _date))

    def display_all_emp(self):
        return self.model.get_all_emp()

    def total_hours_worked(self, _id, dates):
        return self.model.get_total_hours(_id, dates)

    def change_clock_time(self, time_type, _id, _date, time_value):
        self.model.set_time_record(time_type, _id, _date, time_value)

if __name__ == '__main__':

    c = Controller()

