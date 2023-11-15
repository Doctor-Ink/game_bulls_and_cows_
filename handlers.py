from aiogram import types, F
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
dp = Dispatcher(storage=storage)


kb = [
    [
        KeyboardButton(text='Играть'),
        KeyboardButton(text='Помощь')
    ],
]
keyboard1 = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer(GREETINGS, reply_markup=keyboard1)
    await state.set_state(ClientState.BEGIN_BOT)


@dp.message(Command("Играть"))
async def start_game(msg: Message, state: FSMContext):
    number = get_digit()
    await msg.answer(f'------Компьютер загадал число - {number}', reply_markup=keyboard1)


@dp.message()
async def number_selection(msg: types.Message):
    cow = 0
    bull = 0
    cur_num = msg.text
    print(cur_num)
    # for i in F.text.lower():
    #     if i in number and F.text.lower().index(i) == number.index(i):
    #         bull += 1
    #     elif i in number:
    #         cow += 1
    print(f'')
    await msg.answer(f'> быки - {bull}, коровы - {cow}', reply_markup=keyboard1)


@dp.message(F.text.lower() == "помощь")
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

