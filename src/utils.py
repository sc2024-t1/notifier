from pymongo.database import Database
from telebot import TeleBot
from telebot.types import Message

from src.models.user import User


def ensure_user_settings(bot: TeleBot, database: Database, message: Message):
    user_settings = User.find_one(database, user_id=message.from_user.id)

    if not user_settings:
        bot.send_message(message.chat.id, "You haven't set up your settings yet. Please use the /start command.")  # TODO: 編輯這個訊息

        return False
