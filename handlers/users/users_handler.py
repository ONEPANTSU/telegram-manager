from aiogram import Dispatcher
from aiogram.types import Message

from handlers.main.main_functions import main_menu
from states import AddUserStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from config import *
from time import localtime
from telethon import TelegramClient


async def add_user_button(message: Message):
    await message.answer(text=MESSAGES["user_phone"])

async def phone_state(message: Message):
    phone = message.text
    if phone:
        client = TelegramClient(f'base/{phone}', API_ID, API_HASH)
        client.start(phone=phone)
    await message.answer(text="Введите номер телеофна 📞")

def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(add_user_button, text=[BUTTONS["users"]])
    dp.register_message_handler(phone_state, state=AddUserStates.phone)