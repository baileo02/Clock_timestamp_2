
class RecordAlreadyExists(Exception):
    pass

class RecordNotFound(Exception):
    pass

class NoEmployeeSelected(Exception):
    pass

class AlreadyClockedOff(Exception):
    pass

class RecordNotComplete(Exception):
    """
    Missing clock On or Off times
    """
    pass

class MissingClockOff(Exception):
    """
    Clock on recorded, but no clock off time
    """
    pass