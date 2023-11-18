from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram.filters import Command
from config_reader import config
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ClientState(StatesGroup):
    '''Хранит на каком этапе диалога находится клиент'''
    START_ORDER = State()
    CITY_SELECTED = State()
    RESTAURANT_SELECTED = State()
    DISH_SELECTED = State()
    DRINK_SELECTED = State()
    PROCCESS_ORDER = State()


bot = Bot(token=config.bot_token.get_secret_value())

# storage = RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key')
# storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')
storage = MemoryStorage()
rt = Router()
dp = Dispatcher(storage=storage)
dp.include_router(rt)


@rt.message(Command('Go'))
async def start_proccess(message: types.Message, state: FSMContext) -> None:
    msg = '''Привет! 👋🤖 Я бот доставки еды! В каком ты городе?'''

    kb = [
        [
            KeyboardButton(text='Москва'),
            KeyboardButton(text='СПБ')
        ],
        [
            KeyboardButton(text='Воронеж'),
            KeyboardButton(text='Липецк')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(msg, reply_markup=keyboard)
    await state.set_state(ClientState.START_ORDER)


@rt.message(ClientState.START_ORDER)
async def choose_restoraunts_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(CITY=user_msg)

    kb = [
        [
            KeyboardButton(text='Китайский дракон'),
            KeyboardButton(text='PyLounge')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer('Выберите заведение', reply_markup=keyboard)
    await state.set_state(ClientState.CITY_SELECTED)


@rt.message(ClientState.CITY_SELECTED)
async def dish_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(RESTAURANT=user_msg)

    kb = [
        [
            KeyboardButton(text='Суп'),
            KeyboardButton(text='Не суп')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer('Выберите блюдо', reply_markup=keyboard)
    await state.set_state(ClientState.RESTAURANT_SELECTED)


@rt.message(ClientState.RESTAURANT_SELECTED)
async def drink_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(DISH=user_msg)

    kb = [
        [
            KeyboardButton(text='Кола'),
            KeyboardButton(text='Тоже кола но РУССКАЯ!')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer('Выберите напиток', reply_markup=keyboard)
    await state.set_state(ClientState.DISH_SELECTED)


@rt.message(ClientState.DISH_SELECTED)
async def order_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(DRINK=user_msg)

    kb = [
        [
            KeyboardButton(text='Оформить заказ'),
            KeyboardButton(text='Отмена')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer('Мы почти закончили', reply_markup=keyboard)
    await state.set_state(ClientState.DRINK_SELECTED)


@rt.message(ClientState.DRINK_SELECTED)
async def finish_process(message: types.Message, state: FSMContext):
    user_msg = message.text
    if user_msg == 'Оформить заказ':
        user_state_data = await state.get_data()
        city = user_state_data['CITY']
        rest = user_state_data['RESTAURANT']
        dish = user_state_data['DISH']
        drink = user_state_data['DRINK']
        msg = f'''Ваш заказ: {dish} {drink} из {rest} ({city}) ОФОРМЛЕН!!!'''
        await message.answer(msg)
    else:
        await message.answer('Пока(')
    await state.finish()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())