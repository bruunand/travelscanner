from datetime import datetime
from enum import IntEnum

from logging import getLogger

from travelscanner.errors import DateExceededException


def parse(value, dictionary, default=None, strip=True):
    if strip:
        value = value.strip()
    ret_val = dictionary.get(value, default)

    if ret_val is default:
        getLogger().warning(f"Unable to parse {value}")

    return int(ret_val)


class Countries(IntEnum):
    UNKNOWN = 0
    CAPE_VERDE = 1
    CROATIA = 2
    CYPRUS = 3
    EGYPT = 4
    FRANCE = 5
    GREECE = 6
    ITALY = 7
    MALTA = 8
    PORTUGAL = 9
    SPAIN = 10
    THAILAND = 11
    UK = 12
    LATVIA = 13
    GERMANY = 14
    BELGIUM = 15
    TURKEY = 16
    POLAND = 17
    AUSTRIA = 18
    HUNGARY = 19
    CZECH_REPUBLIC = 20
    NETHERLANDS = 21
    USA = 22
    UAE = 23
    IRELAND = 24
    HONG_KONG = 25
    SWEDEN = 26
    MOROCCO = 27
    ISRAEL = 28
    MONTENEGRO = 29
    ICELAND = 30
    TANZANIA = 31
    INDONESIA = 32
    JAPAN = 33
    SRI_LANKA = 34
    DOMINICAN_REPUBLIC = 35
    MAURITIUS = 36
    MEXICO = 37
    MALDIVES = 38
    MALAYSIA = 39
    SEYCHELLES = 40
    BULGARIA = 41
    LITHUANIA = 42
    SINGAPORE = 43
    VIETNAM = 44
    CUBA = 45
    BARBADOS = 46
    BRAZIL = 47
    INDIA = 48
    ARUBA = 49
    TUNISIA = 50
    JORDAN = 51
    JAMAICA = 52
    NETHERLANDS_ANTILLES = 53

    @staticmethod
    def parse_da(name):
        return parse(name, {'Spanien': Countries.SPAIN,
                            'Grækenland': Countries.GREECE,
                            'Cypern': Countries.CYPRUS,
                            'Tyskland': Countries.GERMANY,
                            'Letland': Countries.LATVIA,
                            'Østrig': Countries.AUSTRIA,
                            'Polen': Countries.POLAND,
                            'Belgien': Countries.BELGIUM,
                            'Storbritannien': Countries.UK,
                            'Tyrkiet': Countries.TURKEY,
                            'Frankrig': Countries.FRANCE,
                            'Ungarn': Countries.HUNGARY,
                            'Egypten': Countries.EGYPT,
                            'Italien': Countries.ITALY,
                            'Tjekkiet': Countries.CZECH_REPUBLIC,
                            'Holland': Countries.NETHERLANDS,
                            'USA': Countries.USA,
                            'Malta': Countries.MALTA,
                            'Forenede Arabiske Emirater': Countries.UAE,
                            'Portugal': Countries.PORTUGAL,
                            'Irland': Countries.IRELAND,
                            'Hong Kong': Countries.HONG_KONG,
                            'Thailand': Countries.THAILAND,
                            'Sverige': Countries.SWEDEN,
                            'Marokko': Countries.MOROCCO,
                            'Israel': Countries.ISRAEL,
                            'Montenegro': Countries.MONTENEGRO,
                            'Island': Countries.ICELAND,
                            'Indonesien': Countries.INDONESIA,
                            'Japan': Countries.JAPAN,
                            'Malaysia': Countries.MALAYSIA,
                            'Den dominikanske republik': Countries.DOMINICAN_REPUBLIC,
                            'Tanzania': Countries.TANZANIA,
                            'Mauritius': Countries.MAURITIUS,
                            'Maldiverne': Countries.MALDIVES,
                            'Sri Lanka': Countries.SRI_LANKA,
                            'Mexico': Countries.MEXICO,
                            'Seychellerne': Countries.SEYCHELLES,
                            'Bulgarien': Countries.BULGARIA,
                            'Litauen': Countries.LITHUANIA,
                            'Kroatien': Countries.CROATIA,
                            'Vietnam': Countries.VIETNAM,
                            'Singapore': Countries.SINGAPORE,
                            'Cuba': Countries.CUBA,
                            'Barbados': Countries.BARBADOS,
                            'Brasilien': Countries.BRAZIL,
                            'Indien': Countries.INDIA,
                            'Aruba': Countries.ARUBA,
                            'Tunesien': Countries.TUNISIA,
                            'Kap Verde Øerne': Countries.CAPE_VERDE,
                            'Jordan': Countries.JORDAN,
                            'Jamaica': Countries.JAMAICA,
                            'Hollandske Antiller': Countries.NETHERLANDS_ANTILLES,
                            }, Countries.UNKNOWN)


class Airports(IntEnum):
    UNKNOWN = 0
    AALBORG = 1
    BILLUND = 2
    COPENHAGEN = 3

    @staticmethod
    def parse_da(name):
        return parse(name, {'København': Airports.COPENHAGEN,
                            'Aalborg': Airports.AALBORG,
                            'Billund': Airports.BILLUND
                            }, Airports.UNKNOWN)


class MealTypes(IntEnum):
    UNKNOWN = 0
    NONE = 1
    NOT_SPECIFIED = 2
    BREAKFAST = 3
    HALF_BOARD = 4
    FULL_BOARD = 5
    ALL_INCLUSIVE = 6

    @staticmethod
    def parse_da(name):
        return parse(name, {'Ikke angivet': MealTypes.NOT_SPECIFIED,
                            'Med morgenmad': MealTypes.BREAKFAST,
                            'Halvpension': MealTypes.HALF_BOARD,
                            'Uden pension': MealTypes.NONE,
                            'All Inclusive': MealTypes.ALL_INCLUSIVE,
                            'All Inclusive med drikkevarer': MealTypes.ALL_INCLUSIVE,
                            'Helpension': MealTypes.FULL_BOARD,
                            '': MealTypes.NONE}, MealTypes.UNKNOWN)


class RoomTypes(IntEnum):
    UNKNOWN = 0
    APARTMENT = 1
    DOUBLE_ROOM = 2
    ECONOMY = 3
    STANDARD_ROOM = 4
    FAMILY = 5
    TWO_PERSON_ROOM = 6
    PREMIUM = 7
    TENT = 8
    BUNGALOW = 9

    '''Not the prettiest approach to take here, but the names are not consistent in any way.'''
    @staticmethod
    def parse_da(name):
        name = name.lower()

        if 'dobbelt' in name or 'double' in name:
            return RoomTypes.DOUBLE_ROOM
        elif 'studio' in name or 'apart' in name or 'lejl' in name:
            return RoomTypes.APARTMENT
        elif 'std' in name or 'enkelt' in name or 'stand' in name:
            return RoomTypes.STANDARD_ROOM
        elif 'economy' in name:
            return RoomTypes.ECONOMY
        elif 'fam' in name:
            return RoomTypes.FAMILY
        elif '2' in name:
            return RoomTypes.TWO_PERSON_ROOM
        elif 'suite' in name or 'panoramic' in name or 'deluxe' in name or 'superior' in name or 'premium' in name:
            return RoomTypes.PREMIUM
        elif 'telt' in name:
            return RoomTypes.TENT
        elif 'bungalow' in name:
            return RoomTypes.BUNGALOW

        return RoomTypes.UNKNOWN


class Vendors(IntEnum):
    UNKNOWN = 0
    SPIES = 1
    BRAVO_TOURS = 2
    TRIPSAVE = 3
    TUI = 4
    SUN_TOURS = 5
    MIXX_TRAVEL = 6
    SUNWEB = 7
    BEACH_TOURS = 8
    DETUR = 9
    NAZAR = 10
    ELIZA_WAS_HERE = 11
    ATLANTIS_REJSER = 12
    AMISOL_TRAVEL = 13
    SUNCHARTER = 14
    AARHUS_CHARTER = 15
    BALKAN_HOLIDAYS = 16
    PRIMO_TOURS = 17
    FOLKEFERIE = 18
    TRIPX = 19
    TURISTREJSER = 20
    APOLLO = 21
    ALMENA_TRAVEL = 22

    @staticmethod
    def parse_da(name):
        return parse(name, {'Spies': Vendors.SPIES,
                            'Bravo Tours': Vendors.BRAVO_TOURS,
                            'TripSave': Vendors.TRIPSAVE,
                            'TUI': Vendors.TUI,
                            'Sun Tours': Vendors.SUN_TOURS,
                            'Mixx Travel': Vendors.MIXX_TRAVEL,
                            'Sunweb': Vendors.SUNWEB,
                            'Beach Tours A/S': Vendors.BEACH_TOURS,
                            'Detur': Vendors.DETUR,
                            'Nazar': Vendors.NAZAR,
                            'Eliza was here': Vendors.ELIZA_WAS_HERE,
                            'Atlantis Rejser': Vendors.ATLANTIS_REJSER,
                            'Amisol Travel': Vendors.AMISOL_TRAVEL,
                            'SunCharter': Vendors.SUNCHARTER,
                            'Aarhus Charter': Vendors.AARHUS_CHARTER,
                            'Balkan Holidays': Vendors.BALKAN_HOLIDAYS,
                            'Primo Tours': Vendors.PRIMO_TOURS,
                            'FolkeFerie.dk': Vendors.FOLKEFERIE,
                            'TripX': Vendors.TRIPX,
                            'Turistrejser': Vendors.TURISTREJSER,
                            'Apollo': Vendors.APOLLO,
                            'Almena Travel': Vendors.ALMENA_TRAVEL}, Vendors.UNKNOWN)


class TravelOptions(object):
    def __init__(self):
        # Price information
        self.min_price = None
        self.max_price = None

        # Country information
        self.destination_countries = None
        self.departure_airports = None

        # Date and duration information
        self.earliest_departure_date = datetime.today()
        self.maximum_days_from_departure = None
        self.duration_days = None

        # Hotel information
        self.minimum_hotel_stars = None
        self.minimum_tripadvisor_rating = None
        self.all_inclusive = False

        # Guest information
        self.number_of_guests = None

    def set_earliest_departure_date(self, date_string):
        self.earliest_departure_date = datetime.strptime(date_string, '%d/%m/%Y')
        delta_time = datetime.today() - self.earliest_departure_date

        if delta_time.days > 0:
            raise DateExceededException(delta_time)
