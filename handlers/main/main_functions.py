from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts.buttons import BUTTONS
from texts.messages import MESSAGES


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    create_post = KeyboardButton(BUTTONS["create_post"])
    markup.add(
        create_post,
    )
    return markup


async def main_menu(message, message_text):
    await message.answer(
        text=message_text,
        reply_markup=get_main_keyboard(),
    )
