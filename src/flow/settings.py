from typing import Iterable

from pymongo.database import Database
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.bot import Notifier
from src.database.character import Character
from src.database.habit import Habit
from src.database.performance import Performance
from src.database.user import User
from src.ui.character_picker import CharacterPicker
from src.utils import ensure_user_settings, generate_heatmap


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
    This isn't actually a flow, just a set of commands.
    """

    def __init__(self, bot: Notifier, database: Database):
        self.bot: Notifier = bot
        self.database: Database = database

    def habits(self, message: Message):
        if not ensure_user_settings(self.bot, self.database, message):
            return
        
        habits = Habit.find(self.database)

        habit_text = "以下是你目前追蹤中的習慣：\n\n"

        for habit in habits:
            habit_text += (f"{habit.title}\n"
                           f"{str(habit.weekdays)}\n"
                           f"{', '.join(habit.times)}\n\n")

        self.bot.reply_to(message, habit_text)

    def start(self, message: Message):
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("點我以開始選擇角色", callback_data="select_character"))

        self.bot.send_message(
            message.chat.id,
            f"{message.from_user.full_name} 好！歡迎使用本習慣養成軟體！你可以設定你的目標和時間，機器人會在適當的時候提醒你。\n"
            "完成後，你可以與角色互動，系統會根據對話判斷你的完成狀態。本軟體也會定期統計你的習慣完成狀況，以熱力圖展示，還有各種成就等你解鎖喔～",
            reply_markup=markup
        )

        return markup

    def select_character(self, call: CallbackQuery):
        self.bot.answer_callback_query(call.id, text="請開始選擇你的角色！")
        characters: Iterable[Character] = Character.find(self.database)  # 可選的角色列表

        picker = CharacterPicker(
            bot=self.bot,
            chat_id=call.message.chat.id,
            callback=self.character_picking_callback,
            characters=list(characters),
            user_id=call.from_user.id
        )

        picker.start()

    def help(self, message: Message):
        self.bot.reply_to(
            message,
            "哈囉！以下是功能列表和使用方式"
            "\n使用 /start 開始你的習慣養成機器人"
            "\n輸入 /help 讓我為你介紹所有功能列表和如何使用這些功能"
            "\n利用 /character 讓我為你顯示所有角色列表並選擇你想要的角色"
            "\n輸入 /add_habit 可以新增想養成的習慣（一次養成一種哦！我們慢慢來），並設定執行時間和執行次數，以及何時結算你的小任務"
            "\n輸入 /stats 獲得近期努力成果和熱力圖"
            "\n輸入 /reset 重置對話"
        )

    def character(self, message: Message):
        characters: Iterable[Character] = Character.find(self.database)  # 可選的角色列表

        picker = CharacterPicker(
            bot=self.bot,
            chat_id=message.chat.id,
            callback=self.character_picking_callback,
            characters=list(characters),
            user_id=message.from_user.id
        )

        picker.start()

    def character_picking_callback(self, chat_id: int, character: Character, user_id: int):
        self.bot.send_message(chat_id, text=f"✅ 成功將你的角色設定為 {character.name}！")

        character = Character.find_one(self.database, character_id=character.character_id)

        user_settings = User(database=self.database, user_id=user_id, selected_character_id=character.character_id)
        user_settings.upsert()

        self.bot.conversation_manager.close_conversation(user_id)  # Close the conversation to apply new character.

        conversation = self.bot.conversation_manager.get_conversation(user_id)

        self.bot.send_chat_action(chat_id, action="typing")
        self.bot.send_message(chat_id, text=conversation.ask("你好"))

    def reset(self, message: Message):
        if not ensure_user_settings(self.bot, self.database, message):
            return

        self.bot.conversation_manager.close_conversation(message.from_user.id)

        self.bot.reply_to(
            message,
            text="成功重置你的對話！"
        )

    def stats(self, message: Message):
        if not ensure_user_settings(self.bot, self.database, message):
            return

        performances = Performance.find(self.database, user_id=message.from_user.id)

        try:
            heatmap_path = generate_heatmap(list(performances))
        except ValueError:
            self.bot.reply_to(message, "❌ 無法生成熱力圖，你可能還沒有完成任何習慣？")
            return

        self.bot.send_photo(
            chat_id=message.chat.id,
            photo=open(heatmap_path, 'rb')
        )


def setup(bot: Notifier, database: Database):
    flow = SettingsFlow(bot, database)

    bot.register_message_handler(flow.start, commands=["start"])
    bot.register_message_handler(flow.habits, commands=["habits"])
    bot.register_message_handler(flow.help, commands=["help"])
    bot.register_message_handler(flow.character, commands=["character"])
    bot.register_message_handler(flow.reset, commands=["reset"])
    bot.register_message_handler(flow.stats, commands=["stats"])
    bot.register_callback_query_handler(
        flow.select_character, lambda call: call.data == "select_character"
    )
