from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    request_admin = State()
