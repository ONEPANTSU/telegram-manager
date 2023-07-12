import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from telethon import TelegramClient

from config import *
from handlers.activity.database import add_phone, get_admin
from handlers.main.main_functions import get_main_keyboard
from handlers.users.ftp_connection import send_file_to_servers
from states import AddUserStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.callbacks import yes_no_callback
from useful.commands_handler import commands_handler
from useful.instruments import bot, clients, code, logger
from useful.keyboards import activity_keyboard, ask_keyboard


@logger.catch
async def not_command_checker(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
        return False
    elif answer == BUTTONS["users"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["user"],
            reply_markup=get_main_keyboard(),
        )
        await add_user_button(message)
        await state.finish()
        return False
    elif answer == BUTTONS["activity"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["activity_menu"],
            reply_markup=activity_keyboard(),
        )
        await state.finish()
        return False
    else:
        return True


@logger.catch
async def add_user_button(message: Message):
    admin_list = get_admin()
    admin = message.from_user.username
    if admin in admin_list:
        await message.answer(text=MESSAGES["user_phone"])
        await AddUserStates.phone.set()
    else:
        await message.answer(text=MESSAGES["access"], reply_markup=None)


@logger.catch
async def phone_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        phone = "+{}".join(filter(str.isdigit, message.text))
        await state.update_data(phone=phone)
        await message.answer(
            text=MESSAGES["user_ask"], reply_markup=ask_keyboard(phone)
        )
        await state.finish()


@logger.catch
async def ask_state(query: CallbackQuery, callback_data: dict, state: FSMContext):
    if await not_command_checker(message=query.message, state=state):
        answer = callback_data["answer"]
        phone = callback_data["phone"]

        await state.update_data(phone=phone)
        await state.update_data(is_password=answer)
        if answer == BUTTONS["yes"]:
            await query.message.edit_text(
                text=MESSAGES["user_password"], reply_markup=None
            )
            await AddUserStates.password.set()
        elif answer == BUTTONS["no"]:
            await query.message.answer(text=MESSAGES["user_sms"])
            await connect(state=state, phone=phone)


@logger.catch
async def password_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        password = message.text
        await state.update_data(password=password)
        phone = (await state.get_data())["phone"]
        await message.answer(text=MESSAGES["user_sms"])
        await connect(phone=phone, password=password, state=state)


async def connect(state, phone, password=None):
    client = TelegramClient(f"base/{phone}", API_ID, API_HASH)
    await client.connect()
    if password is not None:
        await client.start(phone=phone, password=password, state=state)
    else:
        await client.start(phone=phone, state=state)


@logger.catch
async def sms_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        phone = (await state.get_data())["phone"]
        code[phone] = message.text
        is_password = (await state.get_data())["is_password"]
        if is_password == BUTTONS["yes"]:
            password = (await state.get_data())["password"]
            await clients[phone]._start(
                phone=phone,
                password=password,
                code_callback=code[phone],
                message=message,
            )
        else:
            await clients[phone]._start(
                phone=phone, code_callback=code[phone], message=message
            )

        for _, _, sessions in os.walk("base"):
            for session in sessions:
                if not session.endswith("journal") and phone in session:
                    try:
                        add_phone(session)
                        file_path = f"base/{session}"
                        send_file_to_servers(file_path=file_path)
                        break
                    except Exception as e:
                        logger.error(f"Refresh Phones Error: {e}")

        await message.answer(
            text="Авторизация прошла успешно.", reply_markup=get_main_keyboard()
        )
        await state.finish()


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(add_user_button, text=[BUTTONS["users"]])
    dp.register_message_handler(phone_state, state=AddUserStates.phone)
    dp.register_message_handler(password_state, state=AddUserStates.password)
    dp.register_message_handler(sms_state, state=AddUserStates.sms)
    dp.register_callback_query_handler(ask_state, yes_no_callback.filter())
