from os import getenv

from pymongo import MongoClient
from pymongo.database import Database
from telebot import TeleBot

from src.gemini.conversations import ConversationManager


class Notifier(TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.database: Database = MongoClient(getenv("MONGO_URI")).get_database("notifier")
        self.conversation_manager: ConversationManager = ConversationManager(self.database)
