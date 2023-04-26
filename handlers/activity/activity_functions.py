import asyncio
import math
import random
import time
from copy import copy
from os import remove, walk
from random import shuffle

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from telethon import TelegramClient, functions
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from config import API_HASH, API_ID, MILES_IN_HOUR, RANDOM_PERCENT
from handlers.main.main_functions import get_main_keyboard
from handlers.users.users_handler import add_user_button
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES, LOADING
from useful.commands_handler import commands_handler
from useful.instruments import bot
from useful.keyboards import activity_keyboard


def get_timing(timing_str):
    timing_arr = timing_str.split("\n")
    timing_dict = {}
    for timing in timing_arr:
        try:
            hour, percent = map(int, timing.split(" - "))
        except:
            try:
                hour, percent = map(int, timing.split("-"))
            except:
                try:
                    hour, percent = map(int, timing.split(" -"))
                except:
                    hour, percent = map(int, timing.split("- "))
        timing_dict[hour] = percent
    if sum(timing_dict.values()) == 100:
        return timing_dict
    else:
        return None


async def percent_timer(timing, function, args, message: Message = None):
    """
    :param message:
    :param timing: get_timing()
    :param function: function of account's activity
    :param args: [channel_link, count],
                [channel_link, count, last_post_id, count_posts],
                [channel_link, count, post_id, position]
    :return: None
    """

    message = await message.answer(text=LOADING[0])

    count = args[1]
    accounts = await get_accounts()
    shuffle(accounts)

    keys = list(timing.keys())
    sum_current_count = 0
    last_account_iter = 0

    start = time.time()

    for time_iter in range(1, max(keys) + 1):
        if time_iter in keys:
            last_iter = False
            hour = time_iter
            percent = timing[hour]
            if time_iter != max(keys):
                current_count = round(count * percent / 100)
                if current_count + sum_current_count <= count:
                    sum_current_count += current_count
                else:
                    current_count = count - sum_current_count
            else:
                last_iter = True
                current_count = count - sum_current_count

            delay = round(MILES_IN_HOUR / current_count)
            current_args = copy(args)
            current_args.append(delay)
            current_accounts = []
            for account_iter in range(
                    last_account_iter, last_account_iter + current_count
            ):
                current_accounts.append(accounts[account_iter])
            current_args[1] = current_count

            loading_args = [last_account_iter, count]

            is_success = await function(
                args=current_args, accounts=current_accounts, last_iter=last_iter, message=message, loading_args=loading_args
            )
            last_account_iter += current_count

            if not is_success:
                return False

        else:
            await asyncio.sleep(MILES_IN_HOUR)

        end = time.time()
        print(start - end)

    return True


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


def get_proxies():
    with open("proxy.txt") as file:
        proxies = file.read().split("\n")

        if "" in proxies:
            proxies.remove("")

        if proxies:
            proxy = proxies.pop(0)
            proxies.append(proxy)
            return proxy

        return proxies


def disconnect_all(accounts):
    for account in accounts:
        account.disconnect()


async def get_accounts():
    accounts = []
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("session"):
                try:
                    addr, port, user, pasw = get_proxies().split(":")

                    proxy = {
                        "proxy_type": "socks5",
                        "addr": addr,
                        "port": int(port),
                        "username": user,
                        "password": pasw,
                        "rdns": True,
                    }

                    client = TelegramClient(
                        f"base/{session}", API_ID, API_HASH, proxy=proxy
                    )
                except:
                    client = TelegramClient(f"base/{session}", API_ID, API_HASH)

                try:
                    await client.connect()
                    if not await client.get_me():
                        await client.disconnect()
                        remove(f"base/{session}")
                    else:
                        print(f"{session} connected")
                        accounts.append(client)
                except:
                    await client.disconnect()
                    remove(f"base/{session}")
        return accounts


# async def get_accounts_len():
#     accounts = await get_accounts()
#     accounts_len = len(accounts)
#     disconnect_all(accounts)
#     return accounts_len


async def get_accounts_len():
    accounts_len = 0
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("session"):
                accounts_len += 1
    return accounts_len


async def edit_message_loading(message: Message, percent=0):
    if percent == 1:
        await message.edit_text(text=LOADING[10])
    elif percent >= 0.9:
        await message.edit_text(text=LOADING[9])
    elif percent >= 0.8:
        await message.edit_text(text=LOADING[8])
    elif percent >= 0.7:
        await message.edit_text(text=LOADING[7])
    elif percent >= 0.6:
        await message.edit_text(text=LOADING[6])
    elif percent >= 0.5:
        await message.edit_text(text=LOADING[5])
    elif percent >= 0.4:
        await message.edit_text(text=LOADING[4])
    elif percent >= 0.3:
        await message.edit_text(text=LOADING[3])
    elif percent >= 0.2:
        await message.edit_text(text=LOADING[2])
    elif percent >= 0.1:
        await message.edit_text(text=LOADING[1])
    else:
        await message.edit_text(text=LOADING[0])


async def subscribe_public_channel(args, accounts=None, last_iter=False, message=None, loading_args=None):
    channel_link = args[0]
    count = args[1]
    delay = args[2]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
    else:
        current_count = 0
        max_count = count
        message = await message.answer(text=LOADING[0])

    if accounts is None:
        accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        shuffle(accounts)
        for account_iter in range(count):
            start = time.time()

            account = accounts[account_iter]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(JoinChannelRequest(channel_link))
                print(f"{phone.phone} вступил в {channel_link}")
            except Exception as error:
                print(str(error))

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)

            end = time.time()
            print(end - start)

        disconnect_all(accounts)
        return True
    else:
        disconnect_all(accounts)
        return False


async def subscribe_private_channel(args, accounts=None, last_iter=False, message=None, loading_args=None):
    channel_link = args[0]
    count = args[1]
    delay = args[2]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
    else:
        current_count = 0
        max_count = count
        message = await message.answer(text=LOADING[0])

    if "https://t.me/+" in channel_link:
        channel_link = channel_link.replace("https://t.me/+", "")
    elif "https://t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("https://t.me/joinchat/", "")
    if "t.me/+" in channel_link:
        channel_link = channel_link.replace("t.me/+", "")
    elif "t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("t.me/joinchat/", "")

    if accounts is None:
        accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        shuffle(accounts)
        for account_iter in range(count):
            account = accounts[account_iter]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(ImportChatInviteRequest(channel_link))
                print(f"{phone.phone} вступил в {channel_link}")
            except Exception as error:
                print(str(error))

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)

        disconnect_all(accounts)
        return True
    else:
        disconnect_all(accounts)
        return False


async def leave_public_channel(args, accounts=None, last_iter=False, message=None, loading_args=None):
    channel_link = args[0]
    count = args[1]
    delay = args[2]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
    else:
        current_count = 0
        max_count = count
        message = await message.answer(text=LOADING[0])

    if accounts is None:
        accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        for account_iter in range(count):
            account = accounts[account_iter]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(LeaveChannelRequest(channel_link))
                print(f"{phone.phone} покинул {channel_link}")
            except Exception as error:
                print(str(error))

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)

        disconnect_all(accounts)
        return True
    else:
        disconnect_all(accounts)
        return False


async def leave_private_channel(args, accounts=None, last_iter=False, message=None, loading_args=None):
    channel_link = args[0]
    count = args[1]
    delay = args[2]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
    else:
        current_count = 0
        max_count = count
        message = await message.answer(text=LOADING[0])

    if accounts is None:
        accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        elif "t.me/+" in channel_link:
            channel_link = channel_link.replace("t.me/+", "https://t.me/joinchat/")
        for account_iter in range(count):
            account = accounts[account_iter]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                try:
                    chat = await account.get_entity(channel_link)
                    chat_title = chat.title
                except:
                    return
                async for dialog in account.iter_dialogs():
                    if dialog.title == chat_title:
                        await dialog.delete()
                        print(f"{phone.phone} покинул {channel_link}")
            except Exception as error:
                print(str(error))

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)

        disconnect_all(accounts)
        return True
    else:
        disconnect_all(accounts)
        return False


async def view_post(args, accounts=None, last_iter=False, message=None, loading_args=None):
    channel_link = args[0]
    count_accounts = args[1]
    last_post_id = args[2]
    count_posts = args[3]
    delay = args[4]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
    else:
        current_count = 0
        max_count = count_accounts
        message = await message.answer(text=LOADING[0])

    if accounts is None:
        accounts = await get_accounts()
    accounts_len = len(accounts)
    if count_accounts <= accounts_len:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        elif "t.me/+" in channel_link:
            channel_link = channel_link.replace("t.me/+", "https://t.me/joinchat/")
        for account_iter in range(count_accounts):
            account = accounts[account_iter]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(
                    functions.messages.GetMessagesViewsRequest(
                        peer=channel_link,
                        id=[
                            post_id
                            for post_id in range(
                                last_post_id, last_post_id - count_posts, -1
                            )
                        ],
                        increment=True,
                    )
                )
                print(f"{phone.phone} посмторел посты в {channel_link}")
            except Exception as error:
                print(str(error))

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count_accounts and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)

        disconnect_all(accounts)
        return True
    else:
        disconnect_all(accounts)
        return False


async def click_on_button(args, accounts=None, last_iter=False, message=None, loading_args=None):
    channel_link = args[0]
    count = args[1]
    post_id = args[2]
    position = args[3]
    delay = args[4]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
    else:
        current_count = 0
        max_count = count
        message = await message.answer(text=LOADING[0])

    if accounts is None:
        accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        elif "t.me/+" in channel_link:
            channel_link = channel_link.replace("t.me/+", "https://t.me/joinchat/")
        for account_iter in range(count):
            account = accounts[account_iter]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                message = await account.get_messages(channel_link, ids=[int(post_id)])
                await message[0].click(position - 1)
                print(f"{phone.phone} нажал на кнопку в {channel_link}")
            except Exception as error:
                print(str(error))

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)

        disconnect_all(accounts)
        return True
    else:
        disconnect_all(accounts)
        return False
