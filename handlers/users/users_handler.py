from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from handlers.main.main_functions import main_menu
from states import AddUserStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from config import *
from time import localtime
from telethon import TelegramClient

from useful.commands_handler import commands_handler


async def add_user_button(message: Message):
    await message.answer(text=MESSAGES["user_phone"])
    await AddUserStates.phone.set()


async def phone_state(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    if phone:
        client = TelegramClient(f'base/{phone}', API_ID, API_HASH)
        client.start(phone=phone)
    await message.answer(text=MESSAGES["user_password"])
    await AddUserStates.password.set()


async def password_state(message: Message, state: FSMContext):
    password = message.text
    await state.update_data(password=password)
    phone = message.text
    if phone:
        client = TelegramClient(f'base/{phone}', API_ID, API_HASH)
        client.start(phone=phone)
    await message.answer(text=MESSAGES["user_sms"])
    await AddUserStates.sms.set()


async def sms_state(message: Message, state: FSMContext):
    sms = message.text
    await state.update_data(sms=sms)
    if phone:
        client = TelegramClient(f'base/{phone}', API_ID, API_HASH)
        client.start(phone=phone)
    await message.answer(text=MESSAGES["user_password"])
    await state.finish()


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(add_user_button, text=[BUTTONS["users"]])
    dp.register_message_handler(phone_state, state=AddUserStates.phone)
    dp.register_message_handler(password_state, state=AddUserStates.password)
    dp.register_message_handler(sms_state, state=AddUserStates.sms)
