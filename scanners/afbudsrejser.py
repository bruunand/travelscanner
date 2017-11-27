from scanner import log_on_failure, Scanner


class AfbudsrejserScanner(Scanner):
    @log_on_failure
    def scan(self):
        pass