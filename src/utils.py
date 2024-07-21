import calendar
import uuid
from typing import Optional, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pymongo.database import Database
from telebot.types import Message

from src.bot import Notifier
from src.database.performance import Performance
from src.database.user import User


def ensure_user_settings(bot: Notifier, database: Database, message: Message) -> Optional[User]:
    """
    Ensure that the user has set up their settings.
    :param bot: The bot instance.
    :param database: The database instance.
    :param message: The message instance.
    :return: True if the user has set up their settings, False otherwise.
    """
    user_settings = User.find_one(database, user_id=message.from_user.id)

    if user_settings:
        return user_settings
    else:
        bot.send_message(
            message.chat.id, "我在資料庫中找不到有關你的紀錄，你能夠試試看 /start 指令嗎？"
        )
        return None


def generate_heatmap(performances: List[Performance]) -> str:
    """
    Generate a heatmap of the performances.
    This will generate a image in the img directory. Careful with the file size.
    :param performances: The performances to generate the heatmap from.
    :return: The path to the generated heatmap image.
    """
    # Create a DataFrame from the performances
    data = {
        'date': [performance.completed_at.date() for performance in performances],
        'succeeded': [performance.succeeded for performance in performances]
    }
    df = pd.DataFrame(data)

    # Count successes per day
    daily_success = df.groupby('date').succeeded.sum().astype(int).reset_index()

    # Create a full range of dates
    start_date = df['date'].min()
    end_date = df['date'].max()
    all_dates = pd.date_range(start=start_date, end=end_date)

    # Reindex to include all dates
    daily_success = daily_success.set_index('date').reindex(all_dates, fill_value=0).rename_axis('date').reset_index()

    # Add week and weekday columns
    daily_success['week'] = daily_success['date'].apply(lambda x: x.isocalendar()[1])
    daily_success['weekday'] = daily_success['date'].apply(lambda x: x.weekday())

    # Pivot table for heatmap
    pivot_table = daily_success.pivot_table(values='succeeded', index='weekday', columns='week', fill_value=0)

    # Plot heatmap
    plt.figure(figsize=(14, 4))
    sns.heatmap(pivot_table, cmap='YlGnBu', cbar=True, linewidths=0.5, annot=True, fmt='g')
    plt.title('Performance Heatmap')
    plt.xlabel('Week Number')
    plt.ylabel('Day of Week')
    plt.yticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=list(calendar.day_name), rotation=0)
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = f"./img/{str(uuid.uuid4())}.jpg"
    plt.savefig(path, format='jpg', dpi=300)

    plt.close()

    return path
