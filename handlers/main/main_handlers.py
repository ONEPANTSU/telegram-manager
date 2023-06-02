from aiogram import Dispatcher
from aiogram.types import Message

from handlers.activity.activity_functions import (
    delete_journals_files,
    get_all_accounts_len,
)
from handlers.activity.database import get_admin
from handlers.main.main_functions import main_menu
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES


async def help_command(message: Message):
    await message.answer(text=MESSAGES["faq"])


async def start_command(message: Message):
    await main_menu(message, message_text=MESSAGES["start"].format(message.from_user))


async def back_by_button(message: Message):
    await main_menu(message, message_text=MESSAGES["main_menu"])


async def back_by_command(message: Message):
    await main_menu(message, message_text=MESSAGES["main_menu"])


async def count_users_button(message: Message):
    admin_list = get_admin()
    admin = message.from_user.username
    if admin in admin_list:
        accounts_len = await get_all_accounts_len()
        await message.answer(
            text=MESSAGES["available_bot"].format(count_user=accounts_len)
        )
    else:
        await message.answer(text=MESSAGES["access"], reply_markup=None)


async def task_button(message: Message):
    delete_journals_files()
    await message.answer(text=MESSAGES["clear_journals"])


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=[COMMANDS["start"]])
    dp.register_message_handler(help_command, commands=[COMMANDS["help"]])
    dp.register_message_handler(back_by_button, text=[BUTTONS["back"]])
    dp.register_message_handler(back_by_command, commands=[COMMANDS["back"]])
    dp.register_message_handler(count_users_button, text=[BUTTONS["count_users"]])
    dp.register_message_handler(task_button, text=[BUTTONS["task"]])
