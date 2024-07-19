from pymongo.database import Database
from telebot.types import Message

from src.bot import Notifier
from src.database.habit import Habit
from src.database.user import User
from src.utils import ensure_user_settings


class NotifyFlow:
    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database

    def chat(self, message: Message):
        """
        Chat with the character the user selected.
        :param message: The message instance.
        :return: None
        """
        # TODO: This is a temporary method. It will actually be global handling instead of a single command.
        if not (user_settings := ensure_user_settings(self.bot, self.database, message)):
            self.bot.reply_to(message, "You haven't set up your settings yet. Please use the /start command.")
            return

        conversation = self.bot.conversation_manager.get_conversation(user_settings.user_id)

        self.bot.reply_to(message, conversation.chat(message.text.lstrip("/chat ")))

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
