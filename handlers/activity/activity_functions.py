import asyncio
import gc
import math
import os
import random
import time
from copy import copy
from os import remove, walk

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from telethon import TelegramClient, functions
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputPeerNotifySettings

from config import API_HASH, API_ID, HOURS_IN_WEEK, MILES_IN_HOUR, RANDOM_PERCENT
from handlers.activity.database import *
from handlers.main.main_functions import get_main_keyboard
from handlers.users.users_handler import add_user_button
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import LOADING, MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot
from useful.keyboards import activity_keyboard
from useful.task_keyboard import create_task_page


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
                    try:
                        hour, percent = map(int, timing.split("- "))
                    except:
                        return None
        timing_dict[hour] = percent
    if sum(timing_dict.values()) == 100:
        return timing_dict
    else:
        return None


async def unsubscribe_timing(accounts, channel_link):
    if len(accounts) >= 6:
        week_percents = {
            1: math.ceil(len(accounts) * 0.1),
            2: math.ceil(len(accounts) * 0.08),
            3: math.ceil(len(accounts) * 0.05),
            4: math.ceil(len(accounts) * 0.03),
            5: math.ceil(len(accounts) * 0.02),
            6: math.ceil(len(accounts) * 0.02),
        }
        keys = []
        for week in range(6):
            for acc in range(week_percents[week + 1]):
                hour = week * HOURS_IN_WEEK + random.randint(1, HOURS_IN_WEEK)
                keys.append(hour)

        shuffle(accounts)

        args = [channel_link, 1, 1]

        account_iter = 0
        start = time.time()

        for time_iter in range(1, max(keys) + 1):
            if time_iter in keys:
                print("trying to unsub")
                gc.collect()
                current_account = []
                try:
                    try:
                        current_account.append(accounts[account_iter])
                    except:
                        print("IndexError: list index out of range")

                    is_success = await leave_channel(
                        args=args, accounts=current_account
                    )
                    print(is_success)
                    account_iter += 1

                    if not is_success:
                        return False
                except:
                    print("IndexError: list index out of range II")
            else:
                await asyncio.sleep(MILES_IN_HOUR)

            end = time.time()
            print(start - end)

        return True


def add_task_to_db(link, count, timing, is_sub):
    if is_sub == 1:
        accounts = get_list_of_numbers(link=link, sub=True)
    elif is_sub == -1:
        accounts = get_list_of_numbers(link=link, sub=False)
    else:
        accounts = get_list_of_numbers()
    shuffle(accounts)
    accounts_for_timing = accounts[:count]
    task_id = add_task(accounts=accounts_for_timing, count=count, timing=timing)
    return task_id


async def percent_timer(
    timing,
    function,
    args,
    prev_message: Message = None,
    return_accounts=False,
    is_sub=0,
):
    """
    :param is_sub: False = -1; True = 1.
    :param return_accounts: for unsubscribe timing
    :param prev_message:
    :param timing: get_timing()
    :param function: function of account's activity
    :param args: [channel_link, count],
                [channel_link, count, last_post_id, count_posts],
                [channel_link, count, post_id, position]
    :return: None
    """

    count = args[1]
    link = args[0]
    try:
        task_id = add_task_to_db(link=link, count=count, timing=timing, is_sub=is_sub)

        await prev_message.answer(text="Задача #" + str(task_id))
        message = await prev_message.answer(text=LOADING[0])
        await prev_message.delete()

        keys = list(timing.keys())
        sum_current_count = 0
        last_account_iter = 0

        start = time.time()

        for time_iter in range(1, max(keys) + 1):
            try:
                task_status = get_task_by_id(task_id)
                if task_status is not None:
                    task_status = task_status[2]
                else:
                    print("Task #" + str(task_id) + " was stopped")
                    break
                print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                if task_status is None:
                    print("Task #" + str(task_id) + " was stopped")
                    break
            except:
                print("TaskStatus Error")

            if time_iter in keys:
                gc.collect()

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
                if current_count != 0:
                    delay = round(MILES_IN_HOUR / current_count)
                    current_args = copy(args)
                    current_args.append(delay)
                    current_accounts = []

                    try:
                        try:
                            current_accounts = get_phone_by_task(task_id)[
                                :current_count
                            ]
                        except:
                            print("IndexError: list index out of range")

                        current_args[1] = current_count

                        loading_args = [last_account_iter, count]

                        is_success = await function(
                            args=current_args,
                            accounts=current_accounts,
                            last_iter=last_iter,
                            prev_message=message,
                            loading_args=loading_args,
                            task_id=task_id,
                        )
                        last_account_iter += current_count

                        if not is_success:
                            if return_accounts:
                                return False, get_phone_by_task(task_id)
                            return False
                    except:
                        print("IndexError: list index out of range II")
            else:
                await asyncio.sleep(MILES_IN_HOUR)

            end = time.time()
            print(start - end)

        try:
            delete_task(task_id)
        except:
            print("DeleteTask Error (#" + str(task_id) + ")")

        if return_accounts:
            return True, get_phone_by_task(task_id)
        return True
    except:
        print("Can't create the task")


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
    elif answer == BUTTONS["count_users"]:
        accounts_len = await get_all_accounts_len()
        await message.answer(
            text=MESSAGES["available_bot"].format(count_user=accounts_len)
        )
    elif answer == BUTTONS["task"]:
        task_list = get_tasks()
        if len(task_list) != 0:
            await create_task_page(
                chat_id=message.chat.id,
                task_list=task_list,
                page=0,
                message=message,
            )
        else:
            await message.answer(
                text=MESSAGES["empty_task"], reply_markup=None
            )
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


def delete_journals_files():
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("journal"):
                try:
                    os.remove("base/" + session)
                except:
                    print("Deleting was excepted")


# def disconnect_all(accounts):
#     for account in accounts:
#         try:
#             account.disconnect()
#         except:
#             pass


async def get_accounts():
    accounts = []
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("session"):
                if not session + "-journal" in sessions:
                    try:
                        addr, port, user, passwd = get_proxies().split(":")

                        proxy = {
                            "proxy_type": "socks5",
                            "addr": addr,
                            "port": int(port),
                            "username": user,
                            "password": passwd,
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


async def get_all_accounts_len():
    accounts_len = 0
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("session"):
                accounts_len += 1
    return accounts_len


def get_list_of_numbers(link=None, sub=False):
    if link is None:
        accounts = []
        for _, _, sessions in walk("base"):
            for session in sessions:
                if session.endswith("session"):
                    accounts.append(session)
        return accounts
    else:
        if "https://t.me/+" in link:
            link = link.replace("https://t.me/+", "")
        elif "https://t.me/joinchat/" in link:
            link = link.replace("https://t.me/joinchat/", "")
        elif "t.me/+" in link:
            link = link.replace("t.me/+", "")
        elif "t.me/joinchat/" in link:
            link = link.replace("t.me/joinchat/", "")
        already_exists = get_phones(link=link)
        try:
            for iteration in range(len(already_exists)):
                already_exists[iteration] = already_exists[iteration][0]
        except:
            pass
        if sub:
            accounts = []
            for _, _, sessions in walk("base"):
                for session in sessions:
                    if session.endswith("session") and not (session in already_exists):
                        accounts.append(session)
            return accounts
        else:
            accounts = []
            for _, _, sessions in walk("base"):
                for session in sessions:
                    if session.endswith("session") and (session in already_exists):
                        accounts.append(session)
            return accounts


async def connect_to_account(session):
    for _, _, sessions in walk("base"):
        if not session + "-journal" in sessions:
            try:
                addr, port, user, passwd = get_proxies().split(":")

                proxy = {
                    "proxy_type": "socks5",
                    "addr": addr,
                    "port": int(port),
                    "username": user,
                    "password": passwd,
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
                    return client
            except:
                await client.disconnect()
                remove(f"base/{session}")
            return None


async def get_accounts_len(link=None, sub=False):
    if link is None:
        accounts_len = 0
        for _, _, sessions in walk("base"):
            for session in sessions:
                if session.endswith("session"):
                    accounts_len += 1
                elif session.endswith("session-journal"):
                    accounts_len -= 1
        return accounts_len
    else:
        if "https://t.me/+" in link:
            link = link.replace("https://t.me/+", "")
        elif "https://t.me/joinchat/" in link:
            link = link.replace("https://t.me/joinchat/", "")
        elif "t.me/+" in link:
            link = link.replace("t.me/+", "")
        elif "t.me/joinchat/" in link:
            link = link.replace("t.me/joinchat/", "")
        already_exists = len(get_phones(link=link))
        if sub:
            accounts_len = 0
            for _, _, sessions in walk("base"):
                for session in sessions:
                    if session.endswith("session"):
                        accounts_len += 1
                    elif session.endswith("session-journal"):
                        accounts_len -= 1
            return accounts_len - already_exists
        else:
            return already_exists


async def edit_message_loading(message: Message, percent=0):
    if percent == 1:
        try:
            await message.edit_text(text=LOADING[10])
        except:
            pass
    elif percent >= 0.9:
        try:
            await message.edit_text(text=LOADING[9])
        except:
            pass
    elif percent >= 0.8:
        try:
            await message.edit_text(text=LOADING[8])
        except:
            pass
    elif percent >= 0.7:
        try:
            await message.edit_text(text=LOADING[7])
        except:
            pass
    elif percent >= 0.6:
        try:
            await message.edit_text(text=LOADING[6])
        except:
            pass
    elif percent >= 0.5:
        try:
            await message.edit_text(text=LOADING[5])
        except:
            pass
    elif percent >= 0.4:
        try:
            await message.edit_text(text=LOADING[4])
        except:
            pass
    elif percent >= 0.3:
        try:
            await message.edit_text(text=LOADING[3])
        except:
            pass
    elif percent >= 0.2:
        try:
            await message.edit_text(text=LOADING[2])
        except:
            pass
    elif percent >= 0.1:
        try:
            await message.edit_text(text=LOADING[1])
        except:
            pass


async def subscribe_public_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    channel_link = args[0]
    count = args[1]
    delay = args[2]
    message = None

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
        message = prev_message
    else:
        current_count = 0
        max_count = count
        if prev_message is not None:
            message = await prev_message.answer(text=LOADING[0])
            await prev_message.delete()

    if accounts is None:
        accounts = get_list_of_numbers(link=channel_link, sub=True)
        shuffle(accounts)
        # disconnect_all(accounts[count:])
        accounts = accounts[:count]
    accounts_len = len(accounts)
    if count <= accounts_len:
        shuffle(accounts)
        for account_iter in range(count):
            if task_id is not None:
                try:
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                    else:
                        print("Task #" + str(task_id) + " was stopped")
                        break
                    print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                    while task_status == 0:
                        await asyncio.sleep(60)
                        task_status = get_task_by_id(task_id)
                        if task_status is not None:
                            task_status = task_status[2]
                    if task_status is None:
                        print("Task #" + str(task_id) + " was stopped")
                        break
                except:
                    print("TaskStatus Error")

            start = time.time()

            account = await connect_to_account(accounts[account_iter])
            if account is not None:
                phone = await account.get_me()
                try:
                    await account(
                        functions.account.UpdateStatusRequest(offline=False)
                    )  # Go to online
                    await account(JoinChannelRequest(channel_link))
                    await account(
                        UpdateNotifySettingsRequest(
                            peer=channel_link,
                            settings=InputPeerNotifySettings(mute_until=2**31 - 1),
                        )
                    )
                    print(f"{phone.phone} вступил в {channel_link}")
                    try:
                        add_database(link=channel_link, phone=accounts[account_iter])
                        delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                    except:
                        print("Не удалось добавить в БД")
                except Exception as error:
                    print(str(error))

                account.disconnect()

                current_count += 1
                done_percent = current_count / max_count
                if message is not None:
                    await edit_message_loading(message, done_percent)

                if not (account_iter + 1 == count and last_iter):
                    del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                    new_delay = delay + random.randint(-del_delay, del_delay)
                    await asyncio.sleep(new_delay)
            else:
                print("Connection error")

                current_count += 1
                done_percent = current_count / max_count
                if message is not None:
                    await edit_message_loading(message, done_percent)

            end = time.time()
            print(end - start)

            gc.collect()
        # disconnect_all(accounts)
        return True
    else:
        # disconnect_all(accounts)
        return False


async def subscribe_private_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    channel_link = args[0]
    count = args[1]
    delay = args[2]
    message = None

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
        message = prev_message
    else:
        current_count = 0
        max_count = count
        if prev_message is not None:
            message = await prev_message.answer(text=LOADING[0])
            await prev_message.delete()

    if "https://t.me/+" in channel_link:
        channel_link = channel_link.replace("https://t.me/+", "")
    elif "https://t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("https://t.me/joinchat/", "")
    if "t.me/+" in channel_link:
        channel_link = channel_link.replace("t.me/+", "")
    elif "t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("t.me/joinchat/", "")

    if accounts is None:
        accounts = get_list_of_numbers(link=channel_link, sub=True)
        shuffle(accounts)
        # disconnect_all(accounts[count:])
        accounts = accounts[:count]
    accounts_len = len(accounts)
    if count > accounts_len:
        count = accounts_len
    shuffle(accounts)
    for account_iter in range(count):
        if task_id is not None:
            try:
                task_status = get_task_by_id(task_id)
                if task_status is not None:
                    task_status = task_status[2]
                else:
                    print("Task #" + str(task_id) + " was stopped")
                    break
                print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                if task_status is None:
                    print("Task #" + str(task_id) + " was stopped")
                    break
            except:
                print("TaskStatus Error")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(ImportChatInviteRequest(channel_link))
                # await account(UpdateNotifySettingsRequest(
                #     peer=channel_link,
                #     settings=InputPeerNotifySettings(mute_until=2 ** 31 - 1))
                # )
                print(f"{phone.phone} вступил в {channel_link}")
                try:
                    add_database(phone=accounts[account_iter], link=channel_link)
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except:
                    print("Не удалось добавить в БД")
            except Exception as error:
                print(str(error))

            account.disconnect()

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)
        else:
            print("Connection error")

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

        gc.collect()
    # disconnect_all(accounts)
    return True
    # else:
    #     disconnect_all(accounts)
    #     return False


async def subscribe_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    if "t.me/+" in args[0]:
        is_success = await subscribe_private_channel(
            args=args,
            accounts=accounts,
            last_iter=last_iter,
            prev_message=prev_message,
            loading_args=loading_args,
            task_id=task_id,
        )
    else:
        is_success = await subscribe_public_channel(
            args=args,
            accounts=accounts,
            last_iter=last_iter,
            prev_message=prev_message,
            loading_args=loading_args,
            task_id=task_id,
        )

    return is_success


async def leave_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    if "t.me/+" in args[0]:
        is_success = await leave_private_channel(
            args=args,
            accounts=accounts,
            last_iter=last_iter,
            prev_message=prev_message,
            loading_args=loading_args,
            task_id=task_id,
        )
    else:
        is_success = await leave_public_channel(
            args=args,
            accounts=accounts,
            last_iter=last_iter,
            prev_message=prev_message,
            loading_args=loading_args,
            task_id=task_id,
        )
    return is_success


async def leave_public_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    channel_link = args[0]
    count = args[1]
    delay = args[2]
    message = None

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
        message = prev_message
    else:
        current_count = 0
        max_count = count
        if prev_message is not None:
            message = await prev_message.answer(text=LOADING[0])
            await prev_message.delete()

    if accounts is None:
        accounts = get_list_of_numbers(link=channel_link, sub=False)
        shuffle(accounts)
        # disconnect_all(accounts[count:])
        accounts = accounts[:count]
    accounts_len = len(accounts)
    if count > accounts_len:
        count = accounts_len
    for account_iter in range(count):
        if task_id is not None:
            try:
                task_status = get_task_by_id(task_id)
                if task_status is not None:
                    task_status = task_status[2]
                else:
                    print("Task #" + str(task_id) + " was stopped")
                    break
                print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                if task_status is None:
                    print("Task #" + str(task_id) + " was stopped")
                    break
            except:
                print("TaskStatus Error")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(LeaveChannelRequest(channel_link))
                print(f"{phone.phone} покинул {channel_link}")
                try:
                    delete_phone_link(link=channel_link, phone=accounts[account_iter])
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except:
                    print("Не удалось удалить из БД")
            except Exception as error:
                print(str(error))

            account.disconnect()

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)
        else:
            print("Connection error")

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

        # gc.collect()
    # disconnect_all(accounts)
    return True
    # else:
    #     disconnect_all(accounts)
    #     return False


async def leave_private_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    channel_link = args[0]
    count = args[1]
    delay = args[2]
    message = None

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
        message = prev_message
    else:
        current_count = 0
        max_count = count
        if prev_message is not None:
            message = await prev_message.answer(text=LOADING[0])
            await prev_message.delete()

    if accounts is None:
        accounts = get_list_of_numbers(link=channel_link, sub=False)
        shuffle(accounts)
        # disconnect_all(accounts[count:])
        accounts = accounts[:count]
    accounts_len = len(accounts)
    if count > accounts_len:
        count = accounts_len
    if "https://t.me/+" in channel_link:
        channel_link = channel_link.replace("https://t.me/+", "https://t.me/joinchat/")
    elif "t.me/+" in channel_link:
        channel_link = channel_link.replace("t.me/+", "https://t.me/joinchat/")

    link_for_db = channel_link.replace("https://t.me/joinchat/", "")

    for account_iter in range(count):
        if task_id is not None:
            try:
                task_status = get_task_by_id(task_id)
                if task_status is not None:
                    task_status = task_status[2]
                else:
                    print("Task #" + str(task_id) + " was stopped")
                    break
                print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                if task_status is None:
                    print("Task #" + str(task_id) + " was stopped")
                    break
            except:
                print("TaskStatus Error")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                try:
                    chat = await account.get_entity(channel_link)
                    chat_title = chat.title
                    async for dialog in account.iter_dialogs():
                        if dialog.title == chat_title:
                            await dialog.delete()
                            print(f"{phone.phone} покинул {channel_link}")
                            break
                except Exception as error:
                    print(str(error))
                    # return False

                try:
                    delete_phone_link(link=link_for_db, phone=accounts[account_iter])
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except Exception as error:
                    print(str(error))

            except Exception as error:
                print(str(error))
        else:
            print("Connection error")

        account.disconnect()

        current_count += 1
        done_percent = current_count / max_count
        if message is not None:
            await edit_message_loading(message, done_percent)

        if not (account_iter + 1 == count and last_iter):
            del_delay = math.floor(delay * RANDOM_PERCENT / 100)
            new_delay = delay + random.randint(-del_delay, del_delay)
            await asyncio.sleep(new_delay)

        gc.collect()
    # disconnect_all(accounts)
    return True
    # else:
    #     disconnect_all(accounts)
    #     return False


async def view_post(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    channel_link = args[0]
    count_accounts = args[1]
    last_post_id = args[2]
    count_posts = args[3]
    delay = args[4]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
        message = prev_message
    else:
        current_count = 0
        max_count = count_accounts
        message = await prev_message.answer(text=LOADING[0])
        await prev_message.delete()

    if accounts is None:
        accounts = get_list_of_numbers()
        shuffle(accounts)
        # disconnect_all(accounts[count_accounts:])
        accounts = accounts[:count_accounts]
    accounts_len = len(accounts)
    if count_accounts > accounts_len:
        count_accounts = accounts_len
    if "https://t.me/+" in channel_link:
        channel_link = channel_link.replace("https://t.me/+", "https://t.me/joinchat/")
    elif "t.me/+" in channel_link:
        channel_link = channel_link.replace("t.me/+", "https://t.me/joinchat/")
    for account_iter in range(count_accounts):
        if task_id is not None:
            try:
                task_status = get_task_by_id(task_id)
                if task_status is not None:
                    task_status = task_status[2]
                else:
                    print("Task #" + str(task_id) + " was stopped")
                    break
                print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                if task_status is None:
                    print("Task #" + str(task_id) + " was stopped")
                    break
            except:
                print("TaskStatus Error")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
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
                try:
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except:
                    pass
                print(f"{phone.phone} посмторел посты в {channel_link}")
            except Exception as error:
                print(str(error))

            account.disconnect()

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count_accounts and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)
        else:
            print("Connection error")

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

        gc.collect()
    # disconnect_all(accounts)
    return True
    # else:
    #     disconnect_all(accounts)
    #     return False


async def click_on_button(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
):
    channel_link = args[0]
    count = args[1]
    post_id = args[2]
    position = args[3]
    delay = args[4]

    if loading_args is not None:
        current_count = loading_args[0]
        max_count = loading_args[1]
        edit_message = prev_message
    else:
        current_count = 0
        max_count = count
        edit_message = await prev_message.answer(text=LOADING[0])
        await prev_message.delete()

    if accounts is None:
        accounts = get_list_of_numbers()
        shuffle(accounts)
        # disconnect_all(accounts[count:])
        accounts = accounts[:count]
    accounts_len = len(accounts)
    if count > accounts_len:
        count = accounts_len
    if "https://t.me/+" in channel_link:
        channel_link = channel_link.replace("https://t.me/+", "https://t.me/joinchat/")
    elif "t.me/+" in channel_link:
        channel_link = channel_link.replace("t.me/+", "https://t.me/joinchat/")
    for account_iter in range(count):
        if task_id is not None:
            try:
                task_status = get_task_by_id(task_id)
                if task_status is not None:
                    task_status = task_status[2]
                else:
                    print("Task #" + str(task_id) + " was stopped")
                    break
                print("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None:
                        task_status = task_status[2]
                if task_status is None:
                    print("Task #" + str(task_id) + " was stopped")
                    break
            except:
                print("TaskStatus Error")

        try:
            account = await connect_to_account(accounts[account_iter])
            if account is not None:
                phone = await account.get_me()
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                message = await account.get_messages(channel_link, ids=[int(post_id)])
                await message[0].click(position - 1)

                try:
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except:
                    pass

                print(f"{phone.phone} нажал на кнопку в {channel_link}")

                account.disconnect()

                current_count += 1
                done_percent = current_count / max_count
                await edit_message_loading(edit_message, done_percent)

                if not (account_iter + 1 == count and last_iter):
                    del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                    new_delay = delay + random.randint(-del_delay, del_delay)
                    await asyncio.sleep(new_delay)

                gc.collect()
        except Exception as error:
            print(str(error))
    # disconnect_all(accounts)
    return True
    # else:
    #     disconnect_all(accounts)
    #     return False
