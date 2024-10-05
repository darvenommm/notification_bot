from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    domain: str = Field(alias="SERVER_DOMAIN")
    host: str = Field("0.0.0.0", alias="SERVER_HOST")
    port: int = Field(8080, alias="SERVER_PORT", ge=0, le=65535)

    webhook_path: str = Field(alias="WEBHOOK_PATH")
    webhook_secret: str | None = Field(None, alias="WEBHOOK_SECRET")

    workers_count: int = Field(1, alias="WORKERS_COUNT", ge=1)

    @property
    def webhook_url(self) -> str:
        return f"{self.domain}/{self.webhook_path.lstrip('/')}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


server_settings = ServerSettings()
