from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from handlers.activity.activity_handler import activity_keyboard
from handlers.main.main_functions import main_menu, get_main_keyboard
from handlers.users.users_handler import add_user_button
from states import ParserStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES

from useful.commands_handler import commands_handler
from useful.instruments import bot


async def parser_button(message: Message):
    await message.answer(text=MESSAGES["channel_link"])
    await ParserStates.link_channel.set()


async def parser_link_channel_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == BUTTONS["users"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["user"],
            reply_markup=get_main_keyboard(),
        )
        await add_user_button(message)
        await state.finish()
    elif answer == BUTTONS["activity"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["activity_menu"],
            reply_markup=activity_keyboard(),
        )
        await state.finish()
    elif answer == BUTTONS["parse"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["parser"],
            reply_markup=get_main_keyboard(),
        )
        await parser_button(message)
        await state.finish()
    else:
        await state.update_data(link_channel=answer)
        await state.finish()


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(parser_button, text=[BUTTONS["parse"]])
    dp.register_message_handler(parser_link_channel_state, state=ParserStates.link_channel)

