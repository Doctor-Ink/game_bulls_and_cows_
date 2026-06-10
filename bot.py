# python 3.12
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from kb import keyboard_start, keyboard_y_n
from text import GREETINGS, HELP_TEXT
from engine import get_digit, cow_bull
from log import log_user_info, logger

try:
    ############## SERVER #########################
    # Для веб сервера забираем переменную ТОКЕН
    TOKEN = os.environ['TG_TOKEN_BULL']
    ############## SERVER #########################

    ################ WEBHOOK #########################
    # Webserver settings
    # bind localhost only to prevent any external access
    WEB_SERVER_HOST = '::'
    # Port for incoming request from reverse proxy. Should be any available port
    WEB_SERVER_PORT = 8301

    # Path to webhook route, on which Telegram will send requests
    WEBHOOK_PATH = '/bot/'
    # Base URL for webhook will be used to generate webhook URL for Telegram,
    # in this example it is used public DNS with HTTPS support
    BASE_WEBHOOK_URL = 'https://doctorink.alwaysdata.net/bullsandcows/'
    ################ WEBHOOK #########################
    # SERVER
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
except:
    from config_reader import config
    # Локальная версия
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


storage = MemoryStorage()
dp = Dispatcher(storage=storage)
rt = Router()
dp.include_router(rt)


@rt.message(Command("start"))
async def start_bot(message: Message):
    log_user_info(message, "START")
    await message.answer(GREETINGS, reply_markup=keyboard_start)


@rt.message(F.text.lower() == "помощь")
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)


@rt.message(F.text.lower().in_({'играть', 'да'}))
async def start_game(msg: Message, state: FSMContext):
    log_user_info(msg, "GAME_START")
    await state.update_data(NUMBER=get_digit())
    await state.update_data(ATTEMPT=0)
    await msg.answer(
        f"------ Компьютер загадал четырёхзначное число!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await msg.answer("Введите ваше предположение (4 разные цифры):")


@rt.message(F.text.lower() == "нет")
async def no_handler(msg: Message):
    await msg.answer('Удачи...')


@rt.message()
async def reply_builder(message: types.Message, state: FSMContext,):
    # Получаем данные состояния
    current_digits = await state.get_data()

    # Проверяем, начата ли игра
    if not current_digits or 'NUMBER' not in current_digits:
        await message.answer("Сначала начните игру командой 'Играть'")
        return

    number = current_digits['NUMBER']
    attempt = current_digits['ATTEMPT']

    # ==========  ПРОВЕРКА НА None ==========
    if message.text is None:
        await message.answer("Пожалуйста, отправьте число текстом (не фото и не стикер)")
        return

    if message.text == number:
        # Логируем победу
        log_user_info(message, "WIN", f"Попыток: {attempt + 1}")
        await message.reply(f"🎉 Вы угадали! Количество ходов - {attempt + 1}")
        await message.answer("Хотите сыграть ещё раз?", reply_markup=keyboard_y_n)
        await state.clear()  # Очищаем состояние после игры
    elif message.text.isdigit() and len(message.text) == len(set(message.text)) == 4:
        # Увеличиваем счётчик попыток ТОЛЬКО при корректном вводе
        await state.update_data(ATTEMPT=attempt + 1)
        bull, cow = cow_bull(cur_num=message.text, res_number=number)
        # Логируем ход
        logger.info(
            f"Пользователь {message.from_user.id}: ход {attempt + 1} = {message.text} (быки:{bull} коровы:{cow})"
        )
        await message.answer(f'№{attempt + 1} - быки - {bull}, коровы - {cow}')
    else:
        # Логируем некорректный ввод
        logger.warning(f"Некорректный ввод от {message.from_user.id}: '{message.text}'")
        await message.answer(
            "❌ Некорректный ввод!\n"
            "Введите четырёхзначное число с 4 разными цифрами\n"
            "Например: 1234"
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())






