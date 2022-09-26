from aiogram.utils.callback_data import CallbackData
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, \
    InlineKeyboardButton

cancel_button = InlineKeyboardButton(
    text='Cancel',
    callback_data='cancel',
)
cancel_markup = InlineKeyboardMarkup().add(cancel_button)

confirm_support_request_callback = CallbackData('confirm_support_request', 'id')
def confirm_support_request_markup(
    support_request_id: int
    ) -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Confirm',
                    callback_data=confirm_support_request_callback.new(
                        id=support_request_id,
                    )
                )
            ]
        ]
    )