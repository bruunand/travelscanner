from logging import getLogger

from peewee import *


class Database(object):
    instance = None

    def __init__(self, driver):
        self.driver = driver
        self.cache = dict()
        self.has_initialized_cache = False

    @staticmethod
    def save_travels(travels):
        saved_sum = 0
        getLogger().info(f"Saving {len(travels)} travels")

        with Database.get_driver().atomic():
            for i, travel in enumerate(travels):
                saved_sum = saved_sum + travel.upsert()

                if i % 500 == 0 or i + 1 == len(travels):
                    getLogger().info(f"{(i+1) / len(travels) * 100}% saved")

        getLogger().info(f"Saving complete, {saved_sum} new entities")

    @staticmethod
    def get_instance():
        if Database.instance is None:
            Database.instance = Database(MySQLDatabase('travelscanner', user='root', password='planner'))

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
