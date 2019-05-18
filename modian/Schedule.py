import asyncio
from itertools import chain
from typing import Dict, List

from aiohttp import ClientSession

import bot.CQBot as bot
import modian.utils.MessageHandler as MessageHandler
from modian.configs.ModianConfig import config
from modian.utils.DBUtil import getLatestTime


async def initLatestTime() -> Dict[str, str]:
    latestTime = {}
    for pro_id in config['pro_ids']:
        latestTime[pro_id] = ''

    r: tuple = await getLatestTime()
    for o in r:
        pro_id, pay_date_time = o
        if pay_date_time is not None:
            latestTime[pro_id] = pay_date_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            latestTime[pro_id] = ''
    return latestTime

loop = asyncio.get_event_loop()
latestTime: dict = asyncio.get_event_loop().run_until_complete(initLatestTime())


async def dailySchedule():
    '''
    日常集资播报计划任务
    '''
    dailyProIds = config['daily']['pro_ids']
    # latestTime = await initLatesproId
    async with ClientSession() as session:
        try:
            # tasks = []
            # for pro_id in dailyProIds:
            #     tasks.append(
            #         asyncio.create_task(MessageHandler.getNewOrders(
            #             pro_id, latestTime[pro_id], session=session))
            #     )
            queryTasks = [asyncio.create_task(
                MessageHandler.getNewOrders(
                    pro_id, latestTime, session=session))
                for pro_id in dailyProIds]

            await asyncio.wait(queryTasks)

            msgs = parseDailyResult(queryTasks)
            if len(msgs) > 0:
                await sendMsg(msgs)
        except asyncio.TimeoutError as e:
            print(f"订单查询超时, {e}")


async def pkSchedule():
    '''
    集资pk播报计划任务
    包含自家新订单播报
    以及对家集资详情播报
    '''
    proId = config['pk']['me']
    vsList = config['pk']['vs']
    # latestTime = await initLatestTime()
    try:
        async with ClientSession() as session:
            orderTask = asyncio.create_task(
                MessageHandler.getNewOrders(
                    proId, latestTime, session=session))

            vsInfoTask = asyncio.create_task(
                MessageHandler.getActiveOrders(
                    vsList, session=session))

            await asyncio.gather(orderTask, vsInfoTask)

            msgs = parsePkResult(orderTask, vsInfoTask)
            if len(msgs) > 0:
                await sendMsg(msgs)
    except asyncio.TimeoutError as e:
        print(f"订单查询超时, {e}")

        # print(orders)
        # print(vsInfo)


def parseDailyResult(results: List[asyncio.Task]) -> List[str]:
    '''
    取出异步任务结果
    将结果变为一维列表
    '''
    # for result in results:
    #     print(result.result())
    return list(chain(*[result.result() for result in results]))


def parsePkResult(results: asyncio.Task, vsInfoTask: asyncio.Task) -> List[str]:
    '''
    取出异步任务结果
    并将结果解析拼接成消息字符串
    '''
    orders: List[str] = results.result()
    vsInfo: str = vsInfoTask.result()
    split = "----------------"
    return [f"{order}\n{split}\n对家详情:\n{vsInfo}" for order in orders]


async def sendMsg(msgs: list):
    '''
    发送消息到QQ群
    '''
    await asyncio.wait(
        [asyncio.create_task(bot.sendMsg(msg))
            for msg in msgs])
