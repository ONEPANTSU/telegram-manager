from aiogram import Dispatcher

from handlers.img_creating import img_creating_handlers
from handlers.main import main_handlers


def register_handlers(dp: Dispatcher):
    main_handlers.register_main_handlers(dp=dp)
    img_creating_handlers.register_img_creating_handlers(dp=dp)