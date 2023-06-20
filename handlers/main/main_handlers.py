import os

from aiogram import Dispatcher
from aiogram.types import Message

from handlers.activity.activity_functions import get_all_accounts_len
from handlers.activity.database import add_phone, get_admin, get_tasks
from handlers.main.main_functions import main_menu
from handlers.task.task_keyboard import task_index
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.instruments import logger


@logger.catch
async def help_command(message: Message):
    await message.answer(text=MESSAGES["faq"])


@logger.catch
async def start_command(message: Message):
    await main_menu(message, message_text=MESSAGES["start"].format(message.from_user))


@logger.catch
async def back_by_button(message: Message):
    await main_menu(message, message_text=MESSAGES["main_menu"])


@logger.catch
async def back_by_command(message: Message):
    await main_menu(message, message_text=MESSAGES["main_menu"])


@logger.catch
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


@logger.catch
async def task_button(message: Message):
    task_list = get_tasks()
    await task_index(message=message, task_list=task_list)


@logger.catch
def delete_journals_files():
    for _, _, sessions in os.walk("base"):
        for session in sessions:
            if session.endswith("journal"):
                try:
                    os.remove("base/" + session)
                    logger.info(f"Delete Journal File {session}")
                except Exception as e:
                    logger.error(f"Delete Journals Files Error: {e}")


@logger.catch
def refresh_phones():
    for _, _, sessions in os.walk("base"):
        for session in sessions:
            if not session.endswith("journal"):
                try:
                    # phone = session.split(".")[0]
                    add_phone(session)
                except Exception as e:
                    logger.error(f"Refresh Phones Error: {e}")


@logger.catch
async def refresh_command(message: Message):
    logger.info(f"Refresh Command")
    delete_journals_files()
    refresh_phones()


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=[COMMANDS["start"]])
    dp.register_message_handler(help_command, commands=[COMMANDS["help"]])
    dp.register_message_handler(back_by_button, text=[BUTTONS["back"]])
    dp.register_message_handler(back_by_command, commands=[COMMANDS["back"]])
    dp.register_message_handler(count_users_button, text=[BUTTONS["count_users"]])
    dp.register_message_handler(task_button, text=[BUTTONS["task"]])
    dp.register_message_handler(refresh_command, commands=[COMMANDS["refresh"]])
