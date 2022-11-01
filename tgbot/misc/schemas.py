import datetime

from pydantic import BaseModel


class TelegramUser(BaseModel):
    telegram_id: int
    full_name: str
    join_time: datetime.datetime
    language: str
