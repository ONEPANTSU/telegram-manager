from aiogram.dispatcher.filters.state import State, StatesGroup


class ViewerPostStates(StatesGroup):
    id_channel = State()
    id_post = State()
    number_of_post = State()
    number_of_accounts = State()
    ask = State()
    delay = State()
    delay_percent = State()
    confirm = State()
    percent_confirm = State()
