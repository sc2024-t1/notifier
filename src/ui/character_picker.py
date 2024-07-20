from typing import Callable, Optional

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from src.bot import Notifier
from src.database.character import Character


class CharacterPicker:
    def __init__(
            self,
            bot: Notifier,
            chat_id: int,
            callback: Callable,
            characters: list[Character],
            selected: int = 0,
            *args, **kwargs
    ):
        """
        A UI for picking character.
        :param bot: The bot instance.
        :param chat_id: The chat id to send the message to.
        :param callback: The callback to call when the user finishes picking the weekdays.
        The callback should accept the chat_id as first argument then the selected character as second argument.
        :param characters: The list of characters to show.
        :param selected: The index of the selected character.
        :param args: The positional arguments to pass to the callback.
        :param kwargs: The keyword arguments to pass to the callback.
        """
        self.bot: Notifier = bot
        self.chat_id: int = chat_id
        self.callback: Callable = callback
        self.args = args
        self.kwargs = kwargs

        self.characters: list[Character] = characters
        self.selected_index = selected

        self.message: Optional[Message] = None

        self.ended: bool = False

    @property
    def selected_character(self):
        return self.characters[self.selected_index]

    def generate_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data="previous"
                    ),
                    InlineKeyboardButton(
                        text=self.characters[self.selected_index].name,
                        callback_data="select"
                    ),
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data="next"
                    )
                ]
            ]
        )

    def render(self):
        if self.message:
            self.bot.edit_message_media(
                chat_id=self.message.chat.id,
                message_id=self.message.id,
                media=InputMediaPhoto(
                    media=self.selected_character.avatar_url,
                )
            )
            self.bot.edit_message_caption(
                caption=f"**{self.selected_character.name}**\n\n"
                        f"{self.selected_character.description}\n\n"
                        f"---\n"
                        f"透過下方按鈕選擇你喜歡的角色，點擊角色名稱確認！",
                chat_id=self.message.chat.id,
                message_id=self.message.id,
                reply_markup=self.generate_markup(),
                parse_mode="markdown"
            )
        else:
            self.message = self.bot.send_photo(
                caption=f"**{self.selected_character.name}**\n\n"
                        f"{self.selected_character.description}\n\n"
                        f"---\n"
                        f"透過下方按鈕選擇你喜歡的角色，點擊角色名稱確認！",
                chat_id=self.chat_id,
                photo=self.characters[self.selected_index].avatar_url,
                reply_markup=self.generate_markup(),
                parse_mode="markdown"
            )

    def callback_query_handler(self, call: CallbackQuery):
        if call.data == "previous":
            self.selected_index -= 1

            if self.selected_index < 0:
                self.selected_index = len(self.characters) - 1

            self.render()
            self.bot.answer_callback_query(
                call.id,
                f"已選擇 {self.characters[self.selected_index]} ({self.selected_index + 1}/{len(self.characters)})"
            )

        elif call.data == "next":
            self.selected_index += 1

            if self.selected_index >= len(self.characters):
                self.selected_index = 0

            self.render()
            self.bot.answer_callback_query(
                call.id,
                f"已選擇 {self.selected_character.name} ({self.selected_index + 1}/{len(self.characters)})"
            )

        elif call.data == "select":
            self.bot.answer_callback_query(
                call.id,
                f"已選擇 {self.selected_character}"
            )
            self.bot.delete_message(self.chat_id, self.message.id)
            self.callback(self.chat_id, self.characters[self.selected_index], *self.args, **self.kwargs)

        else:
            raise ValueError(f"Unknown callback data: {call.data}")

    def start(self):
        self.render()

        self.bot.register_callback_query_handler(
            self.callback_query_handler,
            lambda call: self.chat_id == self.message.chat.id and self.message.id == call.message.id and not self.ended
        )
