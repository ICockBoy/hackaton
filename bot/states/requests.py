from aiogram.fsm.state import StatesGroup, State


class RequestsStates(StatesGroup):
    write_request = State()
