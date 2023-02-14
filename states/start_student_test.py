from aiogram.dispatcher.filters.state import StatesGroup, State


class StartTesting(StatesGroup):
    test = State()