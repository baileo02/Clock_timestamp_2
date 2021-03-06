# Model should be the only place that has access to the database.
# Does NOT communicate with the view, the controller does that
# Thus the code should be mainly producing outputs to specific database items.

from database_connection import Database
from datetime_utility import TimeCalculation, convert_min_overflow
from datetime import datetime
import exception_utility as excep


class Model:

    def __init__(self):
        self.db = Database('timesheet.db')

    @staticmethod
    def get_current_date():
        return datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def get_current_time():
        return datetime.today().strftime('%H:%M')


    def get_name_by_id(self, _id):
        return self.db.get_name_by_id(_id)

    def get_id_by_name(self, _name):
        return self.db.get_id_by_name(_name)

    def get_time(self, time_type, _id, _date):
        return self.db.get_time(time_type, _id, _date)

    def get_latest_emp_clock(self, _id):
        return self.db.get_last_clock_in_date(_id)

    def get_num_of_emp(self):
        return self.db.get_num_of_emp()

    def get_all_emp(self):
        return self.db.get_all_emp()

    def get_num_days_worked(self, dates, _id):
        days_worked = 0
        for date in dates:
            if self.get_hours_worked(_id, date):
                days_worked += 1
        return days_worked

    def get_hours_worked(self, _id, _date:str):
        clock_off_time = TimeCalculation(self.db.get_time('clock_off', _id, _date))
        clock_on_time = TimeCalculation(self.db.get_time('clock_on', _id, _date))
        # print(clock_on_time.time)
        # print(type(clock_on_time.time))
        try:
            if clock_on_time.time and clock_off_time.time:
                time_worked = clock_off_time - clock_on_time
                return time_worked
            elif clock_on_time.time and not clock_off_time.time:
                raise excep.MissingClockOff
        except excep.MissingClockOff:
            return 'Amend'

    # GETS ID AND A LIST OF DATES AND RETURNS THE TOTAL HOURS, MIN
    # hours_worked input must be a tuple with two integers e.g. (6,30)
    def get_total_hours(self, _id, dates):
        total_hours = 0
        hours_list = []
        for date in dates:
            hours_worked = self.get_hours_worked(_id, date)
            if hours_worked and not isinstance(hours_worked, str):
                hours_list.append(self.get_hours_worked(_id, date))
                total_hours = [sum(sum_hours) for sum_hours in zip(*hours_list)]
        return convert_min_overflow(total_hours)

    def create_time_record(self, time_type, _id, _date, time_value):
        self.db.insert_time_record(time_type, _id, _date, time_value)

    def create_new_emp(self, _name):
        self.db.insert_new_employee(_name)

    def set_time_record(self, time_type, _id, _date, time_value):
        self.db.update_time_record(time_type, _id, _date, time_value)

