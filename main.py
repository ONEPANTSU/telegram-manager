from aiogram import executor

from useful.instruments import dp, logger, loop
from useful.registrator import register_handlers

register_handlers(dp=dp)

if __name__ == "__main__":
    executor.start_polling(dp, loop=loop)
