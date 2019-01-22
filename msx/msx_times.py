import csv
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

from genders import Genders
from levels import Levels
from courses import Courses
from disciplines import Disciplines
from time_standard import TimeStandard
from meet import Meet
from import_msx_from_csv import import_msx_from_csv
from result import Result
from time_string import convert_time, display_time
from results_portal_scrape import ResultsPortalScrape
from qualifying_result import QualifyingResult


class MsxTimes:

    def __init__(self):

        self.time_standards = []
        self.bronze_results = []
        self.silver_results = []
        self.gold_results = []
        self.platinum_results = []

        self.qualifications = None

    def set_time_standards(self, time_standards):

        self.time_standards = self.time_standards + time_standards

    # TODO optimise
    def get_time_standard(self, distance, discipline, course, gender, age_minimum, age_maximum):

        for time_std in self.time_standards:
            if time_std.distance == distance:
                if time_std.discipline == discipline:
                    if time_std.course == course:
                        if time_std.gender == gender:
                            if time_std.age_minimum == age_minimum and time_std.age_maximum == age_maximum:
                                return time_std

        return None

    def check_results(self, event, results):

        for result in results:

            time_std = self.get_time_standard(result.distance, result.discipline, result.course,
                                              result.gender, result.age_min, result.age_max)

            #print("Bronze time: %s >= Final time: %s" % (time_std.bronze, result.final_time))

            if time_std is not None:

                # Compare result to time standard
                if time_std.get_bronze() >= result.get_final_time():
                    # print("%s %s %s %s Bronze time: %s >= Final time: %s" % (time_std.gender, result.age,
                    #                                                          time_std.distance, time_std.discipline,
                    #                                                          display_time(time_std.bronze / 100),
                    #                                                          display_time(result.final_time / 100)))
                    qr = QualifyingResult(event.event_id, event.meet_name, result, Levels.BRONZE)
                    self.bronze_results.append(qr)

                if time_std.get_silver() >= result.get_final_time():
                    # print("%s %s Silver time: %s >= Final time: %s" % (time_std.distance, time_std.discipline, time_std.silver, result.final_time))
                    qr = QualifyingResult(event.event_id, event.meet_name, result, Levels.SILVER)
                    self.silver_results.append(qr)

                if time_std.get_gold() >= result.get_final_time():
                    # print("%s %s Gold time: %s >= Final time: %s" % (time_std.distance, time_std.discipline, time_std.gold, result.final_time))
                    qr = QualifyingResult(event.event_id, event.meet_name, result, Levels.GOLD)
                    self.gold_results.append(qr)

                if time_std.get_platinum() >= result.get_final_time():
                    # print("%s %s Platinum time: %s >= Final time: %s" % (time_std.distance, time_std.discipline, time_std.platinum, result.final_time))
                    qr = QualifyingResult(event.event_id, event.meet_name, result, Levels.PLATINUM)
                    self.platinum_results.append(qr)

    def calculate_levels(self):

        qr_data = []

        for qr in self.bronze_results:
            qr_data.append(qr.to_dict())
        for qr in self.silver_results:
            qr_data.append(qr.to_dict())
        for qr in self.gold_results:
            qr_data.append(qr.to_dict())
        for qr in self.platinum_results:
            qr_data.append(qr.to_dict())

        qr_df = pd.DataFrame(qr_data)

        self.qualifications = qr_df[['swimmer_name', 'msa_id', 'level_name']].groupby(['swimmer_name', 'msa_id', 'level_name']).size()


if __name__ == "__main__":

    msx = MsxTimes()
    msx.set_time_standards(import_msx_from_csv('MSX2016 Qualifying Standard Times Male.csv'))
    msx.set_time_standards(import_msx_from_csv('MSX2016 Qualifying Standard Times Female.csv'))

    # time_std = msx.get_time_standard(200, Disciplines.FREESTYLE, Courses.SC, Genders.MALE, 60, 64)
    #
    # if time_std is not None:
    #
    #     print(time_std.get_bronze())

    rp = ResultsPortalScrape()

    print("Loaded %s MSX Time Standards" % len(msx.time_standards))

    events = rp.get_events(2018, "QLD")

    i = 0

    for event in events:

        # Temp only look at one event
        # if i > 0:
        #     break

        print("Retrieving results for %s..." % event.meet_name)
        results = rp.get_event_results(event)
        print("Processing results for %s..." % event.meet_name)
        msx.check_results(event, results)

        i += 1

    print("Total Qualifying Times:")
    print("Bronze: %s" % len(msx.bronze_results))
    print("Silver: %s" % len(msx.silver_results))
    print("Gold: %s" % len(msx.gold_results))
    print("Platinum: %s" % len(msx.platinum_results))

    msx.calculate_levels()

    if msx.qualifications is not None:

        print(msx.qualifications)
        msx.qualifications.to_csv('2018.csv')
