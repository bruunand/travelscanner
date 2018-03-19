from abc import ABCMeta, abstractmethod
from enum import IntEnum
from logging import getLogger


def get_default_if_none(value, default):
    """Returns the specified value unless it is none, in which case the specified default will be returned."""
    return default if value is None else value


def validate_dictionary(source, needles, haystack):
    """Used to validate whether requested entities (airports or countries) are supported by a certain scanner."""
    if needles is None:
        return

    for item in needles:
        if not haystack.__contains__(item):
            getLogger().warning(f"Skipping {item}, not supported by {source.__class__.__name__}")


def join_values(keys, dictionary, separator):
    """Joins a list of entities (airports or countries) as long as they are contained in the scanner's dictionary."""
    values = []

    for key in keys:
        if dictionary.__contains__(key):
            values.append(dictionary[key])

    return separator.join(values)


def log_on_failure(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exception:
            getLogger().warning(f"Error in {func.__qualname__}: {exception}")

    return wrapper


class Crawlers(IntEnum):
    TRAVELMARKET = 0,
    SPIES = 1,
    AFBUDSREJSER = 2


class Crawler(metaclass=ABCMeta):
    BaseHeaders = {"User-Agent": None}

    def __init__(self):
        self.agent = None

        # Dictionaries used to convert values by different platforms
        self.airport_dictionary = {}
        self.country_dictionary = {}

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def crawl(self):
        pass

    def set_agent(self, agent):
        self.agent = agent

        # Print items missing in own dictionaries
        # This is to inform the user of any desired options that cannot be fulfilled by certain crawlers
        validate_dictionary(self, self.get_options().destination_countries, self.country_dictionary)
        validate_dictionary(self, self.get_options().departure_airports, self.airport_dictionary)

    def get_options(self):
        return self.agent.travel_options
