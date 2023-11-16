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
async def start_handler(message: Message):
    kb = [
        [
            KeyboardButton(text='Играть'),
            KeyboardButton(text='Помощь')
        ],
    ]
    keyboard1 = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(GREETINGS, reply_markup=keyboard1)


@rt.message(F.text.lower() == "Помощь")
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)


@rt.message(Command("Играть"))
async def start_game(msg: Message, state: FSMContext):
    number = get_digit()
    await msg.answer(f'------Компьютер загадал число - {number}')
    await state.set_state(ClientState.START_GAME)


# @dp.message(state=ClientState.START_GAME)
# async def start_game(msg: Message, state: FSMContext):
#     await msg.answer('Введите четырёхзначное число с неповторяющимися цифрами')
#     await state.set_state(ClientState.IN_THE_GAME)


# @dp.message()
# async def number_selection(msg: types.Message):
#     cow = 0
#     bull = 0
#     cur_num = msg.text
#     print(cur_num)
#     # for i in F.text.lower():
#     #     if i in number and F.text.lower().index(i) == number.index(i):
#     #         bull += 1
#     #     elif i in number:
#     #         cow += 1
#     print(f'')
#     await msg.answer(f'> быки - {bull}, коровы - {cow}', reply_markup=keyboard1)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

