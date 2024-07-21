import uuid

from pymongo.database import Database
from telebot.types import Message

from src.bot import Notifier
from src.database.habit import Habit
from src.database.user import User
from src.ui.weekday_picker import Weekdays, WeekdayPicker
from src.utils import ensure_user_settings


# TODO: assigned to 13
class AddHabitFlow:
    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database

    def add_habit(self, message: Message):
        if not (user_settings := ensure_user_settings(self.bot, self.database, message)):
            return

        self.bot.reply_to(message, user_settings.selected_character.ask_habit_title)  # TODO: 編輯這個訊息

        self.bot.register_next_step_handler(message, self.habit_title, user_settings=user_settings)

    def habit_title(self, message: Message, user_settings: User):
        habit_title = message.text

        self.bot.reply_to(
            message, user_settings.selected_character.ask_habit_title_ack
            .replace("%habit_title%", habit_title)
        )  # TODO: 編輯這個訊息

        picker = WeekdayPicker(
            self.bot, message.chat.id,
            self.habit_weekdays,
            habit_title=habit_title,
            user_settings=user_settings,
            text=user_settings.selected_character.ask_weekday
        )
        picker.start()

    def habit_weekdays(self, chat_id: int, weekdays: Weekdays, habit_title: str, user_settings: User):
        message = self.bot.send_message(
            chat_id,
            user_settings.selected_character.ask_habit_time
            .replace("%weekdays%", str(weekdays))
            .replace("%habit_title%", habit_title)
        )  # TODO: 編輯這個訊息

        self.bot.register_next_step_handler(
            message, self.habit_times, habit_title=habit_title, weekdays=weekdays, user_settings=user_settings
        )

    def habit_times(self, message: Message, habit_title: str, weekdays: Weekdays, user_settings: User):
        times = message.text.split(", ")

        if any(time not in ["{:02d}:00".format(i) for i in range(24)] for time in times):
            self.bot.reply_to(message, user_settings.selected_character.wrong_time_format)  # TODO: 編輯這個訊息
            self.bot.register_next_step_handler(
                message, self.habit_times, habit_title=habit_title, weekdays=weekdays, user_settings=user_settings
            )
            return

        self.bot.reply_to(
            message,
            user_settings.selected_character.add_habit_done
            .replace("%weekdays%", str(weekdays))
            .replace("%times%", ', '.join(times))
            .replace("%habit_title%", habit_title)
        )  # TODO: 編輯這個訊息

        self.habit_upsert(message, habit_title=habit_title, weekdays=weekdays, times=times, user_settings=user_settings)

    def habit_upsert(self, message: Message, habit_title: str, weekdays: Weekdays, times: list[str],
                     user_settings: User):
        habit = Habit(
            database=self.database,
            owner_id=message.from_user.id,
            title=habit_title,
            habit_id=str(uuid.uuid4()),
            weekdays=weekdays.flags,
            times=times
        )

        habit.upsert()
        self.bot.send_message(
            message.chat.id,
            user_settings.selected_character.add_habit_upsert_success
        )


def setup(bot: Notifier, database: Database):
    flow = AddHabitFlow(bot, database)

    bot.register_message_handler(flow.add_habit, commands=["add_habit"])
