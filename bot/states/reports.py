from aiogram.fsm.state import StatesGroup, State


class ReportsStates(StatesGroup):
    write_problem = State()
