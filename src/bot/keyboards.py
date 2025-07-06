from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ИИ")],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Майка", callback_data="t-shirt"),
            InlineKeyboardButton(text="Кепка", callback_data="Cap"),
        ]
    ]
)


type_mess = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Линейный'),
        KeyboardButton(text='Перемешанный')
    ]
    ],resize_keyboard=True, one_time_keyboard=True)
