import re
from concurrent.futures import ThreadPoolExecutor
from json import loads
from logging import getLogger

from requests import get

from travelscanner.crawlers.crawler import log_on_failure
from travelscanner.data.datasets import load_unscraped_hotels
from travelscanner.models.tripadvisor_rating import TripAdvisorRating


# Scraper for TripAdvisor hotel ratings
class Scraper:
    BASE_URL = "https://www.tripadvisor.com"
    REVIEW_REGEX = re.compile(r'"ratingValue":"(\d+\.\d)","reviewCount":"(\d+)"')
    DISTRIBUTION_REGEX = re.compile(r'<span class="fill" style="width:(\d+)%;">')
    BLACKLIST = ['vandreferie', 'rundrejse']

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

    @log_on_failure
    def add_rating(self, hotel, area, country):
        if self.cancel_tasks:
            return

        # Check if hotel name is blacklisted
        hotel = hotel.lower()
        for blacklisted in Scraper.BLACKLIST:
            if blacklisted in hotel:
                return

        url = self.get_hotel_url(f"{Scraper.normalize(hotel)} {Scraper.normalize(area)}")

        if url is not None:
            get_result = get(f"{Scraper.BASE_URL}{url}")

            if get_result.status_code == 200:
                review = Scraper.REVIEW_REGEX.search(get_result.text)
                ratings = Scraper.DISTRIBUTION_REGEX.findall(get_result.text)

                if review is None or ratings is None or not len(ratings) == 5:
                    return

                ratings = [float(rating) / 100 for rating in ratings]

                if review is not None and ratings is not None and len(ratings) == 5:
                    TripAdvisorRating.create(country=country, hotel=hotel, area=area, rating=float(review.group(1)),
                                             review_count=int(review.group(2)), excellent=ratings[0], good=ratings[1],
                                             average=ratings[2], poor=ratings[3], terrible=ratings[4]).save()

    def scrape(self, unscraped_hotels):
        self.cancel_tasks = False

        getLogger().info(f"Scraping {len(unscraped_hotels)} hotel reviews")

        # Distribute tasks to multiple workers
        with ThreadPoolExecutor(max_workers=20) as executor:
            for name, area, country in unscraped_hotels:
                executor.submit(self.add_rating, name, area, country)

        getLogger().info(f"Scraping finished")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape(load_unscraped_hotels())
