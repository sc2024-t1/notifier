from typing import Dict

from pymongo.database import Database

from src.models.mongo_object import MongoObject
from src.ui.weekday_picker import Weekdays


class Habit(MongoObject):
    collection_name = "habits"

    def __init__(
            self,
            database: Database,
            title: str,
            habit_id: str,
            weekdays: int,
            times: list[str]
    ):
        super().__init__(database)

        self.habit_id: str = habit_id
        self.title: str = title
        self.weekdays: weekdays = Weekdays(weekdays)
        self.times: list[str] = times

    def unique_identifier(self) -> Dict:
        return {
            "habit_id": self.habit_id
        }

    def to_dict(self) -> Dict:
        return {
            "habit_id": self.habit_id,
            "title": self.title,
            "weekdays": self.weekdays.flags,
            "times": self.times
        }
