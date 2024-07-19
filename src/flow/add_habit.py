from telebot import TeleBot
from telebot.types import Message

from src.ui.weekday_picker import Weekdays


class AddHabitFlow:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def add_habit(self, message: Message):
        self.bot.reply_to(message, "What habit would you like to add?")

        self.bot.register_next_step_handler(message, self.habit_name)

    def habit_name(self, message: Message):
        habit_name = message.text

        self.bot.reply_to(
            message, f"Got it! You want to add the habit '{habit_name}'. What is the description of this habit?",
        )
        pass

    # TODO: Implement the ui.WeekdayPicker for interactive picking of weekdays here. self.habit_upsert as callback.
    # self.bot.register_next_step_handler(message, self.habit_days, habit_name=habit_name)

    # def habit_upsert(self, call, habit_name: str, weekdays: Weekdays, times: list[str]):


def setup(bot: TeleBot):
    flow = AddHabitFlow(bot)

    bot.register_message_handler(flow.add_habit, commands=["add_habit"])
    bot.register_callback_query_handler()
