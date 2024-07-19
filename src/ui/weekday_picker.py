from typing import Callable, Optional

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
    def __init__(self, bot: Notifier, callback: Callable, weekdays: Optional[Weekdays] = None, *args, **kwargs):
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
        self.callback: Callable = callback
        self.args = args
        self.kwargs = kwargs

        self.weekdays: Weekdays = weekdays or Weekdays()

    def start(self, chat_id: int):
        """
        Starts the UI. Note that this function won't block. It will return immediately after the UI is started.
        The callback will be called when the user finishes picking the weekdays.
        :param chat_id: The chat ID to send the UI to.
        :return: None
        """
        # TODO: Registers the handler to the bot then start the UI.
        self.callback(chat_id, Weekdays(1), *self.args, **self.kwargs)  # Temporary
        self.stop()

    def stop(self):
        # TODO: Unregister the handler.
        pass
