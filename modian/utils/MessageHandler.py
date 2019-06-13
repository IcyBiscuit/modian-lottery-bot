import asyncio
from typing import Any, Dict, List

from aiohttp import ClientSession

import modian.utils.ModianUtil as modian
import templates.modian.ModianTemplate as templates
from modian.handlers.AbstractOrderHandler import AbstractOrderHandler
from modian.handlers.ModianDailyAndLotteryHandler import \
    ModianDailyAndLotteryHandler
from modian.utils.DBUtil import insert_new_orders

url_prefix = "https://m.modian.com/project/"
handler: AbstractOrderHandler = ModianDailyAndLotteryHandler()


async def get_active_orders(pro_ids: list,
                            session: ClientSession = None) -> str:
    '''
    返回正在进行的集资详情信息
    '''
    orders = await modian.get_detail(pro_ids, session)
    return '\n'.join([programme_detail_resolver(order)
                      for order in orders['data']])


async def get_ranks(pro_id: str, type: int = 1, limit: int = 5,
                    session: ClientSession = None) -> str:
    '''
    返回集资榜单信息
    :param limit: 需要显示的排名 0为不限制
    :returns: 返回前limit名的排名 长度不足则全部返回
    '''
    resp = await modian.get_rankings(pro_id, type=type, session=session)

    ranking: List[Dict[str, Any]] = resp['data']
    if limit != 0 and len(ranking) > limit:
        ranking = ranking[:limit]

    msg = templates.ranking_template(ranking, type)
    return msg


async def get_new_orders(pro_id: str,
                         last_time_dict: Dict[str, str],
                         session: ClientSession = None) -> str:
    '''
    获取并过滤新订单
    '''
    detail_task: asyncio.Task = asyncio.create_task(
        modian.get_detail_one(pro_id, session=session))

    orders_task: asyncio.Task = asyncio.create_task(
        modian.get_sorted_orders(pro_id, session=session))

    ranking_task: asyncio.Task = asyncio.create_task(
        get_ranks(pro_id, session=session))

    await asyncio.gather(detail_task, orders_task, ranking_task)

    detail = detail_task.result()
    orders = orders_task.result()
    ranking = ranking_task.result()

    if(detail['status'] == 2):
        print('集资详情信息获取错误')
    if(orders['status'] == 2):
        print('集资订单信息获取错误')

    # 获取上一次的最新时间
    last_time: str = last_time_dict[pro_id]
    # 更新订单最新时间
    last_time_dict[pro_id] = orders['data'][0]['pay_success_time']

    new_orders: List[Dict[str, Any]] = []
    if len(orders['data']) > 0:
        order_filter(orders['data'], new_orders, last_time)
    # 全为新订单, 则多查询一页
    if last_time != '' and len(orders['data']) == len(new_orders):
        orders = await modian.get_sorted_orders(pro_id, page=2,
                                                session=session)
        order_filter(orders['data'], new_orders, last_time)

    await insert_new_orders(pro_id, new_orders)

    # 处理集资订单并返回播报信息
    msgs = await resolve_order_messages(handler, new_orders,
                                        detail['data'][0], ranking)
    return msgs


def programme_detail_resolver(detail: Dict[str, Any]) -> str:
    '''
    将集资项目进度详情解析成字符串
    '''
    msg = templates.programme_detail_template(detail)
    return msg


def order_filter(orders: List[Dict[str, Any]],
                 new_orders: List[Dict[str, Any]],
                 last_time: str = '') -> List[Dict[str, Any]]:
    '''
    根据参数中的最新时间过滤订单
    使用字符串比较
    '''
    for order in orders:
        if last_time == '' or order['pay_success_time'] > last_time:
            new_orders.append(order)


async def resolve_order_messages(handler: AbstractOrderHandler,
                                 orders: List[Dict[str, Any]],
                                 detail: Dict[str, Any],
                                 ranking: str = '') -> List[str]:
    return await handler.handle(orders, detail, ranking)
