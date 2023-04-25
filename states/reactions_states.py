from aiogram.dispatcher.filters.state import State, StatesGroup


class ReactionsStates(StatesGroup):
    id_channel = State()
    id_post = State()
    number_of_button = State()
    number_of_accounts = State()
    ask = State()
    delay = State()
    delay_percent = State()
