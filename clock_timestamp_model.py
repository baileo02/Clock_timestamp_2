# Model should be the only place that has access to the database.
# Does NOT communicate with the view, the controller does that
# Thus the code should be mainly producing outputs to specific database items.

from database_connection import Database
from datetime_utility import TimeCalculation


class Model:

    def __init__(self):
        self.db = Database('timesheet.db')

    def get_name_by_id(self, _id):
        return self.db.get_name_by_id(_id)

    def get_id_by_name(self, _name):
        return self.db.get_id_by_name(_name)

    def get_time(self, time_type, _id, _date):
        return self.db.get_time(time_type, _id, _date)

    def get_hours_worked(self, _id, _date):
        clock_off_time = TimeCalculation(self.db.get_time('clock_off', _id, _date))
        clock_on_time = TimeCalculation(self.db.get_time('clock_on', _id, _date))
        time_worked = clock_off_time - clock_on_time
        return time_worked

    def create_time_record(self, time_type, _id, _date, time_value):
        self.db.insert_time_record(time_type, _id, _date, time_value)

    def set_time_record(self, time_type, _id, _date, time_value):
        self.db.update_time_record(time_type, _id, _date, time_value)
