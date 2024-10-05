import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from typing import AsyncGenerator
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from settings.server import server_settings
from core.storages.bot import BotStorage
from core.bot.base_bot import BaseBot
from routes.server.tg import tg_router


class WebhooksBot(BaseBot):
    def run(self) -> None:
        super().run()
        uvicorn.run(
            self.get_server(),
            host=server_settings.host,
            port=server_settings.port,
            workers=server_settings.workers_count,
        )

    def get_server(self) -> FastAPI:
        server = FastAPI(
            docs_url="/swagger",
            lifespan=self._server_lifespan,
            default_response_class=ORJSONResponse,
        )

        server.include_router(tg_router)

        server.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])

        return server

    @staticmethod
    @asynccontextmanager
    async def _server_lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        bot = BotStorage().bot

        await bot.set_webhook(
            server_settings.webhook_url,
            secret_token=server_settings.webhook_secret,
        )
        yield
        await bot.delete_webhook()
        await bot.session.close()


webhooks_bot = WebhooksBot()
