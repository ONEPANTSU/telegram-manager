from aiogram.dispatcher.filters.state import State, StatesGroup


class SubscribeStates(StatesGroup):
    channel_link = State()
    number_of_accounts = State()
    delay = State()
