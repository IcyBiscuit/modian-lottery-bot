import json
from typing import Any, Dict

from aiohttp import ClientResponse, ClientSession

from modian.utils.SignUtil import get_sign

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}


async def get_detail(pro_ids: list,
                     session: ClientSession = None) -> Dict[str, Any]:
    """
    项目筹款结果查询
    :param pro_ids: 需要查询的订单列表
    :param session: 可供复用的ClientSession实例
    :returns: 订单详情
    """
    """
    传入订单pro_id数组 拼接成字符串 pro_id1, pro_id2, ... 作为请求参数
    """
    pro_ids_str = ','.join(pro_ids)
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_ids_str
    }
    sign = get_sign(form)
    form['sign'] = sign

    body = await make_request_and_get_body(url, form, header, session=session)
    return json.loads(body)


async def get_detail_one(pro_id: str,
                         session: ClientSession = None) -> Dict[str, Any]:
    """
    获取一条订单pri_id (字符串格式)
    """
    return await get_detail([pro_id], session=session)


async def get_rankings(pro_id: str, type: int = 1, page: int = 1,
                       session: ClientSession = None) -> Dict[str, Any]:
    """
    项目榜单查询
    type = 1 聚聚榜
    type = 2 打卡榜
    默认为集资榜单
    :param pro_id: 订单id
    :param type: 查询榜单的类型
    :param page: 查询的页码
    :param session: 可供复用的ClientSession实例
    :returns: 榜单信息
    """
    url = 'https://wds.modian.com/api/project/rankings'
    form = {
        'page': page,
        'pro_id': pro_id,
        'type': type
    }
    sign = get_sign(form)
    form['sign'] = sign
    body = await make_request_and_get_body(url, form, header, session=session)
    # print(body)
    return json.loads(body)


async def get_sorted_orders(pro_id, page=1, sort_by=1,
                            session: ClientSession = None) -> Dict[str, Any]:
    """
    获取订单列表
    :param pro_id: 订单id
    :param sort_by: 排序类型 1 按支付时间倒序 0 按下单时间倒序
    :param page: 查询的页码
    :param session: 可供复用的ClientSession实例
    :returns: 订单信息
    """
    url = 'https://wds.modian.com/api/project/sorted_orders'
    form = {
        'page': page,
        'pro_id': pro_id,
        'sort_by': sort_by
    }
    sign = get_sign(form)
    form['sign'] = sign

    body = await make_request_and_get_body(url, form, header, session=session)
    return json.loads(body)


async def make_request_and_get_body(url: str, data: dict, headers: dict,
                                    session: ClientSession = None) -> str:
    """
    发送请求封装
    可提供复用的ClientSession连接池
    若无连接池, 则创建
    :param url: 请求的url
    :param data: 请求的表单数据
    :param header:
    :param session: 可供复用的ClientSession实例
    :returns: 以字符串形式返回请求的body部分
    """
    resp: ClientResponse = None
    # 没有可复用的ClientSession则创建实例
    if session is None:
        print('using new session')
        async with ClientSession() as clientSession:
            resp = await clientSession.post(
                url=url, data=data, headers=headers)
    else:
        resp = await session.post(
            url=url, data=data, headers=headers)
    async with resp:
        return await resp.text()
