from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "Эспрессо"), KeyboardButton(text = "Капучино"), KeyboardButton(text = "Ристретто"),
        ],
        [
            KeyboardButton(text = "Кофе Раф"), KeyboardButton(text = "Лавандовый Раф"), KeyboardButton(text = "Эйр "
                                                                                                           "Латте"),
        ],

    ]
)
