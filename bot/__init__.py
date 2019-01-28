import asyncio

from typing import Optional, Union

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import base

import config
import db

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.middlewares import StatisticMiddleware


class DonnuBot(Bot):
    def __init__(self, token: base.String,
                 loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
                 connections_limit: Optional[base.Integer] = None, proxy: Optional[base.String] = None,
                 proxy_auth: Optional[aiohttp.BasicAuth] = None, validate_token: Optional[base.Boolean] = True,
                 parse_mode=None):
        super().__init__(token, loop, connections_limit, proxy, proxy_auth, validate_token, parse_mode)

        # Prepare database before bot start
        asyncio.get_event_loop().run_until_complete(db.prepare_db())


bot = DonnuBot(token=config.TELEGRAM_API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(StatisticMiddleware())

import bot.handler
