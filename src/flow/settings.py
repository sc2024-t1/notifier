from pymongo.database import Database
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


def generate_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Yes", callback_data="cb_yes"),
        InlineKeyboardButton("No", callback_data="cb_no")
    )
    return markup


class SettingsFlow:
    """
    This isn't actually a flow, just some utility commands.
    """

    def __init__(self, bot: TeleBot, database: Database):
        self.bot: TeleBot = bot
        self.database: Database = database

    def start(self, message: Message):
        # TODO: /start 指令
        # TODO: 回覆用戶一個歡迎訊息，其中包含這個機器人的基本使用方法
        self.bot.reply_to(message, "Hello!")  # TODO: EDIT THIS

    def help(self, message: Message):
        # TODO: /help 指令
        # TODO: 回覆用戶一個幫助訊息，其中包含這個機器人的指令列表
        self.bot.reply_to(message, "Hello!")


def setup(bot: TeleBot, database: Database):
    flow = SettingsFlow(bot, database)

    bot.register_message_handler(flow.start, commands=["start"])
    bot.register_message_handler(flow.help, commands=["help"])