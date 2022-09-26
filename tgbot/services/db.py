from asgiref.sync import sync_to_async

from web.app import models
from tgbot.misc import schemas


@sync_to_async
def add_telegram_user(telegram_id, full_name) -> None:
    models.TelegramUser.objects.create(
        telegram_id=telegram_id,
        full_name=full_name,
    )

@sync_to_async
def get_telegram_users() -> schemas.TelegramUser:
    return list(
        schemas.TelegramUser(**user) \
            for user in models.TelegramUser.objects.all().values()
    )