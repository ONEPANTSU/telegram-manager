from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)
from aiogram.utils.callback_data import CallbackData

from handlers.activity.activity_functions import *
from handlers.main.main_functions import get_main_keyboard
from handlers.users.users_handler import add_user_button
from states import ReactionsStates, SubscribeStates, UnsubscribeStates, ViewerPostStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot

subscribe_callback = CallbackData("subscribe_public_button", "is_public")
unsubscribe_callback = CallbackData("unsubscribe_public_button", "is_public")
unsubscribe_all_callback = CallbackData("unsubscribe_all_button")
viewer_post_callback = CallbackData("viewer_post_button")
reactions_callback = CallbackData("reactions_button")


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


def activity_keyboard():
    subscribe_public_button = InlineKeyboardButton(
        text=BUTTONS["subscribe_public"],
        callback_data=subscribe_callback.new(is_public=True),
    )
    subscribe_private_button = InlineKeyboardButton(
        text=BUTTONS["subscribe_private"],
        callback_data=subscribe_callback.new(is_public=False),
    )
    unsubscribe_public_button = InlineKeyboardButton(
        text=BUTTONS["unsubscribe_public"],
        callback_data=unsubscribe_callback.new(is_public=True),
    )
    unsubscribe_private_button = InlineKeyboardButton(
        text=BUTTONS["unsubscribe_private"],
        callback_data=unsubscribe_callback.new(is_public=False),
    )
    view_button = InlineKeyboardButton(
        text=BUTTONS["view"], callback_data=viewer_post_callback.new()
    )
    react_button = InlineKeyboardButton(
        text=BUTTONS["react"], callback_data=reactions_callback.new()
    )
    unsubscribe_all_button = InlineKeyboardButton(
        text=BUTTONS["unsubscribe_all"], callback_data=unsubscribe_all_callback.new()
    )
    act_keyboard = InlineKeyboardMarkup(row_width=1).add(
        subscribe_public_button,
        subscribe_private_button,
        unsubscribe_public_button,
        unsubscribe_private_button,
        unsubscribe_all_button,
        view_button,
        react_button,
    )
    return act_keyboard


async def chose_activity(message: Message):
    await message.answer(
        text=MESSAGES["chose_activity"], reply_markup=activity_keyboard()
    )


"""
SUBSCRIBE PUBLIC CHANNEL STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def subscribe_query(query: CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.edit_text(text=MESSAGES["channel_link"], reply_markup=None)
    is_public = callback_data.get("is_public")
    await state.update_data(is_public=is_public)
    await SubscribeStates.channel_link.set()


async def subscribe_channel_link_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        await state.update_data(channel_link=answer)
        await message.answer(text=MESSAGES["number_of_accounts"])
        await SubscribeStates.number_of_accounts.set()


async def subscribe_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await SubscribeStates.number_of_accounts.set()
        else:
            await state.update_data(count=int(answer))
            await message.answer(text=MESSAGES["delay"])
            await SubscribeStates.delay.set()


async def subscribe_delay_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await SubscribeStates.delay.set()
        else:
            await state.update_data(delay=int(answer))
            data = await state.get_data()
            is_public = data["is_public"] == "True"
            if is_public:
                await subscribe_public_channel(
                    channel_link=data["channel_link"],
                    count=data["count"],
                    delay=data["delay"],
                )
            else:
                await subscribe_private_channel(
                    channel_link=data["channel_link"],
                    count=data["count"],
                    delay=data["delay"],
                )
            await message.answer(text=MESSAGES["subscribe"])
            await state.finish()


"""
 UNSUBSCRIBE PUBLIC CHANNEL STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def unsubscribe_query(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    await query.message.answer(text=MESSAGES["channel_link"])
    is_public = callback_data.get("is_public")
    await state.update_data(is_public=is_public)
    await UnsubscribeStates.channel_link.set()


async def unsubscribe_channel_link_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        await state.update_data(channel_link=answer)
        await message.answer(text=MESSAGES["number_of_accounts"])
        await UnsubscribeStates.number_of_accounts.set()


async def unsubscribe_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await UnsubscribeStates.number_of_accounts.set()
        else:
            await state.update_data(count=int(answer))
            await message.answer(text=MESSAGES["delay"])
            await UnsubscribeStates.delay.set()


async def unsubscribe_delay_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await UnsubscribeStates.delay.set()
        else:
            await state.update_data(delay=int(answer))
            data = await state.get_data()
            is_public = data["is_public"] == "True"
            if is_public:
                await leave_public_channel(
                    channel_link=data["channel_link"],
                    count=data["count"],
                    delay=data["delay"],
                )
            else:
                await leave_private_channel(
                    channel_link=data["channel_link"],
                    count=data["count"],
                    delay=data["delay"],
                )
            await message.answer(text=MESSAGES["unsubscribe"])
            await state.finish()


# выбор приватный или неприватный канал


"""
  UNSUBSCRIBE ALL CHANNELS STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def unsubscribe_all_query():
    pass


"""
       POST VIEWERS STATES⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def viewer_post_button(query: CallbackQuery):
    await query.message.answer(text=MESSAGES["channel_link"])
    await ViewerPostStates.id_channel.set()


async def viewer_id_channel_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        await state.update_data(channel_link=answer)
        await message.answer(text=MESSAGES["id_post"])
        await ViewerPostStates.id_post.set()


async def viewer_id_post_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.id_post.set()
        else:
            await state.update_data(last_post_id=int(answer))
            await message.answer(text=MESSAGES["number_of_post"])
            await ViewerPostStates.number_of_post.set()


async def number_of_post_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.number_of_post.set()
        else:
            await state.update_data(count_posts=int(answer))
            await message.answer(text=MESSAGES["number_of_accounts"])
            await ViewerPostStates.number_of_accounts.set()


async def viewer_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.number_of_accounts.set()
        else:
            await state.update_data(count_accounts=int(answer))
            await message.answer(text=MESSAGES["delay"])
            await ViewerPostStates.delay.set()


async def viewer_delay_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.delay.set()
        else:
            await state.update_data(delay=int(answer))
            data = await state.get_data()
            await view_post(
                data["channel_link"],
                data["last_post_id"],
                data["count_posts"],
                data["count_accounts"],
                data["delay"],
            )
            await message.answer(text=MESSAGES["viewer_post"])
            await state.finish()


"""
        REACTIONS STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def reactions_query(query: CallbackQuery):
    await query.message.answer(text=MESSAGES["id_channel"])
    await ReactionsStates.id_channel.set()


async def reactions_id_channel_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.id_channel.set()
        else:
            await state.update_data(id_channel=answer)
            await message.answer(text=MESSAGES["id_post"])
            await ReactionsStates.id_post.set()


async def reactions_id_post_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.id_post.set()
        else:
            await state.update_data(id_post=answer)
            await message.answer(text=MESSAGES["number_of_button"])
            await ReactionsStates.number_of_button.set()


async def number_of_button_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.number_of_button.set()
        else:
            await state.update_data(number_of_button=answer)
            await message.answer(text=MESSAGES["number_of_accounts"])
            await ReactionsStates.number_of_accounts.set()


async def reactions_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.number_of_accounts.set()
        else:
            await state.update_data(number_of_accounts=answer)
            await message.answer(text=MESSAGES["delay"])
            await ReactionsStates.delay.set()


async def reactions_delay_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.delay.set()
        else:
            await state.update_data(delay=answer)
            await message.answer(text=MESSAGES["reactions"])
            await state.finish()


def register_activity_handlers(dp: Dispatcher):
    dp.register_message_handler(chose_activity, text=[BUTTONS["activity"]])
    dp.register_callback_query_handler(subscribe_query, subscribe_callback.filter())
    dp.register_callback_query_handler(unsubscribe_query, unsubscribe_callback.filter())
    dp.register_callback_query_handler(
        viewer_post_button, viewer_post_callback.filter()
    )
    dp.register_callback_query_handler(reactions_query, reactions_callback.filter())
    dp.register_callback_query_handler(
        chose_activity, unsubscribe_all_callback.filter()
    )
    dp.register_message_handler(
        subscribe_channel_link_state, state=SubscribeStates.channel_link
    )
    dp.register_message_handler(
        subscribe_number_of_accounts_state, state=SubscribeStates.number_of_accounts
    )
    dp.register_message_handler(subscribe_delay_state, state=SubscribeStates.delay)
    dp.register_message_handler(
        unsubscribe_channel_link_state, state=UnsubscribeStates.channel_link
    )
    dp.register_message_handler(
        unsubscribe_number_of_accounts_state, state=UnsubscribeStates.number_of_accounts
    )
    dp.register_message_handler(unsubscribe_delay_state, state=UnsubscribeStates.delay)
    dp.register_message_handler(
        viewer_id_channel_state, state=ViewerPostStates.id_channel
    )
    dp.register_message_handler(viewer_id_post_state, state=ViewerPostStates.id_post)
    dp.register_message_handler(
        number_of_post_state, state=ViewerPostStates.number_of_post
    )
    dp.register_message_handler(
        viewer_number_of_accounts_state, state=ViewerPostStates.number_of_accounts
    )
    dp.register_message_handler(viewer_delay_state, state=ViewerPostStates.delay)
    dp.register_message_handler(
        reactions_id_channel_state, state=ReactionsStates.id_channel
    )
    dp.register_message_handler(reactions_id_post_state, state=ReactionsStates.id_post)
    dp.register_message_handler(
        number_of_button_state, state=ReactionsStates.number_of_button
    )
    dp.register_message_handler(
        reactions_number_of_accounts_state, state=ReactionsStates.number_of_accounts
    )
    dp.register_message_handler(reactions_delay_state, state=ReactionsStates.delay)
