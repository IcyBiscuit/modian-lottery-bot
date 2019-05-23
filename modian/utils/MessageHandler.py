import asyncio
from typing import Any, Dict, List

from aiohttp import ClientSession

import modian.utils.ModianUtil as modian
import templates.modian.ModianTemplate as templates
from lottery.Lottery import lottery
from modian.utils.DBUtil import insertNewOrders

url_prefix = "https://m.modian.com/project/"


async def getActiveOrders(pro_ids: list,
                          session: ClientSession = None) -> str:
    '''
    返回正在进行的集资详情信息
    '''
    orders = await modian.getDetail(pro_ids, session)
    return '\n'.join([programmeDetailResolver(order)
                      for order in orders['data']])


async def getRanks(pro_id: str, type: int = 1, limit: int = 5,
                   session: ClientSession = None) -> str:
    '''
    返回集资榜单信息
    :param limit: 需要显示的排名 0为不限制
    :returns: 返回前limit名的排名 长度不足则全部返回
    '''
    resp = await modian.getRankings(pro_id, type=type, session=session)

    ranking: List[Dict[str, Any]] = resp['data']
    if limit != 0 and len(ranking) > limit:
        ranking = ranking[:limit]

    msg = templates.rankingTemplate(ranking, type)
    return msg


async def getNewOrders(proId: str,
                       lastTimeDict: Dict[str, str],
                       session: ClientSession = None) -> str:
    '''
    获取并过滤新订单
    '''
    detailTask: asyncio.Task = asyncio.create_task(
        modian.getDetailOne(proId, session=session))

    ordersTask: asyncio.Task = asyncio.create_task(
        modian.getSortedOrders(proId, session=session))

    rankingTask: asyncio.Task = asyncio.create_task(
        getRanks(proId, session=session))

    await asyncio.gather(detailTask, ordersTask, rankingTask)

    detail = detailTask.result()
    orders = ordersTask.result()
    ranking = rankingTask.result()

    if(detail['status'] == 2):
        print('集资详情信息获取错误')
    if(orders['status'] == 2):
        print('集资订单信息获取错误')

    # 获取上一次的最新时间
    lastTime: str = lastTimeDict[proId]
    # 更新订单最新时间
    lastTimeDict[proId] = orders['data'][0]['pay_success_time']

    newOrders: List[Dict[str, Any]] = []
    if len(orders['data']) > 0:
        orderFilter(orders['data'], newOrders, lastTime)
    # 全为新订单, 则多查询一页
    if lastTime != '' and len(orders['data']) == len(newOrders):
        orders = await modian.getSortedOrders(proId, page=2, session=session)
        orderFilter(orders['data'], newOrders, lastTime)

    await insertNewOrders(proId, newOrders)

    # 不需要抽卡可以把这里注释掉
    lotteryMsgs = await lottery(newOrders)
    return ordersAndLotteryResultsResolver(newOrders, detail['data'][0],
                                           lotteryMsgs, ranking)

    # 此处是不抽卡的处理逻辑
    # msgs = orderMessagesResolver(newOrders, detail['data'][0], ranking)
    # return msgs


def programmeDetailResolver(detail: Dict[str, Any]) -> str:
    '''
    将集资项目进度详情解析成字符串
    '''
    msg = templates.programmeDetailTemplate(detail)
    return msg


def orderFilter(orders: List[Dict[str, Any]],
                newOrders: List[Dict[str, Any]],
                lastTime: str = '') -> List[Dict[str, Any]]:
    '''
    根据参数中的最新时间过滤订单
    使用字符串比较
    '''
    for order in orders:
        if lastTime == '' or order['pay_success_time'] > lastTime:
            newOrders.append(order)


def orderMessagesResolver(orders: List[Dict[str, Any]],
                          detail: Dict[str, Any],
                          ranking: str = '') -> List[str]:
    '''
    将新订单结果解析成消息字符串
    '''
    msgs: List[str] = [templates.orderTemplate(order) +
                       templates.programmeDetailTemplate(detail) +
                       ranking
                       for order in orders]
    return msgs


def ordersAndLotteryResultsResolver(ordersResults: List[Dict[str, Any]],
                                    detail: Dict[str, Any],
                                    lotteryResults: List[str],
                                    ranking: str = '') -> List[str]:
    '''
    组合集资结果以及抽卡结果
    '''
    msgs: List[str] = []
    for i in range(len(ordersResults)):
        order = ordersResults[i]
        cards = lotteryResults[i]

        msg = templates.orderTemplate(order)\
            + templates.programmeDetailTemplate(detail)\
            + cards\
            + ranking
        msgs.append(msg)
    return msgs
