from pymongo.database import Database
from telebot.types import Message

from src.bot import Notifier
from src.database.habit import Habit
from src.database.user import User


class NotifyFlow:
    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database

    def on_message(self, message: Message):
        # TODO: 處理日常聊天
        # TODO: 確認這個訊息是否是回覆自提醒
        pass

    def notify(self, user_id: int):
        """
        Notifies the user for their upcoming habits. Ignores the time settings
        and sends the message immediately.
        :param user_id: The user ID.
        """
        user_settings = User.find_one(self.database, user_id=user_id)

        if not user_settings:
            raise ValueError("User settings not found.")

        habits = Habit.find(self.database, owner_id=user_id)

        for habit in habits:
            pass


def setup(bot: Notifier, database: Database):
    flow = NotifyFlow(bot, database)

    bot.register_message_handler(flow.on_message, content_types=["text"])
    # TODO: Register the handlers
