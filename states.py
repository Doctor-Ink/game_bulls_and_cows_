from aiogram.fsm.state import StatesGroup, State


class ClientState(StatesGroup):
    """Хранит на каком этапе диалога находится клиент"""
    BEGIN_BOT = State()
    START_GAME = State()
    IN_THE_GAME = State()
    FINISH_GAME = State()