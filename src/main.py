from os import getenv, listdir

from dotenv import load_dotenv
from google import generativeai
from pymongo import MongoClient
from pymongo.database import Database
from telebot import TeleBot


def main():
    load_dotenv()

    generativeai.configure(api_key=getenv("GEMINI_API_KEY"))

    bot = TeleBot(getenv("BOT_TOKEN"))
    database = MongoClient(getenv("MONGO_URI")).get_database("notifier")

    register_flows(bot, database)

    bot.infinity_polling()


def register_flows(bot: TeleBot, database: Database):
    for file in listdir("src/flow"):
        if not file.endswith('.py'):
            continue

        module = __import__(f"flow.{file[:-3]}", fromlist=["setup"])
        module.setup(bot, database)


if __name__ == "__main__":
    main()
