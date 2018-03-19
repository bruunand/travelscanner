class DateExceededException(Exception):
    def __init__(self, delta_time):
        self.delta_time = delta_time

    def __str__(self):
        return f"Departure date exceeded by {self.delta_time.days} days."


class NoCrawlersException(Exception):
    pass


class OptionContradictionException(Exception):
    def __init__(self, message):
        self.message = message
