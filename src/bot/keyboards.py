from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог"), KeyboardButton(text="Корзина")],
        [KeyboardButton(text="ИИ"), KeyboardButton(text="О нас")],
    ],
    resize_keyboard=True,
)

catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Майка", callback_data="t-shirt"),
            InlineKeyboardButton(text="Кепка", callback_data="Cap"),
        ]
    ]
)


number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Отправить номер",
                request_contact=True,
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        ]
    ]
)
