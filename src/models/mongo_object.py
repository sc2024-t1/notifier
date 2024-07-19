from abc import ABC, abstractmethod
from logging import getLogger, Logger
from typing import Generic, TypeVar, Type, Optional, AsyncIterator, Dict

from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult

T = TypeVar("T", bound="MongoObject")


class MongoObject(ABC, Generic[T]):
    collection_name: str
    logger: Logger = getLogger("mongo")

    def __init__(self, database: Database):
        self.database: Database = database

    @abstractmethod
    def unique_identifier(self) -> Dict:
        """
        Returns a dictionary representing the unique identifier for the document.

        Must be implemented by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the document to be upserted.

        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def upsert(self) -> UpdateResult:
        """
        Updates or inserts a document in the collection.

        :return: The UpdateResult of the update operation.
        """
        self.logger.info(
            f"Upserting {self.__class__.collection_name} document: {self.to_dict()}"
        )

        data = self.to_dict()

        return self.database.get_collection(self.__class__.collection_name).update_one(
            self.unique_identifier(),
            {"$set": data},
            upsert=True
        )

    def delete(self) -> DeleteResult:
        """
        Deletes this document from the collection.

        :return: The DeleteResult of the delete operation.
        """
        self.logger.info(
            f"Deleting {self.__class__.collection_name} document: {self.unique_identifier()}"
        )

        return self.database.get_collection(self.__class__.collection_name).delete_one(
            self.unique_identifier()
        )

    @classmethod
    def find_one(cls: Type[T], database: Database, **kwargs) -> Optional[T]:
        """
        Find a document in the collection that matches the specified query.
        """
        cls.logger.info(f"Finding one {cls.collection_name} document: {kwargs}")

        document = database.get_collection(cls.collection_name).find_one(kwargs)

        if not document:
            return None

        # noinspection PyUnresolvedReferences
        del document["_id"]

        return cls(database=database, **document)

    @classmethod
    def find(cls: Type[T], database: Database, **kwargs) -> AsyncIterator[T]:
        """
        Find all documents in the collection that match the specified query.
        """
        cls.logger.info(f"Finding {cls.collection_name} documents: {kwargs}")

        cursor = database.get_collection(cls.collection_name).find(kwargs)

        for document in cursor:
            del document["_id"]

            yield cls(database=database, **document)
