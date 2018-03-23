import re
from concurrent.futures import ThreadPoolExecutor
from json import loads
from logging import getLogger

from requests import get

from travelscanner.data.datasets import load_unscraped_hotels
from travelscanner.models.tripadvisor_rating import TripAdvisorRating


# Scraper for TripAdvisor hotel ratings
class Scraper:
    BASE_URL = "https://www.tripadvisor.com"
    COMPILED = re.compile(r'"ratingValue":"(\d+\.\d)","reviewCount":"(\d+)"')

    def __init__(self):
        self.cancel_tasks = False

    @staticmethod
    def normalize(string):
        special_characters = [',', '-', '/']

        for character in special_characters:
            if character in string:
                string = string.split(character)[0]

        return string.lower().replace("lejligheder", "apartments").replace("hotel", "").strip()

    def get_hotel_url(self, query):
        payload = {'action': 'API', 'types': 'hotel', 'urlList': 'true', 'name_depth': '3', 'scoreThreshold': '0.0',
                   'typeahead1_5': 'true', 'query': query}

        # Get from API
        get_result = get(f"{Scraper.BASE_URL}/TypeAheadJson", params=payload,
                         headers={'X-Requested-With': 'XMLHttpRequest'})
        if not get_result.status_code == 200:
            return None
        json = loads(get_result.text)

        for item in json['results']:
            if not item['type'] == 'HOTEL':
                continue

            return item['url']

        print(f"No URL for {query} (returned: {get_result.text})")

        self.cancel_tasks = True

        return None

    def get_rating(self, name, area):
        if self.cancel_tasks:
            return None, None

        url = self.get_hotel_url(f"{Scraper.normalize(name)} {Scraper.normalize(area)}")

        if url is not None:
            get_result = get(f"{Scraper.BASE_URL}{url}")

            if get_result.status_code == 200:
                match = Scraper.COMPILED.search(get_result.text)

                if match is not None:
                    return float(match.group(1)), int(match.group(2))
                else:
                    return 3.0, 0

            print(f"Could not get rating from URL {url}")

        return None, None

    def add_rating(self, name, area, country):
        rating, review_count = self.get_rating(name, area)

        if rating is not None and review_count is not None:
            TripAdvisorRating.create(country=country, hotel=name, area=area,
                                     rating=rating, review_count=review_count).save()

    def scrape(self, unscraped_hotels):
        self.cancel_tasks = False

        getLogger().info(f"Scraping {len(unscraped_hotels)} hotel reviews")

        # Distribute tasks to multiple workers
        with ThreadPoolExecutor(max_workers=3) as executor:
            for name, area, country in unscraped_hotels:
                executor.submit(self.add_rating, name, area, country)

        getLogger().info(f"Scraping finished")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape(load_unscraped_hotels())
