from aiogram.types.inline_keyboard import InlineKeyboardMarkup, \
    InlineKeyboardButton

cancel_button = InlineKeyboardButton(
    text='Cancel',
    callback_data='cancel',
)
cancel_markup = InlineKeyboardMarkup().add(cancel_button)
