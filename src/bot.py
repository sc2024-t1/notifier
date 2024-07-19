from os import getenv

from pymongo import MongoClient
from telebot import TeleBot

from src.gemini.conversations import ConversationManager


class Notifier(TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.database = MongoClient(getenv("MONGO_URI")).get_database("notifier")
        self.conversation_manager = ConversationManager(self.database)
