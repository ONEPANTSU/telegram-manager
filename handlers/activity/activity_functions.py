import asyncio
from os import remove, walk
from random import shuffle

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from telethon import TelegramClient, functions
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from config import API_HASH, API_ID
from handlers.main.main_functions import get_main_keyboard
from handlers.users.users_handler import add_user_button
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot
from useful.keyboards import activity_keyboard


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


async def get_accounts_len():
    accounts = await get_accounts()
    accounts_len = len(accounts)
    disconnect_all(accounts)
    return accounts_len


async def subscribe_public_channel(message: Message, channel_link, count, delay):
    accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        shuffle(accounts)
        for account in range(count):
            account = accounts[account]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(JoinChannelRequest(channel_link))
                print(f"{phone.phone} вступил в {channel_link}")
            except Exception as error:
                print(str(error))
            await asyncio.sleep(delay)
        disconnect_all(accounts)
        return True
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["count_user_error"].format(count=accounts_len),
            reply_markup=get_main_keyboard(),
        )
        disconnect_all(accounts)
        return False


async def subscribe_private_channel(message: Message, channel_link, count, delay):
    if "https://t.me/+" in channel_link:
        channel_link = channel_link.replace("https://t.me/+", "")
    elif "https://t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("https://t.me/joinchat/", "")
    elif "t.me/joinchat/" in channel_link:
        channel_link = channel_link.replace("t.me/joinchat/", "")
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["link_error"],
        )

    accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        shuffle(accounts)
        for account in range(count):
            account = accounts[account]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(ImportChatInviteRequest(channel_link))
                print(f"{phone.phone} вступил в {channel_link}")
            except Exception as error:
                print(str(error))
            await asyncio.sleep(delay)
        disconnect_all(accounts)
        return True
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["count_user_error"].format(count=accounts_len),
        )
        disconnect_all(accounts)
        return False


async def leave_public_channel(message: Message, channel_link, count, delay):
    accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        for account in range(count):
            account = accounts[account]
            phone = await account.get_me()
            try:
                await account(
                    functions.account.UpdateStatusRequest(offline=False)
                )  # Go to online
                await account(LeaveChannelRequest(channel_link))
                print(f"{phone.phone} покинул {channel_link}")
            except Exception as error:
                print(str(error))
            await asyncio.sleep(delay)
        disconnect_all(accounts)
        return True
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["count_user_error"].format(count=accounts_len),
        )
        disconnect_all(accounts)
        return False


async def leave_private_channel(message: Message, channel_link, count, delay):
    accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace("https://t.me/+", "https://t.me/joinchat/")
        for account in range(count):
            account = accounts[account]
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
            await asyncio.sleep(delay)
        disconnect_all(accounts)
        return True
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["count_user_error"].format(count=accounts_len),
        )
        disconnect_all(accounts)
        return False


async def view_post(message: Message, channel_link, last_post_id, count_posts, count_accounts, delay):
    accounts = await get_accounts()
    accounts_len = len(accounts)
    if count_accounts <= accounts_len:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace("https://t.me/+", "https://t.me/joinchat/")
        for account in range(count_accounts):
            account = accounts[account]
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
            await asyncio.sleep(delay)
        disconnect_all(accounts)
        return True
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["count_user_error"].format(count=accounts_len),
        )
        disconnect_all(accounts)
        return False


async def click_on_button(message: Message, channel_link, post_id, position, count, delay):
    accounts = await get_accounts()
    accounts_len = len(accounts)
    if count <= accounts_len:
        if "https://t.me/+" in channel_link:
            channel_link = channel_link.replace("https://t.me/+", "https://t.me/joinchat/")
        for account in range(count):
            account = accounts[account]
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
            await asyncio.sleep(delay)
        disconnect_all(accounts)
        return True
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["count_user_error"].format(count=accounts_len),
        )
        disconnect_all(accounts)
        return False
