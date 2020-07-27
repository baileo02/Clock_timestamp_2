import tkinter as tk
from tkinter import ttk
from generic_templates import FrameTemplate

class ClockOn(FrameTemplate):

    def __init__(self, parent_frame, text, time_type=None, employee=None, time_value=None):
        super().__init__(parent_frame, text)
        # PARENT IS CLOCK ON FRAME > NOTEBOOK > ROOT
        self.parent_frame = parent_frame

        # PROPERTY VARIABLES FOR MODEL GET AND SET
        self.time_type = time_type
        self.employee = employee
        self.time_value = time_value

        # INITIALIZE COMBOBOX
        self.combobox = ttk.Combobox(self.parent_frame, state='readonly')
        self.combobox.grid()

        # INITIALIZE BUTTONS
        self.on_button = tk.Button(self.parent_frame, text='CLOCK ON')
        self.off_button = tk.Button(self.parent_frame, text='CLOCK OFF')
        self.on_button.grid(sticky='ew')
        self.off_button.grid(sticky='ew')

        # INITIALIZE LABELS
        self.on_label = tk.Label(self.parent_frame)
        self.off_label = tk.Label(self.parent_frame)
        self.on_label.grid(row=2, column=1)
        self.off_label.grid(row=3, column=1)

    def populate_emp_list(self, emp_list):
        self.combobox['values'] = emp_list

    @property
    def time_type(self):
        print('getting time type')
        return self._time_type

    @time_type.setter
    def time_type(self, value):
        print('setting time type value')
        self._time_type = value

    @property
    def employee(self):
        print('getting employee')
        return self._employee

    @employee.setter
    def employee(self, value):
        print('setting employee')
        self._employee = value

    @property
    def time_value(self):
        print('getting time value')
        return self._time_value

    @time_value.setter
    def time_value(self, value):
        print('setting time value')
        self._time_value = value

    def on_combo_select(self):
        self.employee = self.combobox.get()
        print(self.employee)

    def click_on(self):
        print('on clicked')
        self.time_type = 'clock_on'

    def click_off(self):
        print('off clicked')
        self.time_type = 'clock_off'



