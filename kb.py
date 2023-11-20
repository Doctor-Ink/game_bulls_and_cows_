from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

kb1 = [
    [
        KeyboardButton(text='Играть'),
        KeyboardButton(text='Помощь')
    ],
]
keyboard_start = ReplyKeyboardMarkup(keyboard=kb1, resize_keyboard=True)

kb2 = [
    [
        KeyboardButton(text='Да'),
        KeyboardButton(text='Нет')
    ],
]
keyboard_y_n = ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)