from pymongo.database import Database
from telebot.types import Message

from src.bot import Notifier
from src.ui.weekday_picker import WeekdayPicker, Weekdays


class TestFlow:
    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database

    def weekday_callback(self, chat_id: int, weekdays: Weekdays):
        print(f"The user selected {weekdays}")

    def weekday_test(self, message: Message):
        picker = WeekdayPicker(self.bot, message.chat.id, callback=self.weekday_callback)

        picker.start(message.chat.id)


def setup(bot: Notifier, database: Database):
    flow = TestFlow(bot, database)

    bot.register_message_handler(flow.weekday_test, commands=["weekday"])
