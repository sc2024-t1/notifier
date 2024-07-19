from os import getenv, listdir

from dotenv import load_dotenv
from google import generativeai
from pymongo.database import Database
from telebot import TeleBot

from src.bot import Notifier


def main():
    load_dotenv()

    generativeai.configure(api_key=getenv("GEMINI_API_KEY"))

    bot = Notifier(getenv("BOT_TOKEN"))

    register_flows(bot, bot.database)

    bot.infinity_polling()


def register_flows(bot: TeleBot, database: Database):
    for file in listdir("src/flow"):
        if not file.endswith('.py'):
            continue

        module = __import__(f"flow.{file[:-3]}", fromlist=["setup"])
        module.setup(bot, database)


if __name__ == "__main__":
    main()
