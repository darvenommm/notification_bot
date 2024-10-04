from aiogram.filters import CommandStart
from aiogram.types import Message

from .router import router


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Hello")
