from aiogram.dispatcher import Dispatcher
from aiogram.types import Message


async def start_handler(message: Message):
    await message.answer(
        text='Hello, world!',
    )
    

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_handler,
        commands=['start'],
    )