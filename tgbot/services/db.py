from asgiref.sync import sync_to_async

from web.app import models
from tgbot.misc import schemas


@sync_to_async
def add_telegram_user(telegram_id: int, full_name: str) -> None:
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

@sync_to_async
def add_support_request(
    user_telegram_id: int,
    ) -> schemas.SupportRequest:
    request: models.SupportRequest = models.SupportRequest.objects.create(
        user_id=user_telegram_id,
    )
    return schemas.SupportRequest(**request.dict())

@sync_to_async
def delete_support_request(request_id) -> None:
    models.SupportRequest.objects.get(id=request_id).delete()

@sync_to_async
def get_support_request(id: int) -> schemas.SupportRequest:
    request: models.SupportRequest = models.SupportRequest.objects.get(id=id)
    return schemas.SupportRequest(**request.dict())