from aiogram.types import Update
from fastapi import Request, HTTPException
from http import HTTPStatus

from settings.server import server_settings
from core.storages.bot import BotStorage
from routes.server.tg.router import tg_router

SECRET_TOKEN_HEADER_NAME = "X-Telegram-Bot-Api-Secret-Token"


@tg_router.post(server_settings.webhook_path, status_code=HTTPStatus.OK)
async def handle_webhook_request(request: Request) -> None:
    if server_settings.webhook_secret != request.headers.get(SECRET_TOKEN_HEADER_NAME):
        raise HTTPException(HTTPStatus.FORBIDDEN, detail="Incorrect secret token")

    (bot, dispatcher) = BotStorage().get_info()

    update_data = await request.json()
    await dispatcher.feed_webhook_update(bot, Update(**update_data))
