from aiogram import Bot, Dispatcher
from bot.config import TELEGRAM_API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.middlewares import StatisticMiddleware


bot = Bot(token=TELEGRAM_API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(StatisticMiddleware())

import bot.handler
