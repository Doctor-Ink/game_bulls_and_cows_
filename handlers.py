from aiogram import types, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.filters import Command
from text import GREETINGS, HELP_TEXT


router = Router()

kb = [
    [
        KeyboardButton(text='Играть'),
        KeyboardButton(text='Помощь')
    ],
]
keyboard1 = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@router.message(Command("Играть"))
async def start_handler(msg: Message):
    await msg.answer(GREETINGS, reply_markup=keyboard1)


@router.message(Command("Играть"))
async def start_game(msg: Message):
    STARTED = False
    while True:
        if STARTED == False:
            print('BOT STARTED!')
            executor.start_pooling(dp)
            STARTED = True
        print('loop')


    await msg.answer(GREETINGS, reply_markup=keyboard1)


@router.message(Command("Помощь"))
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
