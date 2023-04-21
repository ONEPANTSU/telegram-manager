from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from handlers.main.main_functions import main_menu
from states import SubscribeStates, UnsubscribeStates, ViewerPostStates, ReactionsStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES


def activity_keyboard():
    sub_button = InlineKeyboardButton(BUTTONS['subscribe'], callback_data='subscribe_button')
    unsub_button = InlineKeyboardButton(BUTTONS['unsubscribe'], callback_data='unsubscribe_button')
    view_button = InlineKeyboardButton(BUTTONS['view'], callback_data='viewer_post_button')
    react_button = InlineKeyboardButton(BUTTONS['react'], callback_data='reactions_button')
    unsub_all_button = InlineKeyboardButton(BUTTONS['unsub_all'], callback_data='unsub_all_button')
    act_keyboard = InlineKeyboardMarkup().add(sub_button, unsub_button, unsub_all_button, view_button, react_button)
    return act_keyboard


activity_callback = CallbackData("button")


async def chose_activity(message: Message):
    await message.reply(text=MESSAGES["chose_activity"], reply_markup=activity_keyboard())


async def chose_activity_callback(message: Message, query: CallbackQuery, callback_data: dict):
    answer = callback_data.get("button")
    if answer == BUTTONS['subscribe']:
        await subscribe_button(message)
    elif answer == BUTTONS['unsubscribe_button']:
        await unsubscribe_button(message)
    elif answer == BUTTONS['viewer_post_button']:
        await viewer_post_button(message)
    elif answer == BUTTONS['reactions_button']:
        await reactions_button(message)
    elif answer == BUTTONS['viewer_post_button']:
        await unsub_all_button(message)


#для подписки


async def subscribe_button(message: Message):
    await message.answer(text=MESSAGES["channel_link"])
    await SubscribeStates.channel_link.set()


async def sub_channel_link_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(channel_link=answer)
    await message.answer(text=MESSAGES["number_of_accounts"])
    await SubscribeStates.number_of_accounts.set()


async def sub_number_of_accounts_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(number_of_accounts=answer)
    await message.answer(text=MESSAGES["delay"])
    await SubscribeStates.delay.set()


async def sub_delay_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(delay=answer)
    await message.answer(text=MESSAGES["subscribe"])
    await state.finish()

#выбор приватный или неприватный канал

#для отписки


async def unsubscribe_button(message: Message):
    await message.answer(text=MESSAGES["channel_link"])
    await UnsubscribeStates.channel_link.set()


async def unsub_channel_link_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(channel_link=answer)
    await message.answer(text=MESSAGES["number_of_accounts"])
    await SubscribeStates.number_of_accounts.set()


async def unsub_number_of_accounts_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(number_of_accounts=answer)
    await message.answer(text=MESSAGES["delay"])
    await SubscribeStates.delay.set()


async def unsub_delay_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(delay=answer)
    await message.answer(text=MESSAGES["unsubscribe"])
    await state.finish()

#выбор приватный или неприватный канал


#для отписки от всех каналов

async def unsub_all_button(message: Message):
    pass

#для просмотров постов

async def viewer_post_button(message: Message):
    await message.answer(text=MESSAGES["id_channel"])
    await ViewerPostStates.id_channel.set()


async def viewer_id_channel_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(id_channel=answer)
    await message.answer(text=MESSAGES["id_post"])
    await ViewerPostStates.id_post.set()


async def viewer_id_post_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(id_post=answer)
    await message.answer(text=MESSAGES["number_of_post"])
    await ViewerPostStates.number_of_post.set()


async def number_of_post_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(number_of_post=answer)
    await message.answer(text=MESSAGES["number_of_accounts"])
    await ViewerPostStates.number_of_accounts.set()


async def viewer_number_of_accounts_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(number_of_accounts=answer)
    await message.answer(text=MESSAGES["delay"])
    await ViewerPostStates.delay.set()


async def viewer_delay_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(delay=answer)
    await message.answer(text=MESSAGES["viewer_post"])
    await state.finish()

#для реакций


async def reactions_button(message: Message):
    await message.answer(text=MESSAGES["id_channel"])
    await ReactionsStates.id_channel.set()


async def reactions_id_channel_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(id_channel=answer)
    await message.answer(text=MESSAGES["id_post"])
    await ReactionsStates.id_post.set()


async def reactions_id_post_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(id_post=answer)
    await message.answer(text=MESSAGES["number_of_button"])
    await ReactionsStates.number_of_button.set()


async def number_of_button_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(number_of_button=answer)
    await message.answer(text=MESSAGES["number_of_accounts"])
    await ReactionsStates.number_of_accounts.set()


async def reactions_number_of_accounts_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(number_of_accounts=answer)
    await message.answer(text=MESSAGES["delay"])
    await ReactionsStates.delay.set()


async def reactions_delay_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(delay=answer)
    await message.answer(text=MESSAGES["reactions"])
    await state.finish()


def register_activity_handlers(dp: Dispatcher):
    dp.register_message_handler(chose_activity, text=[BUTTONS["activity"]])
    dp.register_callback_query_handler(chose_activity_callback, activity_callback.filter())
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


