from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.utils import markdown

from tgbot.config import Config
from tgbot.keyboards import inline
from tgbot.misc import schemas
from tgbot.services import db


async def support_handler(message: Message):
    new_message = await message.answer(
        text='Sending support request...',
    )
    support_request: schemas.SupportRequest = await db.add_support_request(
        user_telegram_id=message.from_user.id,
    )
    await send_requests_to_admins(
        bot=message.bot,
        text=(
            'New support request from user '
            f'{markdown.hbold(message.from_user.full_name)} '
            'with id '
            f'{markdown.hcode(message.from_user.id)} \n'
            f'request id: {markdown.hcode(support_request.id)} \n'
        ),
        support_request=support_request,
    )
    new_message = await new_message.edit_text(
        text='Your support request was sent to admins',
    )

async def send_requests_to_admins(
    bot: Bot,
    text: str,
    support_request: schemas.SupportRequest
    ):
    config: Config = bot['config']
    for admin in config.tg_bot.admin_ids:
        await bot.send_message(
            chat_id=admin,
            text=text,
            reply_markup=inline.confirm_support_request_markup(
                support_request_id=support_request.id,
            ),    
        )

async def confirm_support_request_handler(
    call: CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
    dp: Dispatcher,
    ):
    await call.answer()
    await call.message.edit_text(
        text=call.message.text + '\nConfirmed',
    )
    support_request = await get_support_requests(callback_data)
    await db.delete_support_request(int(callback_data['id']))
    # inviter - хто запитував підтримку
    # invitee - хто підтвердив запит
    await set_state_to_support_dialog(
        dp=dp,
        inviter_telegram_id=support_request.user_id,
        invitee_telegram_id=call.from_user.id,
    )
    await call.bot.send_message(
        chat_id=support_request.user_id,
        text=(
            'Dialog with support started\n'
            'You can send messages to support\n'
            'To stop dialog send /stop'
        )
    )
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=(
            'Dialog with user started\n'
            'You can send messages to user\n'
            'To stop dialog send /stop'
        )
    )

async def set_state_to_support_dialog(
    dp: Dispatcher, 
    inviter_telegram_id: int,
    invitee_telegram_id: int,
    ):
    inviter_state = dp.current_state(
        user=inviter_telegram_id,
        chat=inviter_telegram_id,
    )
    await inviter_state.set_state('support_dialog')
    await inviter_state.update_data(
        invitee_telegram_id=invitee_telegram_id,
        inviter_telegram_id=inviter_telegram_id,
    )
    invitee_state = dp.current_state(
        user=invitee_telegram_id,
        chat=invitee_telegram_id,
    )
    await invitee_state.set_state('support_dialog')
    await invitee_state.update_data(
        inviter_telegram_id=inviter_telegram_id,
        invitee_telegram_id=invitee_telegram_id,
    )
 
async def forward_messages(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if message.from_user.id == state_data['inviter_telegram_id']:
        companion_id = state_data['invitee_telegram_id']
    else:
        companion_id = state_data['inviter_telegram_id']
    await message.copy_to(chat_id=companion_id)


async def get_support_requests(callback_data: dict) -> schemas.SupportRequest:
    support_request_id = int(callback_data['id'])
    support_request: schemas.SupportRequest = await db.get_support_request(
        id=support_request_id,
    )
    return support_request

async def stop_dialog_state_between_inviter_and_invitee(
    dp: Dispatcher,
    invitee_telegram_id: int,
    inviter_telegram_id: int,
    ):
    for telegram_id in (invitee_telegram_id, inviter_telegram_id):
        state = dp.current_state(
            user=telegram_id,
            chat=telegram_id,
        )
        await state.reset_state()

async def stop_support_dialog_handler(
    message: Message,
    dp: Dispatcher,
    state: FSMContext,
    ):
    state_data = await state.get_data()
    await stop_dialog_state_between_inviter_and_invitee(
        dp=dp,
        invitee_telegram_id=state_data['invitee_telegram_id'],
        inviter_telegram_id=state_data['inviter_telegram_id'],
    )
    if message.from_user.id == state_data['inviter_telegram_id']:
        text_to_user = 'You stopped dialog with support'
        text_to_support = 'User stopped dialog with support'

    else:
        text_to_support = 'You stopped dialog with user'
        text_to_user = 'Support stopped dialog with you'
    await message.bot.send_message(
        chat_id=state_data['invitee_telegram_id'],
        text=text_to_support,
    )
    await message.bot.send_message(
        chat_id=state_data['inviter_telegram_id'],
        text=text_to_user,
    )


def register_support_handlers(dp: Dispatcher):
    dp.register_message_handler(
        support_handler,
        commands=['support'],
    )
    dp.register_callback_query_handler(
        confirm_support_request_handler,
        inline.confirm_support_request_callback.filter(),
    )
    dp.register_message_handler(
        stop_support_dialog_handler,
        state='support_dialog',
        commands=['stop'],
    )
    dp.register_message_handler(
        forward_messages,
        state='support_dialog',
        content_types=ContentType.ANY,
    )