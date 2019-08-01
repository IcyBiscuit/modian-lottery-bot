import asyncio

import aiomysql

from configs.DBConfig import config


async def creat_pool() -> aiomysql.Pool:
    pool = await aiomysql.create_pool(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        db=config['db'],
        autocommit=False)
    return pool


loop = asyncio.get_event_loop()
pool: aiomysql.Pool = loop.run_until_complete(creat_pool())
