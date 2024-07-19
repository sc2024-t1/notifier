from telebot import TeleBot


class Test:
    def __init__(self, bot: TeleBot):
        self.bot: TeleBot = bot

    def test(self, message):
        self.bot.send_message()


def setup(bot: TeleBot):
    flow = Test(bot)

    bot.register_message_handler(flow.test, commands=["test"])
