from aiogram.dispatcher.filters.state import State, StatesGroup


class SubscribeStates(StatesGroup):
    channel = State()
    text2 = State()
    text3 = State()
