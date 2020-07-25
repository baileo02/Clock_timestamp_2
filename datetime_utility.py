from datetime import datetime


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
def convert_min_overflow(hour_min_list: list):
    hour_min_list[0] += (hour_min_list[1] // 60)
    hour_min_list[1] = (hour_min_list[1] % 60)
    return hour_min_list

