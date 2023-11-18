from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.filters import Command
from text import GREETINGS, HELP_TEXT
from engine import get_digit
from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging


class ClientState(StatesGroup):
    """Хранит на каком этапе диалога находится клиент"""
    BEGIN_BOT = State()
    START_GAME = State()
    IN_THE_GAME = State()
    FINISH_GAME = State()


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
storage = MemoryStorage()
rt = Router()
dp = Dispatcher(storage=storage)
dp.include_router(rt)


@rt.message(Command("start"))
async def start_bot(message: Message, state: FSMContext):
    kb = [
        [
            KeyboardButton(text='Играть'),
            KeyboardButton(text='Помощь')
        ],
    ]
    keyboard1 = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(GREETINGS, reply_markup=keyboard1)
    await state.set_state(ClientState.BEGIN_BOT)


@rt.message(F.text.lower() == "помощь")
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)


@rt.message(F.text.lower() == "играть")
@rt.message(F.text.lower() == "да")
async def start_game(msg: Message, state: FSMContext):
    number = get_digit()
    attempt = 0
    await state.update_data(NUMBER=number)
    await state.update_data(ATTEMPT=attempt)
    await msg.answer(
        f"------Компьютер загадал число - {len(str(number)) * '*'}",
        reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ClientState.START_GAME)


@rt.message(F.text.lower() == "нет")
async def help_handler(msg: Message):
    await msg.answer('Пидор ответ!')


@rt.message(ClientState.START_GAME)
async def reply_builder(message: types.Message, state: FSMContext,):
    current_digit = await state.get_data()
    number = current_digit['NUMBER']
    attempt = current_digit['ATTEMPT']
    attempt += 1
    await message.answer("Введите четырёхзначное число с неповторяющимися цифрами - ")
    if message.text == number:
        kb = [
            [
                KeyboardButton(text='Да'),
                KeyboardButton(text='Нет')
            ],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.answer(f"Вы угадали !!! Количество ходов - {attempt}")
        await message.answer("Хотите сыграть ещё раз?", reply_markup=keyboard)
    elif message.text.isdigit() and len(message.text) == 4 and len(message.text) == len(set(message.text)):
        cow = 0
        bull = 0
        await state.update_data(ATTEMPT=attempt)
        for i in message.text:
            if i in number and message.text.index(i) == number.index(i):
                bull += 1
            elif i in number:
                cow += 1
        await message.answer(f'№{attempt} - быки - {bull}, коровы - {cow}')
    else:
        await state.update_data(ATTEMPT=attempt)
        await message.answer("Некорректный ввод")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

