from scanners.scanner import log_on_failure, Scanner


class AfbudsrejserScanner(Scanner):
    def get_alias(self):
        return "Afbudsrejser"

    @log_on_failure
    def scan(self):
        pass
