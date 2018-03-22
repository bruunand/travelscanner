from concurrent.futures import ThreadPoolExecutor

from logging import getLogger

from travelscanner.data.database import Database
from travelscanner.data.datasets import load_unscraped_hotels

from requests import get
from json import loads

from travelscanner.models.tripadvisor_rating import TripAdvisorRating

import re

BASE_URL = "https://www.tripadvisor.com"
compiled = re.compile(r'"ratingValue":"(\d+\.\d)","reviewCount":"(\d+)"')


def normalize_name(name):
    if '-' in name:
        name = name.split('-')[0]

    return name.lower().replace("lejligheder", "apartments").replace("hotel", "").strip()


def get_hotel_url(query):
    payload = {'action': 'API', 'types': 'hotel', 'urlList': 'true', 'name_depth': '3', 'scoreThreshold': '0.3',
               'typeahead1_5': 'true', 'query': query}

    # Get from API
    get_result = get(f"{BASE_URL}/TypeAheadJson", params=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
    if not get_result.status_code == 200:
        return None
    json = loads(get_result.text)

    for item in json['results']:
        if not item['type'] == 'HOTEL':
            continue

        return item['url']

    print(f"No URL for {query} (returned: {get_result.text})")

    return None


def get_rating(name, area):
    url = get_hotel_url(f"{normalize_name(name)} {area.lower().strip()}")

    if url is not None:
        get_result = get(f"{BASE_URL}{url}")

        if get_result.status_code == 200:
            match = compiled.search(get_result.text)

            if match is not None:
                return float(match.group(1)), int(match.group(2))

        print(f"Could not get rating from URL {url}")

    return None, None


def add_rating(name, area, country, destination_list):
    rating, review_count = get_rating(name, area)

    if rating is not None and review_count is not None:
        destination_list.append(TripAdvisorRating.create(country=country, hotel_name=name, area=area,
                                                         rating=rating, review_count=review_count))


if __name__ == "__main__":
    unscraped_hotels = load_unscraped_hotels()
    ratings = []

    getLogger().info(f"Scraping {len(unscraped_hotels)} hotel reviews")

    # Distribute tasks to multiple workers
    with ThreadPoolExecutor(max_workers=50) as executor:
        for name, area, country in unscraped_hotels:
            executor.submit(add_rating, name, area, country, ratings)

    getLogger().info(f"Scraping finished, saving {len(ratings)} ratings to database")

    # All retrieved, now save to database
    with Database.get_driver().atomic():
        for rating in ratings:
            rating.save()

    getLogger().info("Results saved")
