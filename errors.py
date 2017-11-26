class DateExceededException(Exception):
    def __init__(self, delta_time):
        self.delta_time = delta_time

    def __str__(self):
        return "Departure date exceeded by {0} days.".format(self.delta_time.days)


class NoScannersException(Exception):
    pass


class OptionContradictionException(Exception):
    def __init__(self, message):
        self.message = message
