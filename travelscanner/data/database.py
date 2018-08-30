import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import peewee


class Database(object):
    instance = None

    def __init__(self, driver):
        self.driver = driver
        self.cache = dict()
        self.has_initialized_cache = False
        self.save_pool = ThreadPoolExecutor(1)

    @staticmethod
    def save_travels(travels):
        logging.getLogger().info(f"Saving {len(travels)} travels")

        saved_sum = 0
        with Database.get_driver().atomic():
            for i, travel in enumerate(travels):
                saved_sum = saved_sum + travel.upsert()

        logging.getLogger().info(f"Saving complete, {saved_sum} new entities")

    @staticmethod
    def get_instance():
        if Database.instance is None:
            Database.instance = Database(peewee.MySQLDatabase('travelscanner', user='travelscanner', password='travelscanner'))

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
