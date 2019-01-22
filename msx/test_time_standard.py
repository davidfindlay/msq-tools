import pytest
from time_standard import TimeStandard
from disciplines import Disciplines
from courses import Courses
from levels import Levels
from genders import Genders


class TestTimeStandard(object):

    def test_ready(self):

        ts = TimeStandard(discipline=Disciplines.FREESTYLE,
                          distance=100,
                          course=Courses.LC,
                          age_minimum=25,
                          age_maximum=29,
                          gender=Genders.MALE,
                          bronze=45.23,
                          silver=40.10,
                          gold=38.99,
                          platinum=35)

        assert ts.is_ready() is True

        ts = TimeStandard(discipline=Disciplines.FREESTYLE,
                          distance=100,
                          course=Courses.LC,
                          age_minimum=25,
                          age_maximum=29,
                          gender=Genders.MALE,
                          bronze=45.23,
                          silver=40.10,
                          gold=None,
                          platinum=35)

        assert ts.is_ready() is False

    def test_truncate(self):

        ts = TimeStandard(discipline=Disciplines.FREESTYLE,
                          distance=100,
                          course=Courses.LC,
                          age_minimum=25,
                          age_maximum=29,
                          gender=Genders.MALE,
                          bronze=45.23,
                          silver=40.10,
                          gold=38.99,
                          platinum=35)

        assert ts.truncate(25.87659) == 2587
        assert ts.truncate(23) == 2300
        assert ts.truncate(1.1233) == 112

    def test_check_age(self):

        ts = TimeStandard(discipline=Disciplines.FREESTYLE,
                          distance=100,
                          course=Courses.LC,
                          age_minimum=35,
                          age_maximum=39,
                          gender=Genders.MALE,
                          bronze=45.23,
                          silver=40.10,
                          gold=38.99,
                          platinum=35)

        assert ts.check_age(34) is False
        assert ts.check_age(35) is True
        assert ts.check_age(37) is True
        assert ts.check_age(39) is True
        assert ts.check_age(40) is False
        assert ts.check_age(0) is False
        assert ts.check_age(-37) is False

    def test_check_time(self):

        ts = TimeStandard(discipline=Disciplines.FREESTYLE,
                          distance=100,
                          course=Courses.LC,
                          age_minimum=35,
                          age_maximum=39,
                          gender=Genders.MALE,
                          bronze=45.23,
                          silver=40.10,
                          gold=38.99,
                          platinum=35)

        # Should return No Qualification
        result = ts.check_time(seconds=45.24)

        assert Levels.BRONZE not in result
        assert Levels.SILVER not in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result
        assert len(result) == 0

        # Should return Bronze
        result = ts.check_time(seconds=45.2399)

        assert Levels.BRONZE in result
        assert Levels.SILVER not in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result

        # Should return Bronze
        result = ts.check_time(seconds=45.2299)

        assert Levels.BRONZE in result
        assert Levels.SILVER not in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result

        # Should return Bronze
        result = ts.check_time(seconds=40.11)

        assert Levels.BRONZE in result
        assert Levels.SILVER not in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result

        # Should return Bronze
        result = ts.check_time(seconds=40.1)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result

        # Should return Bronze
        result = ts.check_time(seconds=40.0999)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result

        # Should return Bronze, Silver and Gold
        result = ts.check_time(seconds=38.991)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD in result
        assert Levels.PLATINUM not in result

        # Should return Bronze and Silver
        result = ts.check_time(seconds=39.00)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD not in result
        assert Levels.PLATINUM not in result

        # Should return Bronze, Silver and Gold
        result = ts.check_time(seconds=35.01)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD in result
        assert Levels.PLATINUM not in result

        # Should return Bronze, Silver, Gold and Platinum
        result = ts.check_time(seconds=35.00)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD in result
        assert Levels.PLATINUM in result

        # Should return Bronze, Silver, Gold and Platinum
        result = ts.check_time(seconds=34.99)

        assert Levels.BRONZE in result
        assert Levels.SILVER in result
        assert Levels.GOLD in result
        assert Levels.PLATINUM in result
