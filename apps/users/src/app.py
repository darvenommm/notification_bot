import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from typing import Callable, AsyncContextManager, AsyncGenerator

from .settings.main import main_settings
from .core.queue import queue_connector
from .modules.users import users_controller, users_publisher, users_consumer


class App:
    __server: FastAPI

    def __init__(self) -> None:
        self.__server = self.__get_set_server()

    def start(self) -> None:
        uvicorn.run(
            self.__server,
            host=str(main_settings.server_host),
            port=main_settings.server_port,
            workers=main_settings.workers_count,
        )

    def __get_set_server(self) -> FastAPI:
        server = FastAPI(
            default_response_class=ORJSONResponse,
            docs_url="/swagger",
            lifespan=self.__get_lifespan(),
        )
        server.include_router(users_controller.router)

        return server

    def __get_lifespan(self) -> Callable[[FastAPI], AsyncContextManager[None]]:
        @asynccontextmanager
        async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
            await queue_connector.init_pool()

            publishing = asyncio.create_task(users_publisher.start())
            consuming = asyncio.create_task(users_consumer.start())

            yield

            try:
                publishing.cancel()
                consuming.cancel()
                await asyncio.gather(publishing, consuming)
            except asyncio.CancelledError:
                print("Success canceled publishing and consuming")

        return lifespan
