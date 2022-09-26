from aiogram.dispatcher import Dispatcher
from aiogram.types import Update

from tgbot.misc.exceptions import *
from web.app import models


async def support_confirmed_by_other(
    update: Update,
    exception: models.SupportRequest.DoesNotExist,
    ) -> bool:
    await update.message.answer(
        text='This request was already confirmed by another',
    )
    return True
    

def register_error_handlers(dp: Dispatcher):
    dp.register_errors_handler(
        callback=support_confirmed_by_other,
        exception=models.SupportRequest.DoesNotExist,
    )
    