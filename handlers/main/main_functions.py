from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from texts.buttons import BUTTONS
from texts.messages import MESSAGES


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1)
    activity = KeyboardButton(BUTTONS["activity"])
    users = KeyboardButton(BUTTONS["users"])
    parse = KeyboardButton(BUTTONS["parse"])
    markup.add(
        activity,
        users,
        parse,
    )
    return markup


async def main_menu(message, message_text):
    await message.answer(
        text=message_text,
        reply_markup=get_main_keyboard(),
    )
