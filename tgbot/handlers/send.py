import asyncio

from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked
from aiogram.utils.markdown import quote_html

from tgbot.services import db
from tgbot.misc import schemas
from tgbot.keyboards import inline


async def send_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Write your message here',
        reply_markup=inline.cancel_markup,
    )
    await state.set_state('get_message_to_send')

async def get_message_and_send_to_users(message: Message, state: FSMContext):
    text = quote_html(message.text)
    message = await message.answer(
        text='Start sending messages',
    )
    await state.finish()
    users: list[schemas.TelegramUser] = await db.get_telegram_users()
    await send_message_to_users(
        bot=message.bot,
        users=users,
        text=text,
    )
    await message.edit_text(
        text='Messages was sent',
    )

async def send_message_to_users(
    bot: Bot, 
    message: str,
    users: list[schemas.TelegramUser]
    ):
    for user in users:
        await asyncio.sleep(1)
        try: 
            await bot.send_message(
                chat_id=user.telegram_id,
                text=message,
            )
        except (ChatNotFound, UserDeactivated, BotBlocked):
            pass
            

def register_send_handlers(dp: Dispatcher):
    dp.register_message_handler(
        send_handler,
        commands=['send'],
    )
    dp.register_message_handler(
        get_message_and_send_to_users,
        state='get_message_to_send',
    )