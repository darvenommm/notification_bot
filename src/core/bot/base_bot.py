from abc import ABC, abstractmethod
from aiogram import Bot, Dispatcher

from src.core.storages import BotStorage
from src.handlers.commands import commands_router


class BaseBot(ABC):
    @abstractmethod
    def run(self) -> None:
        self._set_base_settings()

    def _set_base_settings(self) -> None:
        bot = Bot(token="")
        dispatcher = Dispatcher()

        dispatcher.include_router(commands_router)

        BotStorage().set_info((bot, dispatcher))
