from aiogram.dispatcher.filters.state import State, StatesGroup


class UnsubscribeStates(StatesGroup):
    channel_link = State()
    number_of_accounts = State()
    ask = State()
    delay = State()
