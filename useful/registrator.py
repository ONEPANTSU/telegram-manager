from aiogram import Dispatcher

from handlers.main import main_handlers
from handlers.activity import activity_handler


def register_handlers(dp: Dispatcher):
    main_handlers.register_main_handlers(dp=dp)
    activity_handler.register_activity_handlers(dp=dp)