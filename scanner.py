from abc import ABCMeta, abstractmethod
from travel_options import Airports, Countries


def validate_dictionary(source, needles, haystack):
    for item in needles:
        if not haystack.__contains__(item):
            print("{0} is not supported by {1}, will be skipped.".format(item, source.__class__.__name__))


def join_values(keys, dictionary, separator):
    values = []

    for key in keys:
        if dictionary.__contains__(key):
            values.append(dictionary[key])

    return separator.join(values)


def log_on_failure(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as exception:
            print("Error in {0}: {1}".format(func.__qualname__, exception))

    return wrapper


class Scanner(metaclass=ABCMeta):
    BaseHeaders = {"User-Agent": None}

    def __init__(self):
        self.agent = None

        # Dictionaries used to convert values by different platforms
        self.airport_dictionary = {}
        self.country_dictionary = {}

    @abstractmethod
    def scan(self):
        pass

    def set_agent(self, agent):
        self.agent = agent

        # Print items missing in own dictionaries
        # This is to inform the user of any desired options that cannot be fulfilled by certain scanners
        validate_dictionary(self, self.get_options().destination_countries, self.country_dictionary)
        validate_dictionary(self, self.get_options().departure_airports, self.airport_dictionary)

    def get_options(self):
        return self.agent.travel_options
