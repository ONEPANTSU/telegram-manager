from aiogram.dispatcher.filters.state import State, StatesGroup


class AddUserStates(StatesGroup):
    phone = State()
    sms = State()
    password = State()
    ask = State()
