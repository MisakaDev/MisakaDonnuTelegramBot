import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from db import User, Statistic


class StatisticMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = await User.get_or_create(message.from_user.id)
        await Statistic.create(user.id, message.text)


class UpdateMiddleware(BaseMiddleware):
    def __init__(self, user_hint):
        super().__init__()
        self._user_hint = user_hint

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await message.reply(self._user_hint)
        raise CancelHandler()
