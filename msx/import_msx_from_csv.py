import csv
import re
from genders import Genders
from levels import Levels
from courses import Courses
from disciplines import Disciplines
from time_standard import TimeStandard
from time_string import convert_time


def get_distance(event):
    m = re.search(r'\d+', event)
    return int(m.group(0))


def get_course(event):
    if "SC" in event:
        return Courses.SC

    if "LC" in event:
        return Courses.LC

    return None


def get_discipline(event):
    if "Freestyle" in event:
        return Disciplines.FREESTYLE

    if "Breaststroke" in event:
        return Disciplines.BREASTSTROKE

    if "Butterfly" in event:
        return Disciplines.BUTTERFLY

    if "Backstroke" in event:
        return Disciplines.BACKSTROKE

    if "Individual Medley" in event:
        return Disciplines.IM

    return None


def import_msx_from_csv(file_name):

    time_standards = []

    msx_age_headers = None
    msx_level_headers = None
    gender = None

    with open(file_name) as csvfile:

        std_reader = csv.reader(csvfile, delimiter=',')

        for row in std_reader:

            if not row[1]:
                continue

            # Grab and store the age group of the table
            if "Men" in row[1] or "Women" in row[1]:
                msx_age_headers = row

                if "Men" in row[1]:
                    gender = Genders.MALE

                if "Women" in row[1]:
                    gender = Genders.FEMALE

                # Fill in missing age headers
                for i in range(1, len(msx_age_headers)):
                    if not msx_age_headers[i]:
                        msx_age_headers[i] = msx_age_headers[i - 1]

                continue

            # Grab and store the level headers of the table
            if "Platinum" in row[1] or "Gold" in row[1] or "Silver" in row[1] \
                    or "Bronze" in row[1]:
                msx_level_headers = row
                continue

            if msx_age_headers is not None and msx_level_headers is not None:

                event = row[0]

                discipline = get_discipline(event)
                course = get_course(event)
                distance = get_distance(event)

                time_std_group = []

                for i in range(1, len(row)):

                    time_std_seconds = convert_time(row[i])

                    time_std_group.append(time_std_seconds)

                    age_minimum = msx_age_headers[i].split(' ')[1].split('-')[0]
                    age_maximum = msx_age_headers[i].split(' ')[1].split('-')[1]

                    #print("%s-%s %s %s" % (age_minimum, age_maximum, msx_level_headers[i], time_std_seconds))

                    if len(time_std_group) == 4:

                        #print(time_std_group)

                        ts = TimeStandard(discipline=discipline,
                                          distance=distance,
                                          course=course,
                                          age_minimum=age_minimum,
                                          age_maximum=age_maximum,
                                          gender=gender,
                                          bronze=time_std_group[3],
                                          silver=time_std_group[2],
                                          gold=time_std_group[1],
                                          platinum=time_std_group[0])

                        time_std_group = []

                        time_standards.append(ts)

    return time_standards
