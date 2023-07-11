import asyncio
import math
import random
import time
from os import remove, walk

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from telethon import TelegramClient, functions
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputPeerNotifySettings

from config import API_HASH, API_ID, RANDOM_PERCENT
from handlers.activity.database import *
from handlers.main.main_functions import get_main_keyboard
from handlers.task.task_keyboard import create_task_page
from handlers.users.users_handler import add_user_button
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import LOADING, MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot, logger
from useful.keyboards import activity_keyboard


@logger.catch
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
            await message.answer(text=MESSAGES["empty_task"], reply_markup=None)
    else:
        return True


@logger.catch
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


@logger.catch
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
                    except Exception as e:
                        logger.error(f"Get Accounts Error: {e}")
                        client = TelegramClient(f"base/{session}", API_ID, API_HASH)

                    try:
                        await client.connect()
                        if not await client.get_me():
                            await client.disconnect()
                            remove(f"base/{session}")
                        else:
                            logger.info(f"{session} connected")
                            accounts.append(client)
                    except Exception as e:
                        logger.error(f"Get Accounts Error: {e}")
                        await client.disconnect()
                        remove(f"base/{session}")
        return accounts


@logger.catch
async def get_all_accounts_len():
    accounts_len = 0
    for _, _, sessions in walk("base"):
        for session in sessions:
            if session.endswith("session"):
                accounts_len += 1
    return accounts_len


@logger.catch
async def get_list_of_numbers(link=None, sub=False):
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
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "https://t.me/joinchat/" in link:
            link = link.replace("https://t.me/joinchat/", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "t.me/+" in link:
            link = link.replace("t.me/+", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "t.me/joinchat/" in link:
            link = link.replace("t.me/joinchat/", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        already_exists = get_phones(link=link)
        try:
            for iteration in range(len(already_exists)):
                already_exists[iteration] = already_exists[iteration][0]
        except Exception as e:
            logger.error(f"Get List Of Numbers Error: {e}")
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


@logger.catch
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
            except Exception as e:
                logger.warning(f"Connection To Account with proxy Error: {e}")
                client = TelegramClient(f"base/{session}", API_ID, API_HASH)

            try:
                await client.connect()
                if not await client.get_me():
                    await client.disconnect()
                    remove(f"base/{session}")
                else:
                    logger.info(f"{session} connected")
                    return client
            except Exception as e:
                logger.warning(f"Connection To Account Error 1: {e}")
                try:
                    await client.disconnect()
                    remove(f"base/{session}")
                except Exception as e:
                    logger.warning(f"Account Disconnect Error {e}")
                try:
                    await client.connect()
                    if not await client.get_me():
                        await client.disconnect()
                        remove(f"base/{session}")
                    else:
                        logger.info(f"{session} connected")
                        return client
                except Exception as e:
                    logger.warning(f"Connection To Account Error 2: {e}")
                    try:
                        await client.disconnect()
                        remove(f"base/{session}")
                    except Exception as e:
                        logger.warning(f"Account Disconnect Error {e}")
                    try:
                        await client.connect()
                        if not await client.get_me():
                            await client.disconnect()
                            remove(f"base/{session}")
                        else:
                            logger.info(f"{session} connected")
                            return client
                    except Exception as e:
                        logger.error(f"Connection To Account Error 3: {e}")
                        try:
                            await client.disconnect()
                            remove(f"base/{session}")
                        except Exception as e:
                            logger.warning(f"Account Disconnect Error {e}")
            return None


@logger.catch
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
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "https://t.me/joinchat/" in link:
            link = link.replace("https://t.me/joinchat/", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "t.me/+" in link:
            link = link.replace("t.me/+", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "t.me/joinchat/" in link:
            link = link.replace("t.me/joinchat/", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
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


@logger.catch
async def edit_message_loading(message: Message, percent=0):
    if percent == 1:
        try:
            await message.edit_text(text=LOADING[10])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.9:
        try:
            await message.edit_text(text=LOADING[9])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.8:
        try:
            await message.edit_text(text=LOADING[8])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.7:
        try:
            await message.edit_text(text=LOADING[7])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.6:
        try:
            await message.edit_text(text=LOADING[6])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.5:
        try:
            await message.edit_text(text=LOADING[5])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.4:
        try:
            await message.edit_text(text=LOADING[4])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.3:
        try:
            await message.edit_text(text=LOADING[3])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.2:
        try:
            await message.edit_text(text=LOADING[2])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")
    elif percent >= 0.1:
        try:
            await message.edit_text(text=LOADING[1])
        except Exception as e:
            logger.error(f"Edit Message Loading Error: {e}")


@logger.catch
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
        accounts = await get_list_of_numbers(link=channel_link, sub=True)
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
                    if task_status is not None and task_status != 200:
                        task_status = task_status[2]
                    else:
                        logger.info("Task #" + str(task_id) + " was stopped")
                        break
                    logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                    while task_status == 0:
                        await asyncio.sleep(60)
                        task_status = get_task_by_id(task_id)
                        if task_status is not None and task_status != 200:
                            task_status = task_status[2]
                    if task_status is None or task_status == 200:
                        logger.info("Task #" + str(task_id) + " was stopped")
                        break
                except Exception as e:
                    logger.error(f"Subscribe Public Channel Error: {e}")
                    break

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
                    logger.info(f"{phone.phone} вступил в {channel_link}")
                    try:
                        add_database(link=channel_link, phone=accounts[account_iter])
                        delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                    except Exception as e:
                        logger.error(f"Subscribe Public Channel Error: {e}")
                except Exception as e:
                    logger.error(f"Subscribe Public Channel Error: {e}")

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
                logger.warning(
                    f"Subscribe Public Chanel: Account's Connection Error ({accounts[account_iter]})"
                )

                current_count += 1
                done_percent = current_count / max_count
                if message is not None:
                    await edit_message_loading(message, done_percent)

            end = time.time()
            logger.info(f"Subscribe public Chanel Timer: {end - start}")
        return True
    else:
        return False


@logger.catch
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

    link_checker = await connect_to_account((await get_list_of_numbers())[0])
    channel = await link_checker(
        functions.messages.CheckChatInviteRequest(channel_link)
    )
    try:
        channel_id = str(channel.title)
    except Exception as e:
        channel_id = str(channel.chat.title)
    link_checker.disconnect()

    if accounts is None:
        accounts = await get_list_of_numbers(link=channel_id, sub=True)
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
                if task_status is not None and task_status != 200:
                    task_status = task_status[2]
                else:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
                logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None and task_status != 200:
                        task_status = task_status[2]
                if task_status is None or task_status == 200:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
            except Exception as e:
                logger.error(f"Subscribe Private Channel Error: {e}")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(ImportChatInviteRequest(channel_link))
                logger.info(f"{phone.phone} вступил в {channel_id}")
                try:
                    add_database(phone=accounts[account_iter], link=channel_id)
                except Exception as e:
                    logger.error(f"Subscribe Private Channel add_database Error: {e}")
                try:
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except Exception as e:
                    logger.error(
                        f"Subscribe Private Channel delete_task_phone Error: {e}"
                    )
            except Exception as e:
                logger.error(f"Subscribe Private Channel Error: {e}")

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
            logger.warning(
                f"Subscribe Private Chanel: Account's Connection Error ({accounts[account_iter]})"
            )

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

    return True


@logger.catch
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


@logger.catch
async def leave_channel(
    args,
    accounts=None,
    last_iter=True,
    prev_message=None,
    loading_args=None,
    task_id=None,
    unsubscribe_percent_timing=False,
):
    if "t.me/+" in args[0] or unsubscribe_percent_timing:
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


@logger.catch
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
        accounts = await get_list_of_numbers(link=channel_link, sub=False)
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
                if task_status is not None and task_status != 200:
                    task_status = task_status[2]
                else:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
                logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None and task_status != 200:
                        task_status = task_status[2]
                if task_status is None or task_status == 200:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
            except Exception as e:
                logger.error(f"Leave Public Channel Error: {e}")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(LeaveChannelRequest(channel_link))
                logger.info(f"{phone.phone} покинул {channel_link}")
                try:
                    delete_phone_link(link=channel_link, phone=accounts[account_iter])
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except Exception as e:
                    logger.error(f"Leave Public Channel Error: {e}")
            except Exception as e:
                logger.error(f"Leave Public Channel Error: {e}")

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
            logger.warning(
                f"Leave Public Chanel: Account's Connection Error ({accounts[account_iter]})"
            )

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)

    return True


@logger.catch
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

    if "t.me/+" in channel_link:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace("https://t.me/+", "")
        elif "http://t.me/+" in channel_link:
            channel_link = channel_link.replace("http://t.me/+", "")
        elif "t.me/+" in channel_link:
            channel_link = channel_link.replace("t.me/+", "")
        link_checker = await connect_to_account((await get_list_of_numbers())[0])
        channel = await link_checker(
            functions.messages.CheckChatInviteRequest(channel_link)
        )
        try:
            channel_id = str(channel.title)
        except Exception as e:
            channel_id = str(channel.chat.title)
        link_checker.disconnect()
    else:
        channel_id = channel_link

    if accounts is None:
        accounts = await get_list_of_numbers(link=channel_id, sub=False)
        shuffle(accounts)
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
                if task_status is not None and task_status != 200:
                    task_status = task_status[2]
                else:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
                logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None and task_status != 200:
                        task_status = task_status[2]
                if task_status is None or task_status == 200:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
            except Exception as e:
                logger.error(f"Leave Private Channel Error: {e}")

        account = await connect_to_account(accounts[account_iter])
        if account is not None:
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                try:
                    # chat = await account.get_entity(channel_link)
                    # chat_title = chat.title
                    async for dialog in account.iter_dialogs():
                        if dialog.title == channel_id:
                            await dialog.delete()
                            logger.info(f"{phone.phone} покинул {channel_id}")
                            break
                except Exception as e:
                    logger.error(f"Leave Private Channel Error: {e}")
                try:
                    delete_phone_link(link=channel_id, phone=accounts[account_iter])
                    delete_task_phone(id_task=task_id, phone=accounts[account_iter])
                except Exception as e:
                    logger.error(f"Leave Private Channel Error: {e}")
            except Exception as e:
                logger.error(f"Leave Private Channel Error: {e}")

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
            logger.warning(
                f"Leave Private Chanel: Account's Connection Error ({accounts[account_iter]})"
            )
    return True


@logger.catch
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
        accounts = await get_list_of_numbers()
        shuffle(accounts)
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
                if task_status is not None and task_status != 200:
                    task_status = task_status[2]
                else:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
                logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None and task_status != 200:
                        task_status = task_status[2]
                if task_status is None or task_status == 200:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
            except Exception as e:
                logger.error(f"View Post Error: {e}")

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
                except Exception as e:
                    logger.error(f"View Post Error: {e}")
                logger.info(f"{phone.phone} посмторел посты в {channel_link}")
            except Exception as e:
                logger.error(f"View Post Error: {e}")

            account.disconnect()

            current_count += 1
            done_percent = current_count / max_count
            await edit_message_loading(message, done_percent)

            if not (account_iter + 1 == count_accounts and last_iter):
                del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                new_delay = delay + random.randint(-del_delay, del_delay)
                await asyncio.sleep(new_delay)
        else:
            logger.warning(
                f"View Post: Account's Connection Error ({accounts[account_iter]})"
            )

            current_count += 1
            done_percent = current_count / max_count
            if message is not None:
                await edit_message_loading(message, done_percent)
    return True


@logger.catch
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
        accounts = await get_list_of_numbers()
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
                if task_status is not None and task_status != 200:
                    task_status = task_status[2]
                else:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
                logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
                while task_status == 0:
                    await asyncio.sleep(60)
                    task_status = get_task_by_id(task_id)
                    if task_status is not None and task_status != 200:
                        task_status = task_status[2]
                if task_status is None or task_status == 200:
                    logger.info("Task #" + str(task_id) + " was stopped")
                    break
            except Exception as e:
                logger.error(f"Click On Button Error: {e}")

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
                except Exception as e:
                    logger.error(f"Click On Button Error: {e}")

                logger.info(f"{phone.phone} нажал на кнопку в {channel_link}")

                account.disconnect()

                current_count += 1
                done_percent = current_count / max_count
                await edit_message_loading(edit_message, done_percent)

                if not (account_iter + 1 == count and last_iter):
                    del_delay = math.floor(delay * RANDOM_PERCENT / 100)
                    new_delay = delay + random.randint(-del_delay, del_delay)
                    await asyncio.sleep(new_delay)
            else:
                logger.warning(
                    f"Click Ob Button: Account's Connection Error ({accounts[account_iter]})"
                )
        except Exception as e:
            logger.error(f"Click On Button Error: {e}")
    return True
