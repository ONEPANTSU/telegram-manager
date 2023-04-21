from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from handlers.main.main_functions import main_menu, get_main_keyboard
from handlers.users.users_handler import add_user_button
from states import SubscribeStates, UnsubscribeStates, ViewerPostStates, ReactionsStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot


def activity_keyboard():
    sub_open_button = InlineKeyboardButton(text=BUTTONS['subscribe_open'], callback_data=subscribe_open_callback.new())
    sub_close_button = InlineKeyboardButton(text=BUTTONS['subscribe_close'],
                                            callback_data=subscribe_close_callback.new())
    unsub_open_button = InlineKeyboardButton(text=BUTTONS['unsubscribe_open'],
                                             callback_data=unsubscribe_open_callback.new())
    unsub_close_button = InlineKeyboardButton(text=BUTTONS['unsubscribe_close'],
                                              callback_data=unsubscribe_close_callback.new())
    view_button = InlineKeyboardButton(text=BUTTONS['view'], callback_data=viewer_post_callback.new())
    react_button = InlineKeyboardButton(text=BUTTONS['react'], callback_data=reactions_callback.new())
    unsub_all_button = InlineKeyboardButton(text=BUTTONS['unsub_all'], callback_data=unsub_all_callback.new())
    act_keyboard = InlineKeyboardMarkup(row_width=1).add(sub_open_button, sub_close_button, unsub_open_button, unsub_close_button,
                                              unsub_all_button, view_button, react_button)
    return act_keyboard


subscribe_open_callback = CallbackData("subscribe_open_button")
subscribe_close_callback = CallbackData("subscribe_close_button")
unsubscribe_open_callback = CallbackData("unsubscribe_open_button")
unsubscribe_close_callback = CallbackData("unsubscribe_close_button")
viewer_post_callback = CallbackData("viewer_post_button")
reactions_callback = CallbackData("reactions_button")
unsub_all_callback = CallbackData("unsub_all_button")


async def chose_activity(message: Message):
    await message.answer(text=MESSAGES["chose_activity"], reply_markup=activity_keyboard())

#для подписки


async def subscribe_button(query: CallbackQuery, callback_data: dict):
    await query.message.edit_text(text=MESSAGES["channel_link"], reply_markup=None)
    await SubscribeStates.channel_link.set()


async def sub_channel_link_state(message: Message, state: FSMContext):
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
    else:
        await state.update_data(channel_link=answer)
        await message.answer(text=MESSAGES["number_of_accounts"])
        await SubscribeStates.number_of_accounts.set()


async def sub_number_of_accounts_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await SubscribeStates.number_of_accounts.set()
        else:
            await state.update_data(number_of_accounts=answer)
            await message.answer(text=MESSAGES["delay"])
            await SubscribeStates.delay.set()


async def sub_delay_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await SubscribeStates.delay.set()
        else:
            await state.update_data(delay=answer)
            await message.answer(text=MESSAGES["subscribe"])
            await state.finish()

#выбор приватный или неприватный канал

#для отписки


async def unsubscribe_button(query: CallbackQuery, callback_data: dict):
    await query.message.answer(text=MESSAGES["channel_link"])
    await UnsubscribeStates.channel_link.set()


async def unsub_channel_link_state(message: Message, state: FSMContext):
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
    else:
        await state.update_data(channel_link=answer)
        await message.answer(text=MESSAGES["number_of_accounts"])
        await UnsubscribeStates.number_of_accounts.set()


async def unsub_number_of_accounts_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await UnsubscribeStates.number_of_accounts.set()
        else:
            await state.update_data(number_of_accounts=answer)
            await message.answer(text=MESSAGES["delay"])
            await UnsubscribeStates.delay.set()


async def unsub_delay_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await UnsubscribeStates.delay.set()
        else:
            await state.update_data(delay=answer)
            await message.answer(text=MESSAGES["unsubscribe"])
            await state.finish()

#выбор приватный или неприватный канал


#для отписки от всех каналов

async def unsub_all_button(message: Message):
    pass

#для просмотров постов


async def viewer_post_button(query: CallbackQuery, callback_data: dict):
    await query.message.answer(text=MESSAGES["id_channel"])
    await ViewerPostStates.id_channel.set()


async def viewer_id_channel_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.id_channel.set()
        else:
            await state.update_data(id_channel=answer)
            await message.answer(text=MESSAGES["id_post"])
            await ViewerPostStates.id_post.set()


async def viewer_id_post_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.id_post.set()
        else:
            await state.update_data(id_post=answer)
            await message.answer(text=MESSAGES["number_of_post"])
            await ViewerPostStates.number_of_post.set()


async def number_of_post_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.number_of_post.set()
        else:
            await state.update_data(number_of_post=answer)
            await message.answer(text=MESSAGES["number_of_accounts"])
            await ViewerPostStates.number_of_accounts.set()


async def viewer_number_of_accounts_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.number_of_accounts.set()
        else:
            await state.update_data(number_of_accounts=answer)
            await message.answer(text=MESSAGES["delay"])
            await ViewerPostStates.delay.set()


async def viewer_delay_state(message: Message, state: FSMContext):
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
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.delay.set()
        else:
            await state.update_data(delay=answer)
            await message.answer(text=MESSAGES["viewer_post"])
            await state.finish()

#для реакций


async def reactions_button(query: CallbackQuery, callback_data: dict):
    await query.message.answer(text=MESSAGES["id_channel"])
    await ReactionsStates.id_channel.set()


async def reactions_id_channel_state(message: Message, state: FSMContext):
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
    else:
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
    else:
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
    else:
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
    else:
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
    else:
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
    dp.register_callback_query_handler(subscribe_button, subscribe_open_callback.filter())
    dp.register_callback_query_handler(subscribe_button, subscribe_close_callback.filter())
    dp.register_callback_query_handler(unsubscribe_button, unsubscribe_open_callback.filter())
    dp.register_callback_query_handler(unsubscribe_button, unsubscribe_close_callback.filter())
    dp.register_callback_query_handler(viewer_post_button, viewer_post_callback.filter())
    dp.register_callback_query_handler(reactions_button, reactions_callback.filter())
    dp.register_callback_query_handler(chose_activity, unsub_all_callback.filter())
    dp.register_message_handler(sub_channel_link_state, state=SubscribeStates.channel_link)
    dp.register_message_handler(sub_number_of_accounts_state, state=SubscribeStates.number_of_accounts)
    dp.register_message_handler(sub_delay_state, state=SubscribeStates.delay)
    dp.register_message_handler(unsub_channel_link_state, state=UnsubscribeStates.channel_link)
    dp.register_message_handler(unsub_number_of_accounts_state, state=UnsubscribeStates.number_of_accounts)
    dp.register_message_handler(unsub_delay_state, state=UnsubscribeStates.delay)
    dp.register_message_handler(viewer_id_channel_state, state=ViewerPostStates.id_channel)
    dp.register_message_handler(viewer_id_post_state, state=ViewerPostStates.id_post)
    dp.register_message_handler(number_of_post_state, state=ViewerPostStates.number_of_post)
    dp.register_message_handler(viewer_number_of_accounts_state, state=ViewerPostStates.number_of_accounts)
    dp.register_message_handler(viewer_delay_state, state=ViewerPostStates.delay)
    dp.register_message_handler(reactions_id_channel_state, state=ReactionsStates.id_channel)
    dp.register_message_handler(reactions_id_post_state, state=ReactionsStates.id_post)
    dp.register_message_handler(number_of_button_state, state=ReactionsStates.number_of_button)
    dp.register_message_handler(reactions_number_of_accounts_state, state=ReactionsStates.number_of_accounts)
    dp.register_message_handler(reactions_delay_state, state=ReactionsStates.delay)


