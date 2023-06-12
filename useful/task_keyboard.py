from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from handlers.activity.database import count_task_phone, get_tasks
from texts.buttons import BUTTONS
from texts.messages import LOADING, MESSAGES
from useful.callbacks import delete_task_callback, stop_task_callback, task_callback
from useful.instruments import bot


def get_task_keyboard(task_list, page: int = 0) -> InlineKeyboardMarkup:
    has_next_page = len(task_list) > page + 1

    page_num_button = create_page_num_button(page, len(task_list))
    delete_button = create_delete_button(page, task_list)
    stop_button = create_stop_button(page, task_list)
    back_button = create_back_button(page)
    next_button = create_next_button(page)
    return create_task_keyboard(
        back_button,
        delete_button,
        stop_button,
        has_next_page,
        next_button,
        page,
        page_num_button,
    )


def create_task_keyboard(
    back_button,
    delete_button,
    stop_button,
    has_next_page,
    next_button,
    page,
    page_num_button,
):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(page_num_button)
    keyboard.row(delete_button)
    keyboard.row(stop_button)
    return add_page_buttons(has_next_page, keyboard, back_button, next_button, page)


def add_page_buttons(has_next_page, keyboard, back_button, next_button, page):
    if page != 0:
        if has_next_page:
            keyboard.row(back_button, next_button)
        else:
            keyboard.row(back_button)
    elif has_next_page:
        keyboard.row(next_button)
    return keyboard


def create_next_button(page):
    return InlineKeyboardButton(
        text=BUTTONS["next"],
        callback_data=task_callback.new(page=page + 1),
    )


def create_back_button(page):
    return InlineKeyboardButton(
        text=BUTTONS["prev"],
        callback_data=task_callback.new(page=page - 1),
    )


def create_delete_button(page, task_list):
    return InlineKeyboardButton(
        text=BUTTONS["delete_task"],
        callback_data=delete_task_callback.new(task_id=task_list[page][0], page=0),
    )


def create_stop_button(page, task_list):
    status = task_list[page][2]
    if status == 1:
        return InlineKeyboardButton(
            text=BUTTONS["stop_task"],
            callback_data=stop_task_callback.new(task_id=task_list[page][0], page=page),
        )
    elif status == 0:
        return InlineKeyboardButton(
            text=BUTTONS["play_task"],
            callback_data=stop_task_callback.new(task_id=task_list[page][0], page=page),
        )


def create_page_num_button(page, task_list_len):
    return InlineKeyboardButton(
        text=f"{page + 1} / {task_list_len}", callback_data="dont_click_me"
    )


async def task_index(message: Message, task_list):
    if len(task_list) != 0:
        await create_task_page(
            chat_id=message.chat.id,
            task_list=task_list,
            page=0,
        )
    else:
        await bot.send_message(chat_id=message.chat.id, text=MESSAGES["empty_task"])


async def refresh_pages(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    task_list = get_tasks()
    await update_page(page, task_list, query)


async def update_page(page, task_list, query):
    if len(task_list) != 0:
        await edit_task_page(query=query, task_list=task_list, page=page)
    else:
        await query.message.edit_text(text=MESSAGES["empty_task"], reply_markup=None)


async def edit_task_page(query: CallbackQuery, task_list, page):
    keyboard, task_info = get_page_content(page, task_list)
    await query.message.edit_text(
        text=task_info,
        reply_markup=keyboard,
    )


async def create_task_page(chat_id, task_list, page):
    keyboard, task_info = get_page_content(page, task_list)
    await bot.send_message(
        chat_id=chat_id,
        text=task_info,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def get_page_content(page, task_list):
    task_info = create_task_info(task_list[page])
    keyboard = get_task_keyboard(task_list=task_list, page=page)
    return keyboard, task_info


def create_task_info(task_data):
    loading = edit_message_loading(task_data)
    task_info = MESSAGES["show_task"].format(task_id=task_data[0], loading=loading)
    return task_info


def edit_message_loading(task_data):
    current_count = count_task_phone(task_data[0])
    percent = (task_data[1] - current_count[0]) / task_data[1]
    if percent == 1:
        return LOADING[10]
    elif percent >= 0.9:
        return LOADING[9]
    elif percent >= 0.8:
        return LOADING[8]
    elif percent >= 0.7:
        return LOADING[7]
    elif percent >= 0.6:
        return LOADING[6]
    elif percent >= 0.5:
        return LOADING[5]
    elif percent >= 0.4:
        return LOADING[4]
    elif percent >= 0.3:
        return LOADING[3]
    elif percent >= 0.2:
        return LOADING[2]
    elif percent >= 0.1:
        return LOADING[1]
    else:
        return LOADING[0]
