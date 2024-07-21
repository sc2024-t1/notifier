import uuid
from datetime import datetime

from pymongo.database import Database
from telebot.types import Message, ReactionTypeEmoji

from src.bot import Notifier
from src.database.habit import Habit
from src.database.performance import Performance
from src.database.user import User
from src.utils import ensure_user_settings


class NotifyFlow:
    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database

        self.waiting_for_ack: dict[int, list[Habit]] = {}  # List of users waiting for performance acknowledgment

    def chat(self, message: Message):
        """
        Chat with the character the user selected.
        :param message: The message instance.
        :return: None
        """
        if not (user_settings := ensure_user_settings(self.bot, self.database, message)):
            return

        if message.from_user.id in self.waiting_for_ack:
            while self.waiting_for_ack.get(message.from_user.id):
                habit = self.waiting_for_ack[message.from_user.id].pop()

                performance = Performance(
                    self.database,
                    habit_id=habit.habit_id,
                    performance_id=str(uuid.uuid4()),
                    user_id=message.from_user.id,
                    succeeded=True,
                    completed_at=datetime.now()
                )

                performance.upsert()

                self.bot.set_message_reaction(
                    message.chat.id,
                    message.message_id,
                    reaction=[ReactionTypeEmoji(
                        emoji="🔥"
                    )]
                )

                if len(self.waiting_for_ack[message.from_user.id]) == 0:
                    del self.waiting_for_ack[message.from_user.id]

        self.bot.send_chat_action(message.chat.id, "typing")

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

        self.bot.send_chat_action(message.chat.id, "typing")

        habits = Habit.find(self.database, owner_id=message.from_user.id)

        for habit in habits:
            conversation = self.bot.conversation_manager.get_conversation(message.from_user.id)

            response = conversation.notify(habit_title=habit.title)

            self.bot.send_message(message.chat.id, response + "\n\n(請回覆這則訊息來確認你的習慣！)")

            if self.waiting_for_ack.get(message.from_user.id) is None:
                self.waiting_for_ack[message.from_user.id] = [habit]
            else:
                self.waiting_for_ack[message.from_user.id].append(habit)


def setup(bot: Notifier, database: Database):
    flow = NotifyFlow(bot, database)

    bot.register_message_handler(
        flow.chat,
        func=lambda message: message.text not in ['/add_habit', '/start', '/character',
                                                  '/notify', '/help', '/reset', '/stats']
    )
    bot.register_message_handler(flow.notify, commands=["notify"])
