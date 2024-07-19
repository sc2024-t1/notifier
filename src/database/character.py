from typing import Dict

from pymongo.database import Database

from src.database.mongo_object import MongoObject


class Character(MongoObject):
    collection_name = "characters"

    def __init__(
            self,
            database: Database,
            character_id: str,
            initial_prompt: str,
            notify_prompt: str,
            avatar_url: str
    ):
        super().__init__(database)

        self.character_id: str = character_id
        self.initial_prompt: str = initial_prompt
        self.notify_prompt: str = notify_prompt
        self.avatar_url: str = avatar_url

    def unique_identifier(self) -> Dict:
        return {
            "character_id": self.character_id
        }

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "initial_prompt": self.initial_prompt,
            "notify_prompt": self.notify_prompt,
            "avatar_url": self.avatar_url
        }
