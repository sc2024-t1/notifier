from typing import Dict

from pymongo.database import Database

from src.database.character import Character
from src.database.mongo_object import MongoObject


class User(MongoObject):
    collection_name = "users"

    def __init__(
            self,
            database: Database,
            user_id: int,
            selected_character_id: str
    ):
        super().__init__(database)

        self.user_id: int = user_id
        self.selected_character_id: str = selected_character_id

    def unique_identifier(self) -> Dict:
        return {
            "user_id": self.user_id
        }

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "selected_character_id": self.selected_character_id
        }

    @property
    def selected_character(self):
        return Character.find_one(self.database, character_id=self.selected_character_id)
