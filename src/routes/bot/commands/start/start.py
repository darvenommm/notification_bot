from aiogram.filters import CommandStart
from aiogram.types import Message

from routes.bot.commands import commands_router


@commands_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Hello")
