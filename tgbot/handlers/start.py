from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from tgbot.services import db


async def start_handler(message: Message):
    await message.answer(
        text=f'Hello, {message.from_user.full_name}!',
    )
    await db.add_telegram_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
    )
    

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_handler,
        commands=['start'],
    )