from levels import Levels
from math import floor


class TimeStandard:

    def __init__(self, discipline, distance, course, gender, age_minimum, age_maximum, bronze, silver, gold, platinum):

        self.discipline = discipline
        self.distance = distance
        self.course = course
        self.gender = gender
        self.age_minimum = int(age_minimum)
        self.age_maximum = int(age_maximum)
        self.bronze = self.truncate(bronze)
        self.silver = self.truncate(silver)
        self.gold = self.truncate(gold)
        self.platinum = self.truncate(platinum)

    def is_ready(self):

        if self.bronze is None:
            return False

        if self.silver is None:
            return False

        if self.gold is None:
            return False

        if self.platinum is None:
            return False

        return True

    # Floors seconds to two decimal places and represent internally in milliseconds
    def truncate(self, seconds):

        if seconds is None:
            return None

        seconds = int(floor(seconds * 100))
        return seconds

    def check_age(self, age):

        if self.age_maximum >= age >= self.age_minimum:
            return True
        else:
            return False

    def check_time(self, seconds):

        if not self.is_ready():
            return None

        seconds = self.truncate(seconds)

        # A time may qualify at more than one level, so prepare to return all qualified levels
        qualifications = []

        if seconds <= self.bronze:
            qualifications.append(Levels.BRONZE)

        if seconds <= self.silver:
            qualifications.append(Levels.SILVER)

        if seconds <= self.gold:
            qualifications.append(Levels.GOLD)

        if seconds <= self.platinum:
            qualifications.append(Levels.PLATINUM)

        return qualifications

    def get_bronze(self):
        return self.bronze / 100

    def get_silver(self):
        return self.silver / 100

    def get_gold(self):
        return self.gold / 100

    def get_platinum(self):
        return self.platinum / 100
