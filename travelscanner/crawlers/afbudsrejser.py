from travelscanner.crawlers.crawler import log_on_failure, Crawler, Crawlers


class Afbudsrejser(Crawler):
    def get_id(self):
        return Crawlers.AFBUDSREJSER

    @log_on_failure
    def crawl(self):
        pass
