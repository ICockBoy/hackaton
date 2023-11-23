from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    fio_send = State()
    apartment_send = State()
    floor_send = State()
    entrance_send = State()
    number_send = State()

