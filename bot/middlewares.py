from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from db import User, Statistic


class StatisticMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = await User.get_or_create(message.from_user.id)
        await Statistic.create(user.id, message.text)
