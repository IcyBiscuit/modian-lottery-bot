import asyncio
import random
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, List

import lottery.Core as Core
import lottery.utils.DBUtil as DBUtil
from configs.LotteryConfig import config
from lottery.Score import calculate_score
import templates.lottery.LotteryTemplate as templates

baseMoney = Decimal(config['baseMoney'])


async def lottery(orders: List[Dict[str, Any]]) -> List[str]:
    '''
    抽卡
    传入订单列表信息
    返回解析后的抽卡结果
    :param orders: 订单信息列表
    :returns: 解析后的抽卡结果 字符串列表
    '''
    lottery_results = await get_lottery_results(orders)
    msgs = lottery_results_resolver(lottery_results)
    return msgs


async def get_lottery_results(
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
        get_lottery_results_task(order)) for order in orders]
    # 执行并发任务
    await asyncio.gather(*tasks)

    # 返回格式: results: List[Dict[str, Any]]
    return [task.result() for task in tasks]


async def get_lottery_results_task(order: Dict[str, Any]):
    '''
    根据订单信息进行抽卡流程
    结果中
    金额不足则为空列表,
    金额过抽卡线则为抽卡结果列表
    '''
    # 获取摩点id 字符串格式
    user_id = str(order['user_id'])
    # 获得集资金额
    money = Decimal(order['backer_money']).quantize(
        Decimal('.01'), rounding=ROUND_HALF_UP)
    if money < baseMoney:
        # results.append({'score': 0, 'result': []})
        return {'score': 0, 'result': []}
    else:
        # 获取抽卡结果列表
        card_results = Core.lottery(money)
        # 根据结果列表计算积分
        score = await calculate_score(user_id, card_results)
        # 结果写入结果列表
        # results.append({
        #     'score': score,
        #     'result': card_result
        # })

        # 数据入库
        # 抽卡数据与积分数据入库
        await DBUtil.insert_lottery_data(order, card_results)
        return {
            'score': score,
            'result': card_results
        }


def lottery_results_resolver(results: List[Dict[str, Any]]) -> List[str]:
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
            score = result['score']
            cards_result = cards_data_resolver(cards)
            msg = templates.lottery_result_template(card, cards_result, score)
            msgs.append(msg)
    return msgs


def cards_data_resolver(cards: List[tuple]) -> str:
    '''
    累计次数
    解析抽卡结果为文字
    '''
    cards_dict = {}
    for card in cards:
        name = card[2]
        if name not in cards_dict:
            cards_dict[name] = 1
        else:
            cards_dict[name] += 1
    msg = templates.card_template(cards_dict)
    return msg
