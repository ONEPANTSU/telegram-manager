from aiogram.types import ReplyKeyboardRemove

from handlers.main.main_functions import main_menu
from texts.commands import COMMANDS
from texts.messages import MESSAGES


async def commands_handler(message):
    answer = message.text.lstrip("/")
    if answer == COMMANDS["start"]:
        await main_menu(
            message,
            message_text=MESSAGES["start"].format(
                message.from_user, reply_markup=ReplyKeyboardRemove()
            ),
        )

    elif answer == COMMANDS["back"]:
        await main_menu(message, message_text=MESSAGES["main_menu"])
