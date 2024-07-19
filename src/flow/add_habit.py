from pymongo.database import Database
from telebot import TeleBot
from telebot.types import Message

from src.models.habit import Habit
from src.ui.weekday_picker import Weekdays, WeekdayPicker
from src.utils import ensure_user_settings


class AddHabitFlow:
    def __init__(self, bot: TeleBot, database: Database):
        self.bot: TeleBot = bot
        self.database: Database = database

    def add_habit(self, message: Message):
        if not ensure_user_settings(self.bot, self.database, message):
            return

        self.bot.reply_to(message, "What habit would you like to add?")  # TODO: 編輯這個訊息

        self.bot.register_next_step_handler(message, self.habit_name)

    def habit_name(self, message: Message):
        habit_name = message.text

        self.bot.reply_to(
            message, f"Got it! You want to add the habit '{habit_name}'. What is the description of this habit?",
        )  # TODO: 編輯這個訊息

        picker = WeekdayPicker(self.bot, self.habit_weekdays, habit_name=habit_name)
        picker.start(message.chat.id)

    def habit_weekdays(self, chat_id: int, weekdays: Weekdays, habit_name: str):
        message = self.bot.send_message(
            chat_id, "What time(s) would you like to do this habit? (e.g. 08:00, 12:00, 18:00)"
        )  # TODO: 編輯這個訊息

        self.bot.register_next_step_handler(message, self.habit_times, habit_name=habit_name, weekdays=weekdays)

    def habit_times(self, message: Message, habit_name: str, weekdays: Weekdays):
        times = message.text.split(", ")

        if any(time not in ["{:02d}:00".format(i) for i in range(24)] for time in times):
            self.bot.reply_to(message, "Invalid time format. Please use the format HH:00.")  # TODO: 編輯這個訊息
            return

        self.bot.reply_to(
            message, f"Got it! You want to add the habit '{habit_name}' on {weekdays} at {', '.join(times)}."
        )  # TODO: 編輯這個訊息

        self.habit_upsert(message, habit_name=habit_name, weekdays=weekdays, times=times)

    def habit_upsert(self, message: Message, habit_name: str, weekdays: Weekdays, times: list[str]):
        habit = Habit(
            database=self.database,
            owner_id=message.from_user.id,
            title=habit_name,
            habit_id="",
            weekdays=weekdays.flags,
            times=times
        )

        habit.upsert()

        self.bot.send_message(message.chat.id, "Habit added successfully!")  # TODO: 編輯這個訊息


def setup(bot: TeleBot, database: Database):
    flow = AddHabitFlow(bot, database)

    bot.register_message_handler(flow.add_habit, commands=["add_habit"])
