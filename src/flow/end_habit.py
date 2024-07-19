from pymongo.database import Database

from src.bot import Notifier


class EndHabit:
    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database


def setup(bot: Notifier, database: Database):
    flow = EndHabit(bot, database)
