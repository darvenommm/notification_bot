from aiogram import Bot, Dispatcher
from typing import Self


class BotStorage:
    __instance: Self
    __dispatcher: Dispatcher
    __bot: Bot

    def __new__(cls, *args, **kwargs) -> Self:
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)

        return cls.__instance

    @property
    def bot(self) -> Bot:
        if not self.__bot:
            raise ValueError("Not defined bot")

        return self.__bot

    @bot.setter
    def bot(self, new_bot: Bot) -> None:
        if not isinstance(new_bot, Bot):
            raise TypeError(f"new_bot instance is not a Bot")

        self.__bot = new_bot

    @property
    def dispatcher(self) -> Dispatcher:
        if not self.__dispatcher:
            raise ValueError("Not defined dispatcher")

        return self.__dispatcher

    @dispatcher.setter
    def dispatcher(self, new_dispatcher: Dispatcher) -> None:
        if not isinstance(new_dispatcher, Dispatcher):
            raise TypeError(f"new_bot instance is not a Dispatcher")

        self.__dispatcher = new_dispatcher

    def get_info(self) -> tuple[Bot, Dispatcher]:
        return (self.bot, self.dispatcher)

    def set_info(self, info: tuple[Bot, Dispatcher]) -> None:
        self.bot = info[0]
        self.dispatcher = info[1]
