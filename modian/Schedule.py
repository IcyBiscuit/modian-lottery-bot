import asyncio
from itertools import chain
from typing import Dict, List

from aiohttp import ClientSession

import bot.CQBot as bot
import modian.utils.MessageHandler as MessageHandler
import templates.modian.ModianTemplate as templates
from configs.ModianConfig import config
from modian.utils.DBUtil import get_latest_time

loop = asyncio.get_event_loop()


async def init_latest_time() -> Dict[str, str]:
    latest_time = {}
    for pro_id in config['pro_ids']:
        latest_time[pro_id] = ''

    r: List[tuple] = await get_latest_time()
    for o in r:
        pro_id, pay_date_time = o
        if pay_date_time is not None:
            latest_time[pro_id] = pay_date_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            latest_time[pro_id] = ''
    return latest_time

latest_time: Dict[str, str] = loop.run_until_complete(init_latest_time())


async def daily_schedule():
    """
    日常集资播报计划任务
    """
    daily_pro_ids = config['daily']['pro_ids']
    async with ClientSession() as session:
        try:
            query_tasks = [asyncio.create_task(
                MessageHandler.get_new_orders(
                    pro_id, latest_time, session=session))
                for pro_id in daily_pro_ids]

            await asyncio.gather(*query_tasks)
            msgs = resolve_daily_result(query_tasks)
            if len(msgs) > 0:
                await send_msg(msgs)
        except asyncio.TimeoutError as e:
            print(f"订单查询超时, {e.with_traceback()}")


async def pk_schedule():
    """
    集资pk播报计划任务
    包含自家新订单播报
    以及对家集资详情播报
    :return None
    """
    pro_id = config['pk']['me']
    vs_list = config['pk']['vs']
    try:
        async with ClientSession() as session:
            order_task = asyncio.create_task(
                MessageHandler.get_new_orders(
                    pro_id, latest_time, session=session))

            vs_info_task = asyncio.create_task(
                MessageHandler.get_active_orders(
                    vs_list, session=session))

            await asyncio.gather(order_task, vs_info_task)

            msgs = resolve_pk_result(order_task, vs_info_task)
            if len(msgs) > 0:
                await send_msg(msgs)
    except asyncio.TimeoutError as e:
        print(f"订单查询超时, {e.with_traceback()}")


def resolve_daily_result(results: List[asyncio.Task]) -> List[str]:
    """
    取出异步任务结果
    将结果变为一维列表
    """
    # for result in results:
    #     print(result.result())
    return list(chain(*[result.result() for result in results]))


def resolve_pk_result(results: asyncio.Task,
                      vs_info_task: asyncio.Task) -> List[str]:
    """
    取出异步任务结果
    并将结果解析拼接成消息字符串
    """
    orders: List[str] = results.result()
    vs_info: str = vs_info_task.result()
    return [templates.pk_template(order, vs_info) for order in orders]


async def send_msg(msgs: list):
    """
    发送消息到QQ群
    """
    await asyncio.gather(
        *[asyncio.create_task(bot.send_msg(msg)) for msg in msgs])
