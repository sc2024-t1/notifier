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
        if not (user_settings := ensure_user_settings(self.bot, self.database, message)):
            return

        conversation = self.bot.conversation_manager.get_conversation(user_settings.user_id)

        self.bot.reply_to(message, conversation.ask(message.text.lstrip("/chat ")))

    def notify(self, message: Message):
        """
        Notifies the user for their upcoming habits. Ignores the time settings
        and sends the message immediately.
        :param message: The message instance.
        """
        user_settings = User.find_one(self.database, user_id=message.from_user.id)

        if not user_settings:
            raise ValueError("User settings not found.")

        habits = Habit.find(self.database, owner_id=message.from_user.id)

        for habit in habits:
            # TODO: Notify for each habit that has reached it's time
            conversation = self.bot.conversation_manager.get_conversation(message.from_user.id)

            response = conversation.notify(habit_title=habit.title)

            self.bot.send_message(message.chat.id, response)


def setup(bot: Notifier, database: Database):
    flow = NotifyFlow(bot, database)

    bot.register_message_handler(flow.chat, func=lambda message: message.text not in ['/add_habit', '/start', '/character', '/notify', '/help', '/reset'])
    bot.register_message_handler(flow.notify, commands=["notify"])
    # TODO: Register the handlers
