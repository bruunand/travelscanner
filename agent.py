from datetime import timedelta
from time import sleep

from errors import NoScannersException
from model.travel_options import TravelOptions


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
            travels = []

            for scanner in self.scanners:
                travels.extend(scanner.scan())

            if self.scan_interval is None:
                break
            else:
                for travel in travels:
                    print(travel.get_hash())

                sleep(self.scan_interval.total_seconds())
