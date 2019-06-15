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
    BaseUrl = "https://www.tripadvisor.com"
    ReviewRegex = re.compile(r'"ratingValue":"(\d+\.\d)","reviewCount":"(\d+)"')
    DistributionRegex = re.compile(r'<span class="hotels-review-list-parts-(.*?)" style="width:(\d+.\d+)%">')
    ClassRegex = re.compile(r'<span class="ui_star_rating star_(\d)0')
    Blacklist = ['krydstogt', 'rejse']

    def __init__(self):
        self.cancel_tasks = False

    @staticmethod
    def normalize(string):
        special_characters = [',', '-', '/', '(', ')']
        replace_keywords = ["lejligheder", "lejl."]

        for character in special_characters:
            if character in string:
                string = string.split(character)[0]

        string = string.lower()
        for keyword in replace_keywords:
            string = string.replace(keyword, "")

        return string.strip()

    def get_hotel_url(self, query):
        payload = {'action': 'API', 'types': 'hotel', 'urlList': 'true', 'name_depth': '3', 'scoreThreshold': '0.0',
                   'typeahead1_5': 'true', 'query': query}

        # Get from API
        get_result = get(f"{Scraper.BaseUrl}/TypeAheadJson", params=payload,
                         headers={'X-Requested-With': 'XMLHttpRequest'})
        if not get_result.status_code == 200:
            return None
        json = loads(get_result.text)

        for item in json['results']:
            if not item['type'] == 'HOTEL':
                continue

            return item['url']

        # print(f"No URL for {query} (returned: {get_result.text})")

        self.cancel_tasks = True

        return None

    @log_on_failure
    def add_rating(self, hotel, area, country):
        if self.cancel_tasks:
            return

        # Check if hotel name is blacklisted
        hotel = hotel.lower()
        for blacklisted in Scraper.Blacklist:
            if blacklisted in hotel:
                return

        url = self.get_hotel_url(f"{Scraper.normalize(hotel)} {Scraper.normalize(area)}")

        if url is not None:
            get_result = get(f"{Scraper.BaseUrl}{url}")

            if get_result.status_code == 200:
                rating = Scraper.ReviewRegex.search(get_result.text)
                user_ratings = Scraper.DistributionRegex.findall(get_result.text)
                official_class = Scraper.ClassRegex.search(get_result.text)

                if rating is None:
                    rating = -1
                    review_count = -1
                else:
                    review_count = int(rating.group(2))
                    rating = float(rating.group(1))

                if user_ratings is None:
                    user_ratings = [0 for _ in range(5)]
                else:
                    user_ratings = [float(rating[1]) / 100 for rating in user_ratings]

                if official_class is None:
                    official_class = -1
                else:
                    official_class = int(official_class.group(1))

                print(official_class)

                if rating is not None and user_ratings is not None and len(user_ratings) == 5:
                    TripAdvisorRating.create(country=country, hotel=hotel, area=area, rating=rating,
                                             review_count=review_count, excellent=user_ratings[0], good=user_ratings[1],
                                             average=user_ratings[2], poor=user_ratings[3], terrible=user_ratings[4],
                                             official_class=official_class).save()

    def scrape(self):
        self.cancel_tasks = False

        # Load unscraped hotels
        unscraped_hotels = load_unscraped_hotels()
        getLogger().info(f"Scraping {len(unscraped_hotels)} hotel reviews")

        # Distribute tasks to multiple workers
        with ThreadPoolExecutor(max_workers=25) as executor:
            for name, area, country in unscraped_hotels:
                executor.submit(self.add_rating, name, area, country)

        getLogger().info(f"Scraping finished")
