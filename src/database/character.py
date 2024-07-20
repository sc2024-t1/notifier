from typing import Dict

from pymongo.database import Database

from src.database.mongo_object import MongoObject


class Character(MongoObject):
    collection_name = "characters"

    def __init__(
            self,
            database: Database,
            character_id: str,
            name: str,
            description: str,
            initial_prompt: str,
            notify_prompt: str,
            avatar_url: str,

            ask_habit_name: str,
            ask_habit_name_ack: str,
            ask_habit_time: str,
            wrong_time_format: str,
            add_habit_done: str,
            add_habit_upsert_success: str
    ):
        super().__init__(database)
        self.character_id: str = character_id
        self.name: str = name
        self.description: str = description
        self.initial_prompt: str = initial_prompt
        self.notify_prompt: str = notify_prompt
        self.avatar_url: str = avatar_url

        self.ask_habit_name: str = ask_habit_name
        self.ask_habit_name_ack: str = ask_habit_name_ack
        self.ask_habit_time: str = ask_habit_time
        self.wrong_time_format: str = wrong_time_format
        self.add_habit_done: str = add_habit_done
        self.add_habit_upsert_success: str = add_habit_upsert_success

    def unique_identifier(self) -> Dict:
        return {
            "character_id": self.character_id
        }

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "name": self.name,
            "description": self.description,
            "initial_prompt": self.initial_prompt,
            "notify_prompt": self.notify_prompt,
            "avatar_url": self.avatar_url
        }
