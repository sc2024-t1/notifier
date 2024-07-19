from telebot import TeleBot


class UtilitiesFlow:
    """
    This isn't actually a flow, just some utility commands.
    """

    def __init__(self, bot: TeleBot):
        self.bot: TeleBot = bot

    def start(self, message):
        # TODO: /start 指令
        # TODO: 回覆用戶一個歡迎訊息，其中包含這個機器人的基本使用方法
        self.bot.reply_to(message, "Hello!")  # TODO: EDIT THIS

    def help(self, message):
        # TODO: /help 指令
        # TODO: 回覆用戶一個幫助訊息，其中包含這個機器人的指令列表
        self.bot.reply_to(message, "Hello!")


def setup(bot: TeleBot):
    flow = UtilitiesFlow(bot)

    bot.register_message_handler(flow.start, commands=["start"])
    bot.register_message_handler(flow.help, commands=["help"])
