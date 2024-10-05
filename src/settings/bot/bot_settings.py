from enum import StrEnum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotType(StrEnum):
    WEBHOOKS = "webhooks"
    POLLING = "polling"


class BotSettings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    bot_type: BotType = Field(BotType.POLLING, alias="BOT_TYPE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


bot_settings = BotSettings()
