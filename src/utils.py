from typing import Optional

from pymongo.database import Database
from telebot.types import Message

from src.bot import Notifier
from src.database.performance import Performance
from src.database.user import User


def ensure_user_settings(bot: Notifier, database: Database, message: Message) -> Optional[User]:
    """
    Ensure that the user has set up their settings.
    :param bot: The bot instance.
    :param database: The database instance.
    :param message: The message instance.
    :return: True if the user has set up their settings, False otherwise.
    """
    user_settings = User.find_one(database, user_id=message.from_user.id)

    if user_settings:
        return user_settings
    else:
        bot.send_message(
            message.chat.id, "我在資料庫中找不到有關你的紀錄，你能夠試試看 /start 指令嗎？"
        )
        return None


def create_heat_map(performances: list[Performance]):
    """
    Create a heat map of the user's history performances
    :return:
    """
    # TODO: 透過傳入的 performances 產出熱力圖  (assigned to Yoru)
    pass
