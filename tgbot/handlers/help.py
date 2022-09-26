from aiogram.bot import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher, FSMContext

from tgbot.keyboards import inline
from tgbot.config import Config


async def help_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Write your message here',
        reply_markup=inline.cancel_markup,
    )
    await state.set_state('get_message_to_help')

async def get_message_and_send_to_admins(message: Message, state: FSMContext):
    text = message.text
    await message.answer(
        text='Your message was sent to admins',
        reply_markup=inline.cancel_markup,
    )
    await state.finish()

async def send_message_to_admins(bot: Bot, text: str):
    config: Config = bot['config']
    for admin in config.tg_bot.admin_ids:
        await bot.send_message(
            chat_id=admin,
            text=text,
        )

def register_help_handlers(dp: Dispatcher):
    dp.register_message_handler(
        help_handler,
        commands=['help'],
    )
    dp.register_message_handler(
        get_message_and_send_to_admins,
        state='get_message_to_help',
    )