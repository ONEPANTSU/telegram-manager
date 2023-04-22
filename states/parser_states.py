from aiogram.dispatcher.filters.state import State, StatesGroup


class ParserStates(StatesGroup):
    link_channel = State()
