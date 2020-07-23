import clock_timestamp_model
import clock_timestamp_view


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def display_emp_name_by_id(self, _id):
        self.view.show_emp_name(self.model.get_name_by_id(_id))

    def display_emp_id_by_name(self, _name):
        self.view.show_emp_id(self.model.get_id_by_name(_name))

    def display_time(self, time_type, _id, _name):
        self.view.show_time(self.model.get_time(time_type, _id, _name))

    def display_hours_worked(self, _id, _date):
        self.view.show_hours_worked(self.model.get_hours_worked(_id, _date))

    def create_time_record(self, time_type, _id, _date, time_value):
        self.model.create_time_record(time_type, _id, _date, time_value)

    def set_time_record(self, time_type, _id, _date, time_value):
        self.model.set_time_record(time_type, _id, _date, time_value)


if __name__ == '__main__':
    c = Controller(clock_timestamp_model.Model(), clock_timestamp_view.View())

    # c.create_time_record('clock_on', 1, '2020-07-23', '12:00')
    c.set_time_record('clock_off', 1, '2020-07-23', '15:00')
