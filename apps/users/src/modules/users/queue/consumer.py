from aio_pika.abc import AbstractIncomingMessage
from msgpack.fallback import unpackb  # type: ignore[import-untyped]
from typing import Any, cast

from users.src.core.queue import queue_connector
from .constants import USERS_RESPONSE_QUEUE
from ..repository import users_repository
from ..dtos.update import UpdateUserDTO


class UsersConsumer:
    async def __process_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            user_id = cast(int | None, message.headers.get("correlation-id"))

            if user_id is None:
                print("Not found user_id in correlation-id header")
                await message.ack()
                return

            payload: dict[str, Any] = unpackb(message.body)
            user_data = UpdateUserDTO(
                full_name=payload["full_name"],
                username=payload["username"],
            )
            await users_repository.update(user_id, user_data)

            await message.ack()
            print("ack start consumer")

    async def start(self) -> None:
        print("start consuming users")

        async with queue_connector.get_connection() as session:
            response_queue = await session.get_queue(USERS_RESPONSE_QUEUE)

            async with response_queue.iterator() as messages_iterator:
                async for message in messages_iterator:
                    await self.__process_message(message)


users_consumer = UsersConsumer()
