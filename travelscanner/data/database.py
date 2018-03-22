from logging import getLogger

from peewee import *


class Database(object):
    instance = None

    def __init__(self, driver):
        self.driver = driver
        self.cache = dict()
        self.has_initialized_cache = False

    @staticmethod
    def initialize_cache():
        if Database.get_instance().has_initialized_cache:
            return

        from travelscanner.models.travel import Travel
        from travelscanner.models.price import Price

        # Initialize cache
        getLogger().info("Initializing cache")

        for travel in Travel.select():
            Database.retrieve_from_cache(travel)

        for price in Price.select():
            Database.retrieve_from_cache(price)

        getLogger().info(f"Loaded {len(Database.get_instance().cache)} elements into cache")

        Database.get_instance().has_initialized_cache = True

    @staticmethod
    def save_travels(travels):
        getLogger().info(f"Saving {len(travels)} travels")

        with Database.get_driver().atomic():
            for i, travel in enumerate(travels):
                travel.upsert()

                if i % 100 == 0 or i + 1 == len(travels):
                    getLogger().info(f"{(i+1) / len(travels) * 100}% saved")

        getLogger().info(f"Saving complete")

    @staticmethod
    def retrieve_from_cache(obj):
        cache = Database.get_instance().cache

        ret_val = cache.get(hash(obj), None)
        if ret_val is None:
            cache[hash(obj)] = obj

        return ret_val

    @staticmethod
    def get_instance():
        if Database.instance is None:
            Database.instance = Database(MySQLDatabase('travelscanner', user='root', password=''))

        return Database.instance

    @staticmethod
    def get_driver():
        return Database.get_instance().driver

    @staticmethod
    def connect():
        return Database.get_driver().connect()

    @staticmethod
    def close():
        return Database.get_driver().close()
