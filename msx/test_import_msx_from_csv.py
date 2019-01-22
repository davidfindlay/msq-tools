import pytest

from courses import Courses
from disciplines import Disciplines
from genders import Genders

from import_msx_from_csv import convert_time, get_distance, get_course, get_discipline, import_msx_from_csv


def test_convert_time():

    assert convert_time("25.32") == 25.32
    assert convert_time("1:29.01") == 89.01
    assert convert_time("30:00.00") == 1800


def test_get_distance():

    assert get_distance("Freestyle 100m SC") == 100
    assert get_distance("Individual Medley 400m LC") == 400
    assert get_distance("Backstroke 50m SC") == 50
    assert get_distance("Breaststroke 200m SC") == 200
    assert get_distance("Freestyle 1500m SC") == 1500


def test_get_course():

    assert get_course("Freestyle 100m SC") == Courses.SC
    assert get_course("Freestyle 100m LC") == Courses.LC


def test_get_discipline():

    assert get_discipline("Freestyle 100m SC") == Disciplines.FREESTYLE
    assert get_discipline("Individual Medley 400m LC") == Disciplines.IM
    assert get_discipline("Backstroke 50m SC") == Disciplines.BACKSTROKE
    assert get_discipline("Butterfly 50m SC") == Disciplines.BUTTERFLY
    assert get_discipline("Breaststroke 200m LC") == Disciplines.BREASTSTROKE

def test_import():

    data = import_msx_from_csv('MSX2016 Qualifying Standard Times Male.csv')

    time_standards_found = 0

    if data is not None:

        for time_standard in data:

            if time_standard.distance == 200:
                if time_standard.discipline == Disciplines.FREESTYLE:
                    if time_standard.course == Courses.LC:

                            if time_standard.age_minimum == 60 and time_standard.age_maximum == 64:

                                assert time_standard.bronze == 18616
                                assert time_standard.silver == 17890
                                assert time_standard.gold == 17200
                                assert time_standard.platinum == 16307

                                time_standards_found += 4

            if time_standard.distance == 1500:
                if time_standard.discipline == Disciplines.FREESTYLE:
                    if time_standard.course == Courses.SC:

                            if time_standard.age_minimum == 18 and time_standard.age_maximum == 24:

                                assert time_standard.bronze == 140127
                                assert time_standard.silver == 129250
                                assert time_standard.gold == 107656
                                assert time_standard.platinum == 102506

                                time_standards_found += 4

            if time_standard.distance == 50:
                if time_standard.discipline == Disciplines.BUTTERFLY:
                    if time_standard.course == Courses.SC:

                            if time_standard.age_minimum == 100 and time_standard.age_maximum == 104:

                                assert time_standard.bronze == 61875
                                assert time_standard.silver == 59946
                                assert time_standard.gold == 59010
                                assert time_standard.platinum == 51500

                                time_standards_found += 4

    assert time_standards_found == 12

