from typing import Dict

from pymongo.database import Database

from src.models.mongo_object import MongoObject


class Character(MongoObject):
    def __init__(
            self,
            database: Database,
            character_id: str,
            prompt: str
    ):
        super().__init__(database)

        self.character_id: str = character_id
        self.prompt: str = prompt

    def unique_identifier(self) -> Dict:
        return {
            "character_id": self.character_id
        }

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "prompt": self.prompt
        }
