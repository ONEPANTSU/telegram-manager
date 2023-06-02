from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts.buttons import BUTTONS


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    activity = KeyboardButton(BUTTONS["activity"])
    users = KeyboardButton(BUTTONS["users"])
    task = KeyboardButton(BUTTONS["task"])
    count_users = KeyboardButton(BUTTONS["count_users"])

    markup.add(activity, users, task, count_users)
    return markup


async def main_menu(message, message_text):
    await message.answer(
        text=message_text,
        reply_markup=get_main_keyboard(),
    )
