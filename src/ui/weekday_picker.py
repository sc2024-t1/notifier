from telebot import TeleBot


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
    def __init__(self, bot: TeleBot):
        self.bot: TeleBot = bot

    def start(self, chat_id: int):
        pass

    def stop(self):
        pass
