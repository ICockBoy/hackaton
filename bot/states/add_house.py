from aiogram.fsm.state import StatesGroup, State


class AddHouseStates(StatesGroup):
    write_house_name = State()
    get_users_group = State()
    get_moderate_group = State()
