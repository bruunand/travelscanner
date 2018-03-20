from peewee import *


class Database(object):
    instance = None

    def __init__(self, driver):
        self.driver = driver
        self.cache = dict()

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
