from aiogram.dispatcher.filters.state import StatesGroup, State


class GetGroup(StatesGroup):
    group = State()