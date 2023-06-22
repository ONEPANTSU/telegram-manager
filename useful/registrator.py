from aiogram import Dispatcher

from handlers.activity import activity_handler
from handlers.main import main_handlers
from handlers.task import task_handler
from handlers.users import users_handler


def register_handlers(dp: Dispatcher):
    main_handlers.register_main_handlers(dp=dp)
    activity_handler.register_activity_handlers(dp=dp)
    task_handler.register_task_handlers(dp=dp)
    users_handler.register_users_handlers(dp=dp)
