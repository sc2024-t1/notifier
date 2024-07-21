from typing import Callable, Optional

from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot import Notifier


class Weekdays:
    MONDAY: int = 1 << 0
    TUESDAY: int = 1 << 1
    WEDNESDAY: int = 1 << 2
    THURSDAY: int = 1 << 3
    FRIDAY: int = 1 << 4
    SATURDAY: int = 1 << 5
    SUNDAY: int = 1 << 6

    def __init__(self, flags: int = 0) -> None:
        self.flags: int = flags

    def enable(self, day: int) -> None:
        self.flags |= day

    def disable(self, day: int) -> None:
        self.flags &= ~day

    def is_enabled(self, day: int) -> bool:
        return bool(self.flags & day)

    def toggle(self, day: int) -> None:
        if self.is_enabled(day):
            self.disable(day)
        else:
            self.enable(day)

    def __str__(self) -> str:
        days = [
            ("Monday", self.MONDAY),
            ("Tuesday", self.TUESDAY),
            ("Wednesday", self.WEDNESDAY),
            ("Thursday", self.THURSDAY),
            ("Friday", self.FRIDAY),
            ("Saturday", self.SATURDAY),
            ("Sunday", self.SUNDAY),
        ]
        enabled_days = [name for name, flag in days if self.is_enabled(flag)]
        return ", ".join(enabled_days) if enabled_days else "None"


class WeekdayPicker:
    def __init__(
            self,
            bot: Notifier,
            chat_id: int,
            callback: Callable,
            weekdays: Optional[Weekdays] = None,
            *args, **kwargs
    ):
        """
        A UI for picking weekdays.
        :param bot: The bot instance.

        :param callback: The callback to call when the user finishes picking the weekdays.
        The callback should accept the chat_id as first argument then the weekdays as the second argument.
        :param weekdays: The initial weekdays to show.
        :param args: The positional arguments to pass to the callback.
        :param kwargs: The keyword arguments to pass to the callback.
        """
        self.bot: Notifier = bot
        self.chat_id: int = chat_id
        self.callback: Callable = callback
        self.args = args
        self.kwargs = kwargs

        self.weekdays: Weekdays = weekdays or Weekdays()

        self.message: Optional[Message] = None

        self.ended: bool = False

    def render(self):
        if self.message:
            self.bot.edit_message_text(
                chat_id=self.message.chat.id,
                message_id=self.message.message_id,
                text="Please select the weekdays:",
                reply_markup=self.generate_markup()
            )
        else:
            self.message = self.bot.send_message(
                chat_id=self.chat_id,
                text="Please select the weekdays:",
                reply_markup=self.generate_markup()
            )

    def generate_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=5)

        markup.add(
            InlineKeyboardButton(
                f"一 {'✅' if self.weekdays.is_enabled(Weekdays.MONDAY) else '❌'}",
                callback_data=Weekdays.MONDAY
            ),
            InlineKeyboardButton(
                f"二 {' ✅' if self.weekdays.is_enabled(Weekdays.TUESDAY) else '❌'}",
                callback_data=Weekdays.TUESDAY
            ),
            InlineKeyboardButton(
                f"三 {'✅' if self.weekdays.is_enabled(Weekdays.WEDNESDAY) else '❌'}",
                callback_data=Weekdays.WEDNESDAY
            ),
            InlineKeyboardButton(
                f"四 {'✅' if self.weekdays.is_enabled(Weekdays.THURSDAY) else '❌'}",
                callback_data=Weekdays.THURSDAY
            ),
            InlineKeyboardButton(
                f"五 {'✅' if self.weekdays.is_enabled(Weekdays.FRIDAY) else '❌'}",
                callback_data=Weekdays.FRIDAY
            ),
            InlineKeyboardButton(
                f"六 {'✅' if self.weekdays.is_enabled(Weekdays.SATURDAY) else '❌'}",
                callback_data=Weekdays.SATURDAY
            ),
            InlineKeyboardButton(
                f"日 {'✅' if self.weekdays.is_enabled(Weekdays.SUNDAY) else '❌'}",
                callback_data=Weekdays.SUNDAY
            )
        )

        markup.add(InlineKeyboardButton("儲存", callback_data="submit"))

        return markup

    def callback_query_handler(self, call: CallbackQuery):
        try:
            self.bot.answer_callback_query(call.id, "✅ 成功選取")
            self.weekdays.toggle(int(call.data))
            self.render()
        except ValueError:
            pass

        if call.data == "submit":
            self.bot.answer_callback_query(call.id, "✅ 成功送出！")
            self.bot.delete_message(self.chat_id, self.message.id)
            self.ended = True
            self.callback(self.chat_id, self.weekdays, *self.args, **self.kwargs)

    def start(self):
        """
        Starts the UI. Note that this function won't block. It will return immediately after the UI is started.
        The callback will be called when the user finishes picking the weekdays.
        :return: None
        """
        self.render()

        # This will cause some problem since the handlers are never removed.
        # Anyway this library doesn't seem providing a method for removing handlers.
        # Should be fine if the bot won't run too long.
        self.bot.register_callback_query_handler(
            self.callback_query_handler,
            lambda call: self.chat_id == self.message.chat.id and self.message.id == call.message.id and not self.ended
        )
