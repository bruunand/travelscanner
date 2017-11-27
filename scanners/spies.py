from scanner import Scanner, log_on_failure
from travel_options import Airports


class SpiesScanner(Scanner):
    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: "503274", Airports.BILLUND: "499708",
                                   Airports.COPENHAGEN: "500055"}

    @log_on_failure
    def scan(self):
        pass