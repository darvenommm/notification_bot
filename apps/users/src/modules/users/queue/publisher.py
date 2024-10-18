import asyncio
from aio_pika import Message
from aio_pika.abc import AbstractChannel
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore[import-untyped]
from msgpack import packb  # type: ignore[import-untyped]
from pydantic import BaseModel

from users.src.core.queue import queue_connector
from ..repository import users_repository
from .constants import USERS_EXCHANGE, USERS_QUEUE, USERS_RESPONSE_QUEUE


class Payload(BaseModel):
    user_id: int


class UsersPublisher:
    async def __declare(self, session: AbstractChannel) -> None:
        users_exchange = await session.declare_exchange(USERS_EXCHANGE, durable=True)
        users_queue = await session.declare_queue(USERS_QUEUE, durable=True)
        await users_queue.bind(users_exchange, routing_key=USERS_QUEUE)

        await session.declare_queue(USERS_RESPONSE_QUEUE, durable=True)

    async def __job(self) -> None:
        print("start jobbing")
        users = await users_repository.get_all()

        async with queue_connector.get_connection() as session:
            for user in users:
                print(f"processing user {user.user_id}")
                payload: bytes = packb(Payload(user_id=user.user_id).model_dump())
                message = Message(payload, headers={"reply-to": USERS_RESPONSE_QUEUE})

                users_exchange = await session.get_exchange(USERS_EXCHANGE, ensure=True)
                await users_exchange.publish(message, USERS_QUEUE)

    async def __set_scheduler(self) -> None:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.__job, "cron", hour=0, minute=0)
        scheduler.start()

    async def start(self) -> None:
        print("Start publishing users")

        async with queue_connector.get_connection() as session:
            await self.__declare(session)
            await self.__set_scheduler()


users_publisher = UsersPublisher()
