from pymongo.database import Database

from src.models.mongo_object import MongoObject


class Performance(MongoObject):
    collection_name = "performances"

    def __init__(self, database: Database, performance_id: str, user_id: int, succeeded: bool):
        super().__init__(database)

        self.performance_id: str = performance_id
        self.user_id: int = user_id
        self.succeeded: bool = succeeded

    def unique_identifier(self):
        return {
            "performance_id": self.performance_id
        }

    def to_dict(self):
        return {
            "performance_id": self.performance_id,
            "user_id": self.user_id,
            "succeeded": self.succeeded
        }
