from result import Result
from levels import Levels


class QualifyingResult(Result):

    def __init__(self, event_id, meet_name, result, level, meet_date=None):

        super().__init__(result.place,
                         result.swimmer_name,
                         result.age,
                         result.age_min,
                         result.age_max,
                         result.gender,
                         result.club_code,
                         result.distance,
                         result.discipline,
                         result.course,
                         result.msa_id,
                         result.final_time,
                         result.split,
                         result.points)

        self.event_id = event_id
        self.meet_name = meet_name
        self.meet_date = meet_date
        self.level = level

    def to_dict(self):

        if self.level == Levels.BRONZE:
            level_name = "Bronze"
        if self.level == Levels.SILVER:
            level_name = "Silver"
        if self.level == Levels.GOLD:
            level_name = "Gold"
        if self.level == Levels.PLATINUM:
            level_name = "Platinum"

        return {
            'event_id': self.event_id,
            'meet_name': self.meet_name,
            'meet_date': self.meet_date,
            'level': self.level,
            'level_name': level_name,
            'place': self.place,
            'swimmer_name': self.swimmer_name,
            'age': self.age,
            'age_min': self.age_min,
            'age_max': self.age_max,
            'gender': self.gender,
            'club_code': self.club_code,
            'distance': self.distance,
            'discipline': self.discipline,
            'course': self.course,
            'msa_id': self.msa_id,
            'final_time': self.final_time,
            'points': self.points
        }