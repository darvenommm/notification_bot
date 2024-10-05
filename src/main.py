from sys import path as python_path
from pathlib import Path

current_dir = Path(__file__).resolve().parent
python_path.append(str(current_dir))
python_path.append(str(current_dir.parent))

from settings.bot import bot_settings, BotType


def start_bot() -> None:
    match bot_settings.bot_type:
        case BotType.WEBHOOKS:
            from core.bot.webhooks import webhooks_bot

            webhooks_bot.run()
        case BotType.POLLING:
            from core.bot.polling import polling_bot

            polling_bot.run()


if __name__ == "__main__":
    start_bot()
