from datetime import datetime
from datetime import timedelta


class TimeCalculation:
    """ Class for adding/subtracting time
        Input in string form
        Output when subtracting returns the time difference in (Hour, Minute) form as a list in string form
    """

    def __init__(self, time: str):
        self.time = time

    def __sub__(self, other):
        if self.time and other.time:
            calculated_time_seconds = (datetime.strptime(self.time, '%H:%M') -
                                       datetime.strptime(other.time, '%H:%M')).seconds
            minutes = (calculated_time_seconds // 60) % 60
            hours = calculated_time_seconds // 3600
            return int(hours), int(minutes)
        else:
            return None

# Converts minute overflow to hours
def convert_min_overflow(hour_min_list):
    if hour_min_list:
        hour_min_list[0] += (hour_min_list[1] // 60)
        hour_min_list[1] = (hour_min_list[1] % 60)
        return hour_min_list
    else:
        return None

def ex_break_time(total_hours, break_hours):
    if total_hours and break_hours:
        total_break_hours = total_hours[0] - break_hours[0]
        total_break_minutes = total_hours[1] - break_hours[1]
        print(total_break_hours, total_break_minutes)
        if total_break_hours > 0:
            return convert_min_overflow([total_break_hours, total_break_minutes])
        else:
            return None

# TAKES INITIAL DATE AND RETURNS A LIST OF DATES FROM THE INITIAL DAY
def week_dates(initial_date, days:int):
    """
    :param initial_date: The starting date in the list where the other dates are incremented from
    :param days: Number of days that will be appended to the list from the initial_date
    :return: A list of dates in string format as '%Y-%m-%d'
    """
    temp = datetime.strptime(initial_date, '%Y-%m-%d')
    temp_list = [temp]
    for i in range(days - 1):
        temp += timedelta(days=1)
        temp_list.append(temp)
    return [datetime.strftime(date, '%Y-%m-%d') for date in temp_list]

# TAKES INITIAL DATE AND RETURNS THE DATE OF A WEEK LATER
def week_date(initial_date, days:int):
    temp = datetime.strptime(initial_date, '%Y-%m-%d')
    temp += timedelta(days=days)
    return temp.strftime('%Y-%m-%d')


