from os import getenv, listdir

from dotenv import load_dotenv
from telebot import TeleBot


def main():
    load_dotenv()

    bot = TeleBot(getenv("BOT_TOKEN"))

    register_flows(bot)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "Hello!")

    bot.infinity_polling()


def register_flows(bot: TeleBot):
    for file in listdir("src/flows"):
        if not file.endswith('.py'):
            continue

        module = __import__(f"flows.{file[:-3]}", fromlist=["setup"])
        module.setup(bot)


if __name__ == "__main__":
    main()
