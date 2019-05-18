from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, List

import lottery.Core as Core
from lottery.configs.config import config
from lottery.Score import calculateScore
import lottery.utils.DBUtil as DBUtil
import asyncio
import random

baseMoney = Decimal(config['baseMoney'])


async def lottery(orders: List[Dict[str, Any]]) -> List[str]:
    '''
    抽卡
    传入订单列表信息
    返回解析后的抽卡结果
    :param orders: 订单信息列表
    :returns: 解析后的抽卡结果 字符串列表
    '''
    lotteryResults = await getLotteryResults(orders)
    msgs = lotteryResultsParser(lotteryResults)
    return msgs


async def getLotteryResults(
        orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    '''
    根据订单信息进行抽卡流程
    :param orders: 订单列表
    :returns: 整个新订单列表的抽卡结果
    '''
    # 订单为空直接返回空列表
    if len(orders) == 0:
        return []

    # 不为空 构造任务并发处理订单信息
    tasks: List[asyncio.Task] = [asyncio.create_task(
        getLotteryResultsTask(order)) for order in orders]
    # 执行并发任务
    await asyncio.wait(tasks)

    # 返回格式: results: List[Dict[str, Any]]
    return [task.result() for task in tasks]


async def getLotteryResultsTask(order: Dict[str, Any]):
    '''
    根据订单信息进行抽卡流程
    结果中
    金额不足则为空列表,
    金额过抽卡线则为抽卡结果列表
    '''
    # 获取摩点id
    userId = str(order['user_id'])
    # 获得集资金额
    money = Decimal(order['backer_money']).quantize(
        Decimal('.01'), rounding=ROUND_HALF_UP)
    if money < baseMoney:
        # results.append({'score': 0, 'result': []})
        return {'score': 0, 'result': []}
    else:
        # 获取抽卡结果列表
        cardResult = Core.lottery(money)
        # 根据结果列表计算积分
        score = await calculateScore(userId, cardResult)
        # 结果写入结果列表
        # results.append({
        #     'score': score,
        #     'result': cardResult
        # })

        # 数据入库
        # 抽卡数据与积分数据入库
        await DBUtil.insertLotteryData(order, cardResult)
        return {
            'score': score,
            'result': cardResult
        }


def lotteryResultsParser(results: List[Dict[str, Any]]) -> List[str]:
    '''
    将抽卡结果解析为文字消息
    '''
    '''
    results=[
        {
            'score':,
            'result':[]
        }
    ]
    '''
    msgs = []
    for result in results:
        cards: List[tuple] = result['result']
        if len(cards) == 0:
            msgs.append('')
        else:
            # 解析抽卡结果
            # 本次积分: {积分} 获得卡牌:
            # {卡牌名称}×{数量}
            card = random.choice(cards)
            msg = f"恭喜获得新卡!\n[CQ:image,file={card[3]}]\n"
            score = result['score']
            msg += f"本次积分: {score} 获得卡牌:\n{parseCardsData(cards)}"
            print(msg)
            msgs.append(msg)
    return msgs


def parseCardsData(cards: List[tuple]) -> str:
    '''
    累计次数
    解析抽卡结果为文字
    '''
    cardsDict = {}
    for card in cards:
        name = card[2]
        if name not in cardsDict:
            cardsDict[name] = 1
        else:
            cardsDict[name] += 1
    msg = ""
    for name, count in cardsDict.items():
        msg += f"{name} × {count}\n"
    return msg
