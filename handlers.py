from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from text import GREETINGS


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(GREETINGS)


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
