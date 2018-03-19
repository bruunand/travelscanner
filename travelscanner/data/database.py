from peewee import *


class Database(object):
    instance = None

    def __init__(self, driver):
        self.driver = driver

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
