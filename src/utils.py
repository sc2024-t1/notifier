from pymongo.database import Database
from telebot import TeleBot
from telebot.types import Message

from src.models.user import User


def ensure_user_settings(bot: TeleBot, database: Database, message: Message) -> bool:
    """
    Ensure that the user has set up their settings.
    :param bot: The bot instance.
    :param database: The database instance.
    :param message: The message instance.
    :return: True if the user has set up their settings, False otherwise.
    """
    user_settings = User.find_one(database, user_id=message.from_user.id)

    if user_settings:
        return True
    else:
        bot.send_message(
            message.chat.id, "You haven't set up your settings yet. Please use the /start command."
        )  # TODO: 編輯這個訊息
        return False
