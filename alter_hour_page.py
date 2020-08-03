import tkinter as tk
from tkinter import ttk
from generic_templates import FrameTemplate
from tkSimpleDialog import Dialog
from tkinter import simpledialog
import tkcalendar
from tkinter import ttk, messagebox


class AlterDialog(Dialog):
    """
    Creates a dialog pop up that returns the selected 24 hour time in string format 'HR:MIN'
    E.g. '16:30'
    """

    def body(self, master):

        tk.Label(master, text="Hour:").grid(row=0)
        tk.Label(master, text="Minute:").grid(row=1)

        self.results = None
        # todo clicking cancel returns None by default
        # todo need to work around this.
        self.hour = ttk.Combobox(master, values=tuple(range(0, 24)), state='readonly')
        self.minute = ttk.Combobox(master, values=tuple(range(0, 60)), state='readonly')

        self.hour.grid(row=0, column=1)
        self.minute.grid(row=1, column=1)

    def apply(self):
        first = self.hour.get()
        second = self.minute.get()
        self.results = str(first).zfill(2) + ':' + str(second).zfill(2)

class AlterHour(FrameTemplate):

    def __init__(self, parent_frame, text, date_value=None, time_type=None, employee=None, time_value=None, user_input=None):
        super().__init__(parent_frame, text)

        # CHOSEN PASSWORD TO ACCESS ALTER CONTROLS
        self._password = 'bj'

        # INITIALIZE VARIABLES
        self.parent_frame = parent_frame
        self.time_type = time_type
        self.employee = employee
        self.user_input = user_input

        # INITIALIZE EMPLOYEE COMBOBOX
        self.emp_combobox = ttk.Combobox(self.parent_frame, state='readonly')
        self.emp_combobox.grid()

        # INITIALIZE DATE SELECT
        self.calendar = tkcalendar.DateEntry(self.parent_frame, date_pattern='y-mm-dd', state='readonly')
        self.calendar.grid(sticky='ew')
        self.date_value = self.calendar.get()

        # INITIALIZE BUTTONS THAT DISPLAY CLOCK ON AND OFF TIMES
        self.on_button = tk.Button(self.parent_frame, text='ON')
        self.off_button = tk.Button(self.parent_frame, text='OFF')
        self.on_button.grid(sticky='ew')
        self.off_button.grid(sticky='ew')

    def populate_emp_list(self, emp_list):
        self.emp_combobox['values'] = emp_list
        self.emp_combobox.set('Select Employee:')

    def ask_password(self):
        self.user_input = tk.simpledialog.askstring('Password', 'Access password', parent=self.parent_frame)
        if self.user_input == self._password:
            return True
        elif not self.user_input:
            print('Cancelled')
        else:
            return False

    def alter_time(self):
        altered_time = AlterDialog(self.parent_frame)
        self.time_value = altered_time.results

    @property
    def time_type(self):
        return self._time_type

    @time_type.setter
    def time_type(self, value):
        self._time_type = value

    @property
    def date_value(self):
        return self._date_value

    @date_value.setter
    def date_value(self, value):
        self._date_value = value

    @property
    def employee(self):
        return self._employee

    @employee.setter
    def employee(self, value):
        self._employee = value

    @property
    def time_value(self):
        return self._time_value

    @time_value.setter
    def time_value(self, value):
        self._time_value = value

    def on_combo_select(self):
        self.employee = self.emp_combobox.get()
        print(self.employee)

    def on_date_select(self):
        self.date_value = self.calendar.get()
        print(self.date_value)
