import aiomysql
import asyncio
from db.config import config


async def creatPool() -> aiomysql.Pool:
    pool = await aiomysql.create_pool(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        db=config['db'],
        autocommit=False)
    return pool


loop = asyncio.get_event_loop()
pool: aiomysql.Pool = loop.run_until_complete(creatPool())
