from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from handlers.activity.activity_functions import *
from states import ReactionsStates, SubscribeStates, UnsubscribeStates, ViewerPostStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.callbacks import (
    delay_callback,
    reactions_callback,
    subscribe_callback,
    unsubscribe_all_callback,
    unsubscribe_callback,
    viewer_post_callback,
)
from useful.instruments import callback_dict
from useful.keyboards import ask_delay_keyboard


async def chose_activity(message: Message):
    await message.answer(
        text=MESSAGES["chose_activity"], reply_markup=activity_keyboard()
    )


"""
    SUBSCRIBE CHANNEL STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def subscribe_query(query: CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.edit_text(text=MESSAGES["channel_link"], reply_markup=None)
    is_public = callback_data.get("is_public")
    await state.update_data(is_public=is_public)
    await SubscribeStates.channel_link.set()


async def subscribe_channel_link_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if answer.startswith("https://t.me/"):
            await state.update_data(channel_link=answer)
            accounts_len = await get_accounts_len()
            await message.answer(
                text=MESSAGES["number_of_accounts"].format(count=accounts_len)
            )
            await SubscribeStates.number_of_accounts.set()
        else:
            await message.answer(text=MESSAGES["link_error"])
            await SubscribeStates.channel_link.set()


async def subscribe_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        accounts_len = await get_accounts_len()
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await SubscribeStates.number_of_accounts.set()
        elif accounts_len < int(answer):
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["count_user_error"].format(count=accounts_len),
            )
            await SubscribeStates.number_of_accounts.set()
        else:
            await state.update_data(count=int(answer))
            data = await state.get_data()
            link = data["channel_link"]
            count = int(answer)
            is_public = data["is_public"]
            await message.answer(
                text=MESSAGES["delay_ask"],
                reply_markup=ask_delay_keyboard(
                    message.from_user.id, link, count, is_public
                ),
            )
            await state.finish()


async def subscribe_ask_delay_state(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    if await not_command_checker(message=query.message, state=state):
        answer = callback_data["answer"]
        user_id = int(callback_data["user_id"])
        link, count, is_public = callback_dict[user_id]
        callback_dict.pop(user_id)
        await state.update_data(channel_link=link)
        await state.update_data(count=count)
        await state.update_data(is_public=is_public)
        await state.update_data(delay_ask=answer)
        if answer == BUTTONS["delay_1"]:  # Обычная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_regular"], reply_markup=None
            )
            await SubscribeStates.delay.set()
        elif answer == BUTTONS["delay_2"]:  # Процентная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_perсent"], reply_markup=None
            )
            # Встатить нужное
            await SubscribeStates.delay_percent.set()


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
                is_success = await subscribe_public_channel(
                    args=[data["channel_link"], data["count"], data["delay"]]
                )
            else:
                is_success = await subscribe_private_channel(
                    args=[data["channel_link"], data["count"], data["delay"]]
                )
            if is_success:
                await message.answer(
                    text=MESSAGES["subscribe"], reply_markup=get_main_keyboard()
                )
                await state.finish()
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES["error"],
                )
                await message.answer(text=MESSAGES["channel_link"])
                await SubscribeStates.channel_link.set()


async def subscribe_delay_percent_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text

        timing = get_timing(answer)
        if timing is None:
            await message.answer(
                text=MESSAGES["delay_perсent"], reply_markup=ReplyKeyboardRemove()
            )
            await SubscribeStates.delay_percent.set()
        else:
            data = await state.get_data()
            is_public = data["is_public"] == "True"
            args = [data["channel_link"], data["count"]]
            if is_public:
                is_success = await percent_timer(timing, subscribe_public_channel, args)
            else:
                is_success = await percent_timer(
                    timing, subscribe_private_channel, args
                )

            if is_success:
                await message.answer(
                    text=MESSAGES["subscribe"], reply_markup=get_main_keyboard()
                )
                await state.finish()

            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES["error"],
                )
                await message.answer(text=MESSAGES["channel_link"])
                await SubscribeStates.channel_link.set()


"""
    UNSUBSCRIBE CHANNEL STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def unsubscribe_query(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    await query.message.edit_text(text=MESSAGES["channel_link"], reply_markup=None)
    is_public = callback_data.get("is_public")
    await state.update_data(is_public=is_public)
    await UnsubscribeStates.channel_link.set()


async def unsubscribe_channel_link_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if answer.startswith("https://t.me/"):
            await state.update_data(channel_link=answer)
            accounts_len = await get_accounts_len()
            await message.answer(
                text=MESSAGES["number_of_accounts"].format(count=accounts_len)
            )
            await UnsubscribeStates.number_of_accounts.set()
        else:
            await message.answer(text=MESSAGES["link_error"])
            await UnsubscribeStates.channel_link.set()


async def unsubscribe_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        accounts_len = await get_accounts_len()
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await UnsubscribeStates.number_of_accounts.set()
        elif accounts_len < int(answer):
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["count_user_error"].format(count=accounts_len),
            )
            await UnsubscribeStates.number_of_accounts.set()
        else:
            await state.update_data(count=int(answer))
            await message.answer(text=MESSAGES["delay_ask"])
            await UnsubscribeStates.delay.set()


async def unsubscribe_ask_delay_state(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    if await not_command_checker(message=query.message, state=state):
        answer = callback_data["answer"]
        user_id = int(callback_data["user_id"])
        link, count, is_public = callback_dict[user_id]
        callback_dict.pop(user_id)
        await state.update_data(channel_link=link)
        await state.update_data(count=count)
        await state.update_data(is_public=is_public)
        await state.update_data(delay_ask=answer)
        if answer == BUTTONS["delay_1"]:  # Обычная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_regular"], reply_markup=None
            )
            await UnsubscribeStates.delay.set()
        elif answer == BUTTONS["delay_2"]:  # Процентная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_perсent"], reply_markup=None
            )
            # Встатить нужное
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
                is_success = await leave_public_channel(
                    args=[data["channel_link"], data["count"], data["delay"]]
                )
            else:
                is_success = await leave_private_channel(
                    args=[data["channel_link"], data["count"], data["delay"]]
                )
            if is_success:
                await message.answer(
                    text=MESSAGES["unsubscribe"], reply_markup=ReplyKeyboardRemove()
                )
                await state.finish()
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES["error"],
                )
                await message.answer(text=MESSAGES["channel_link"])
                await UnsubscribeStates.channel_link.set()


"""
       POST VIEWERS STATES⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def viewer_post_button(query: CallbackQuery):
    await query.message.edit_text(text=MESSAGES["channel_link"], reply_markup=None)
    await ViewerPostStates.id_channel.set()


async def viewer_id_channel_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if answer.startswith("https://t.me/"):
            await state.update_data(channel_link=answer)
            await message.answer(text=MESSAGES["id_post"])
            await ViewerPostStates.id_post.set()
        else:
            await message.answer(text=MESSAGES["link_error"])
            await ViewerPostStates.id_channel.set()


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
            accounts_len = await get_accounts_len()
            await message.answer(
                text=MESSAGES["number_of_accounts"].format(count=accounts_len)
            )
            await ViewerPostStates.number_of_accounts.set()


async def viewer_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        accounts_len = await get_accounts_len()
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ViewerPostStates.number_of_accounts.set()
        elif accounts_len < int(answer):
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["count_user_error"].format(count=accounts_len),
            )
            await ViewerPostStates.number_of_accounts.set()
        else:
            await state.update_data(count_accounts=int(answer))
            await message.answer(text=MESSAGES["delay_ask"])
            await ViewerPostStates.delay.set()


async def viewer_ask_delay_state(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    if await not_command_checker(message=query.message, state=state):
        answer = callback_data["answer"]
        user_id = int(callback_data["user_id"])
        link, count, is_public = callback_dict[user_id]
        callback_dict.pop(user_id)
        await state.update_data(channel_link=link)
        await state.update_data(count=count)
        await state.update_data(is_public=is_public)
        await state.update_data(delay_ask=answer)
        if answer == BUTTONS["delay_1"]:  # Обычная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_regular"], reply_markup=None
            )
            await ViewerPostStates.delay.set()
        elif answer == BUTTONS["delay_2"]:  # Процентная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_perсent"], reply_markup=None
            )
            # Встатить нужное
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
            is_success = await view_post(
                args=[
                    data["channel_link"],
                    data["count_accounts"],
                    data["last_post_id"],
                    data["count_posts"],
                    data["delay"],
                ]
            )
            if is_success:
                await message.answer(
                    text=MESSAGES["viewer_post"], reply_markup=ReplyKeyboardRemove()
                )
                await state.finish()
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES["error"],
                )
                await message.answer(text=MESSAGES["channel_link"])
                await ViewerPostStates.id_channel.set()


"""
        REACTIONS STATES⠀⠀⠀⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀
               ⣿⣿⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


async def reactions_query(query: CallbackQuery):
    await query.message.edit_text(text=MESSAGES["channel_link"], reply_markup=None)
    await ReactionsStates.id_channel.set()


async def reactions_id_channel_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if answer.startswith("https://t.me/"):
            await state.update_data(channel_link=answer)
            await message.answer(text=MESSAGES["id_post"])
            await ReactionsStates.id_post.set()
        else:
            await message.answer(text=MESSAGES["link_error"])
            await ReactionsStates.id_channel.set()


async def reactions_id_post_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.id_post.set()
        else:
            await state.update_data(post_id=int(answer))
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
            await state.update_data(position=int(answer))
            accounts_len = await get_accounts_len()
            await message.answer(
                text=MESSAGES["number_of_accounts"].format(count=accounts_len)
            )
            await ReactionsStates.number_of_accounts.set()


async def reactions_number_of_accounts_state(message: Message, state: FSMContext):
    if await not_command_checker(message=message, state=state):
        answer = message.text
        accounts_len = await get_accounts_len()
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["isdigit"], reply_markup=ReplyKeyboardRemove()
            )
            await ReactionsStates.number_of_accounts.set()
        elif accounts_len < int(answer):
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["count_user_error"].format(count=accounts_len),
            )
            await ReactionsStates.number_of_accounts.set()
        else:
            await state.update_data(count=int(answer))
            await message.answer(text=MESSAGES["delay_ask"])
            await ReactionsStates.delay.set()


async def reactions_ask_delay_state(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    if await not_command_checker(message=query.message, state=state):
        answer = callback_data["answer"]
        user_id = int(callback_data["user_id"])
        link, count, is_public = callback_dict[user_id]
        callback_dict.pop(user_id)
        await state.update_data(channel_link=link)
        await state.update_data(count=count)
        await state.update_data(is_public=is_public)
        await state.update_data(delay_ask=answer)
        if answer == BUTTONS["delay_1"]:  # Обычная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_regular"], reply_markup=None
            )
            await ReactionsStates.delay.set()
        elif answer == BUTTONS["delay_2"]:  # Процентная задержка
            await query.message.edit_text(
                text=MESSAGES["delay_perсent"], reply_markup=None
            )
            # Встатить нужное
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
            await state.update_data(delay=int(answer))
            data = await state.get_data()
            is_success = await click_on_button(
                args=[
                    data["channel_link"],
                    data["count"],
                    data["post_id"],
                    data["position"],
                    data["delay"],
                ]
            )
            if is_success:
                await message.answer(
                    text=MESSAGES["reactions"], reply_markup=ReplyKeyboardRemove()
                )
                await state.finish()
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES["error"],
                )
                await message.answer(text=MESSAGES["channel_link"])
                await ReactionsStates.id_channel.set()


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
    dp.register_callback_query_handler(
        subscribe_ask_delay_state, delay_callback.filter()
    )
    dp.register_message_handler(subscribe_delay_state, state=SubscribeStates.delay)
    dp.register_message_handler(
        subscribe_delay_percent_state, state=SubscribeStates.delay_percent
    )
    dp.register_message_handler(
        unsubscribe_channel_link_state, state=UnsubscribeStates.channel_link
    )
    dp.register_message_handler(
        unsubscribe_number_of_accounts_state, state=UnsubscribeStates.number_of_accounts
    )
    dp.register_callback_query_handler(
        unsubscribe_ask_delay_state, delay_callback.filter()
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
    dp.register_callback_query_handler(viewer_ask_delay_state, delay_callback.filter())
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
    dp.register_callback_query_handler(
        reactions_ask_delay_state, delay_callback.filter()
    )
    dp.register_message_handler(reactions_delay_state, state=ReactionsStates.delay)
