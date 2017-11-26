from travel_options import TravelOptions
from datetime import timedelta
from time import sleep
from errors import NoScannersException


class Agent(object):
    def __init__(self):
        self.scanners = []
        self.travel_options = TravelOptions()
        self.scan_interval = timedelta(minutes=5)

    def get_travel_options(self):
        return self.travel_options

    def add_scanner(self, scanner):
        scanner.set_agent(self)
        self.scanners.append(scanner)

    def set_scanning_interval(self, scan_interval):
        self.scan_interval = scan_interval

    def scan_loop(self):
        if len(self.scanners) == 0:
            raise NoScannersException()

        while True:
            [scanner.scan() for scanner in self.scanners]

            if self.scan_interval is None:
                break
            else:
                sleep(self.scan_interval.total_seconds())
