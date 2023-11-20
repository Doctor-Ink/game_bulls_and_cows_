from aiogram import types, F, Router, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from kb import keyboard_start, keyboard_y_n
from text import GREETINGS, HELP_TEXT
from engine import get_digit, cow_bull
from config_reader import config
import asyncio
import logging


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
storage = MemoryStorage()
rt = Router()
dp = Dispatcher(storage=storage)
dp.include_router(rt)


@rt.message(Command("start"))
@rt.message(F.text.lower() == "нет")
async def start_bot(message: Message):
    await message.answer(GREETINGS, reply_markup=keyboard_start)


@rt.message(F.text.lower() == "помощь")
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)


@rt.message(F.text.lower().in_({'играть', 'да'}))
async def start_game(msg: Message, state: FSMContext):
    await state.update_data(NUMBER=get_digit())
    await state.update_data(ATTEMPT=0)
    await msg.answer(
        f"------Компьютер загадал число - **** ",
        reply_markup=types.ReplyKeyboardRemove())


@rt.message(F.text.lower() == "нет")
async def help_handler(msg: Message):
    await msg.answer('Удачи...')


@rt.message()
async def reply_builder(message: types.Message, state: FSMContext,):
    current_digits = await state.get_data()
    number = current_digits['NUMBER']
    attempt = current_digits['ATTEMPT']
    await state.update_data(ATTEMPT=attempt + 1)
    await message.answer("Введите четырёхзначное число с неповторяющимися цифрами - ")
    if message.text == number:
        await message.reply(f"Вы угадали !!! Количество ходов - {attempt}")
        await message.answer("Хотите сыграть ещё раз?", reply_markup=keyboard_y_n)
    elif message.text.isdigit() and len(message.text) == 4 and len(message.text) == len(set(message.text)):
        bull, cow = cow_bull(cur_num=message.text, res_number=number)
        await message.answer(f'№{attempt + 1} - быки - {bull}, коровы - {cow}')
    else:
        await message.answer("Некорректный ввод")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

