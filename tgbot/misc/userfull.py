import asyncio

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation


async def mailing(
    dp: Dispatcher,
    users_ids: list[int],
    message: Message,
) -> dict:
    bot = dp.bot
    result: dict = dict(
        success=[],
        failed=[],
    )
    while users_ids:
        await asyncio.sleep(0.5)
        user_id = users_ids.pop()
        user_state = dp.current_state(user=user_id, chat=user_id)
        if await user_state.get_state() is not None:
            continue
        try:
            await bot.copy_message(
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                chat_id=user_id,
            )
        except (CantInitiateConversation, BotBlocked):
            result['failed'].append(user_id)
            continue
        result['success'].append(user_id)
    return result
