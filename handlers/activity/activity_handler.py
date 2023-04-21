from aiogram import Dispatcher
from aiogram.types import Message

from handlers.main.main_functions import main_menu
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES


async def chose_activity(message: Message):
    await message.reply(text="Hello")
    await main_menu(message, message_text=MESSAGES["start"].format(message.from_user))


def register_activity_handlers(dp: Dispatcher):
    dp.register_message_handler(chose_activity, text=[BUTTONS["activity"]])
