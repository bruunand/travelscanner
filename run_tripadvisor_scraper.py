from time import sleep

from travelscanner.data.datasets import load_unscraped_hotels
from travelscanner.tripadvisor.scraper import Scraper

if __name__ == "__main__":
    while True:
        scraper = Scraper()
        scraper.scrape(load_unscraped_hotels())

        sleep(60)
