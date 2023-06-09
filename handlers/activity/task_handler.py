from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from handlers.activity.database import delete_task, get_tasks, change_task_status
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.callbacks import task_callback, confirm_delete_task_callback, delete_task_callback, stop_task_callback
from useful.keyboards import confirm_deleting_task_keyboard
from useful.task_keyboard import refresh_pages, create_task_page


async def task_page_handler(query: CallbackQuery, callback_data: dict):
    await refresh_pages(query=query, callback_data=callback_data)


async def delete_task_handler(query: CallbackQuery, callback_data: dict):
    id_task = callback_data["task_id"]
    await query.message.edit_text(text=MESSAGES["confirm_deleting_task"],
                                  reply_markup=confirm_deleting_task_keyboard(id_task))


async def delete_confirm_query(query: CallbackQuery, callback_data: dict):
    answer = callback_data["answer"]
    id_task = callback_data["task_id"]
    chat_id = query.message.chat.id
    if answer == BUTTONS["yes_confirm"]:
        delete_task(id_task)  # удаляем задачу
        task_list = get_tasks()
        if len(task_list) != 0:
            await create_task_page(
                chat_id=chat_id,
                task_list=task_list,
                page=0,
            )
        else:
            await query.message.edit_text(text=MESSAGES["empty_task"], reply_markup=None)
    elif answer == BUTTONS["no_confirm"]:  # Не подтверждено
        await query.message.edit_text(text=MESSAGES["confirm_no"], reply_markup=None)


async def stop_task_handler(query: CallbackQuery, callback_data: dict):
    id_task = callback_data["task_id"]
    page = int(callback_data["page"])
    chat_id = query.message.chat.id
    task_list = get_tasks()
    status = task_list[page][2]
    if status == 1:
        change_task_status(id_task, 0)
    elif status == 0:
        change_task_status(id_task, 1)
    await refresh_pages(query=query, callback_data=callback_data)


def register_task_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        task_page_handler, task_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_task_handler, delete_task_callback.filter()
    )
    dp.register_callback_query_handler(
        stop_task_handler, stop_task_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_confirm_query, confirm_delete_task_callback.filter()
    )
