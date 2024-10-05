from abc import ABC, abstractmethod
from aiogram import Bot, Dispatcher

from settings.bot import bot_settings
from core.storages.bot import BotStorage
from routes.bot.commands import commands_router


class BaseBot(ABC):
    @abstractmethod
    def run(self) -> None:
        self._set_base_settings()

    def _set_base_settings(self) -> None:
        dispatcher = Dispatcher()
        bot = Bot(token=bot_settings.bot_token)

        dispatcher.include_router(commands_router)

        BotStorage().set_info((bot, dispatcher))
