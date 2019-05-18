import json

from aiohttp import ClientSession

from modian.utils.SignUtil import getSign

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}


async def getDetail(pro_ids: list, session: ClientSession = None) -> dict:
    '''
    项目筹款结果查询
    传入订单pro_id数组
    拼接成字符串 pro_id1, pro_id2, ... 作为请求参数
    '''
    pro_ids_str = ','.join(pro_ids)
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_ids_str
    }
    sign = getSign(form)
    form['sign'] = sign

    body = await makeRequest(url, form, header, session=session)
    return json.loads(body)


async def getDetailOne(pro_id: str, session: ClientSession = None) -> dict:
    '''
    获取一条订单pri_id(字符串格式)
    '''
    return await getDetail([pro_id], session=session)


async def getRankings(pro_id: str, type: int = 1, page: int = 1,
                      session: ClientSession = None) -> dict:
    '''
    项目榜单查询
    type = 1 聚聚榜
    type = 2 打卡榜
    '''
    url = 'https://wds.modian.com/api/project/rankings'
    form = {
        'page': page,
        'pro_id': pro_id,
        'type': type
    }
    sign = getSign(form)
    form['sign'] = sign
    body = await makeRequest(url, form, header, session=session)
    # print(body)
    return json.loads(body)


async def getSortedOrders(pro_id, page=1, sort_by=1,
                          session: ClientSession = None) -> dict:
    '''
    获取订单列表
    sort_by = 1 按支付时间倒序
    sort_by = 0 按下单时间倒序
    '''
    url = 'https://wds.modian.com/api/project/sorted_orders'
    form = {
        'page': page,
        'pro_id': pro_id,
        'sort_by': sort_by
    }
    sign = getSign(form)
    form['sign'] = sign

    body = await makeRequest(url, form, header, session=session)
    return json.loads(body)


async def makeRequest(url: str, data: dict, headers: dict,
                      session: ClientSession = None) -> str:
    '''
    发送请求封装
    可提供复用的ClientSession连接池
    若无连接池, 则创建
    :returns: 以字符串形式返回请求的body部分
    '''
    if session is None:
        print('using new session')
        async with ClientSession() as clientSession:
            resp = await clientSession.post(
                url=url, data=data, headers=headers)
    else:
        resp = await session.post(
            url=url, data=data, headers=headers)
    body = await resp.text()
    return body
