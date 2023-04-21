from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateImgStates(StatesGroup):
    text1 = State()
    text2 = State()
    text3 = State()
