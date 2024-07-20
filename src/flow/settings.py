from typing import Iterable

from pymongo.database import Database
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot import Notifier
from src.database.character import Character
from src.database.user import User
from src.ui.character_picker import CharacterPicker


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
        
    def start(self, message: Message):
        # TODO: /start 指令
        # TODO: 回覆用戶一個歡迎訊息，其中包含這個機器人的基本使用方法，且讓用戶選擇他的初始角色，選擇角色的邏輯應該在下方的 character 方法中
        # TODO: (assigned to Ain)
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("點我以開始選擇角色", callback_data= "start_character"))
        self.bot.send_message(message.chat.id, f"{message.from_user.full_name} 好！歡迎使用本習慣養成軟體！你可以設定你的目標和時間，機器人會在適當的時候提醒你。\
                              完成後，你可以與角色互動，系統會根據對話判斷你的完成狀態。本軟體也會定期統計你的習慣完成狀況，以熱力圖展示，還有各種成就等你解鎖喔～")
        # TODO: call the function "character" by hitting the button
        return markup
    
    def help(self, message: Message):
        # TODO: /help 指令
        # TODO: 回覆用戶一個幫助訊息，其中包含這個機器人的指令列表 ()
        # TODO: (assigned to Eva)
        self.bot.reply_to(message, "Hello!")

    def character(self, message: Message):
        characters: Iterable[Character] = Character.find(self.database)  # 可選的角色列表

        picker = CharacterPicker(
            bot=self.bot,
            chat_id=message.chat.id,
            callback=self.select_character,
            characters=list(characters),
            user_id=message.from_user.id
        )

        picker.start()

    def select_character(self, chat_id: int, character: Character, user_id: int):
        self.bot.send_message(chat_id, text=f"✅ 成功將你的角色設定為 {character.name}！")

        character = Character.find_one(self.database, character_id=character.character_id)

        user_settings = User(database=self.database, user_id=user_id, selected_character_id=character.character_id)
        user_settings.upsert()

        self.bot.conversation_manager.close_conversation(user_id)  # Close the conversation to apply new character.

        conversation = self.bot.conversation_manager.get_conversation(user_id)

        self.bot.send_chat_action(chat_id, action="typing")
        self.bot.send_message(chat_id, text=conversation.ask("你好"))


def setup(bot: Notifier, database: Database):
    flow = SettingsFlow(bot, database)

    bot.register_message_handler(flow.start, commands=["start"])
    bot.register_message_handler(flow.help, commands=["help"])
    bot.register_message_handler(flow.character, commands=["character"])
    bot.register_callback_query_handler(
        flow.select_character, lambda call: call.data in ["cb_yes", "cb_no"]
    )  # TODO: 編輯這個 lambda 函數來過濾 callback_data
