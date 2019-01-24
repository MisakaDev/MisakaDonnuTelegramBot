from bot import dp
from db import db

import asyncio
from aiogram import executor

import logging

logging.basicConfig(level=logging.INFO)


async def prepare_db():
    from db.config import DB_HOST, DB_NAME, DB_USER_LOGIN, DB_USER_PASSWORD

    await db.set_bind('postgresql://{}:{}@{}/{}'.format(DB_USER_LOGIN,
                                                        DB_USER_PASSWORD,
                                                        DB_HOST,
                                                        DB_NAME)
                      )
    await db.gino.create_all()


if __name__ == '__main__':
    asyncio.get_event_loop().create_task(prepare_db())
    executor.start_polling(dp, skip_updates=True)
