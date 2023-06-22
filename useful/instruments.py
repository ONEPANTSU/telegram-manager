import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from config import BOT_TOKEN

storage = MemoryStorage()
loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=storage)
code = {}
clients = {}

logger.add(
    "TGM.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10 MB",
    compression="zip",
)

callback_dict = {}  # {"from_user": ["link", count]}
