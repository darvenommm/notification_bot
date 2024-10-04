import uvloop

from src.core.storages import BotStorage
from .base_bot import BaseBot


class PollingBot(BaseBot):
    def run(self) -> None:
        super().run()
        uvloop.run(self._start_bot())

    async def _start_bot(self) -> None:
        (bot, dispatcher) = BotStorage().get_info()

        await bot.delete_webhook()
        await dispatcher.start_polling(bot)
