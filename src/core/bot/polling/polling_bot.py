import asyncio
import uvloop

from core.storages.bot import BotStorage
from core.bot.base_bot import BaseBot


class PollingBot(BaseBot):
    def run(self) -> None:
        super().run()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.run(self._start_bot())

    async def _start_bot(self) -> None:
        (bot, dispatcher) = BotStorage().get_info()
        await dispatcher.start_polling(bot)


polling_bot = PollingBot()
