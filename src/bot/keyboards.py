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

ai_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Мировые кухни'),
        KeyboardButton(text='Выбор блюд')
    ]
    ],resize_keyboard=True, one_time_keyboard=True)


type_mess = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Линейный'),
        KeyboardButton(text='Перемешанный')
    ]
    ],resize_keyboard=True, one_time_keyboard=True)
