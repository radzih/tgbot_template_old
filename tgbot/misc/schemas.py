import datetime

from pydantic import BaseModel


class TelegramUser(BaseModel):
    telegram_id: int
    full_name: str
    join_time: datetime.datetime
    language: str


class SupportRequest(BaseModel):
    id: int
    user_id: int
    created_time: datetime.datetime
