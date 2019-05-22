from typing import Any, Dict, List, Set

from aiomysql import Cursor

from configs.LotteryConfig import config
from db.Pooling import pool


async def initCardTable(cards: List[tuple]):
    '''
    向数据库写入卡牌信息
    用于新卡牌数据读入
    '''
    sql = """
    insert into cards
        (level, name, pic_dir, version)
    values
        (%s, %s, %s, %s)
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.executemany(sql, cards)
        await conn.commit()


async def getCardsByVersion(version: int) -> List[tuple]:
    '''
    根据卡牌版本
    获取相应的卡牌
    :param version: 需要读取的卡牌版本号
    :returns: 对应版本号的卡牌列表结果集
    '''
    sql = """
    select
        id, level, name, pic_dir
    from
        cards
    where
        version = %s
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, version)
            return await cursor.fetchall()


async def markOrderOne(orderInfo: Dict[str, Any], cursor: Cursor):
    '''
    将一条订单信息标记为已经抽卡
    :param orderInfo: 订单信息
    '''
    sql = """
    update daily
    set
        lottery = 1
    where
        pay_date_time = %s and user_id = %s
    """
    data = (orderInfo['pay_success_time'], orderInfo['user_id'])
    await cursor.execute(sql, data)


async def markOrderMany(orderInfoList: List[Dict[str, Any]], cursor: Cursor):
    '''
    将多条订单标记为已抽卡
    '''
    sql = """
    insert into daily
        (pay_date_time,user_id)
    values
        (%s, %s)
    on duplicate key update
        lottery = 1;
    """
    datas = [(orderInfo['pay_success_time'], orderInfo['user_id'])
             for orderInfo in orderInfoList]
    await cursor.executemany(sql, datas)


async def insertLotteryData(orderInfo: Dict[str, Any], cards: List[tuple]):
    '''
    将抽卡结果写入数据库
    :param orderInfo: 订单信息
    :param cards: 卡牌列表
    '''
    sql = """
    insert ignore into lottery_record
        (user_id, card_id, pay_date_time, insert_time, card_version)
    values
        (%s, %s, %s, now(), %s)
    """
    '''
    订单信息
    {
        "user_id": ,
        "nickname": "",
        "order_time": "2019-05-11 10:44:13",
        "pay_success_time": "2019-05-11 10:44:20",
        "backer_money":
    }
    '''
    rows: List[tuple] = lotteryDataRowsBuilder(orderInfo, cards)
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                # 写入卡牌数据
                await cursor.executemany(sql, rows)
                # 标记订单状态为已经抽取卡牌
                await markOrderOne(orderInfo, cursor)
                await conn.commit()
            except Exception as e:
                print(e.with_traceback())
                await conn.rollback()


async def getOrders() -> List[tuple]:
    '''
    获取未抽卡的订单
    '''
    sql = """
    SELECT
        user_id, pay_date_time, money, pro_id
    FROM
        daily
    WHERE
        lottery = 0 AND money >= '13.14'
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql)
            return await cursor.fetchall()


async def getCardsByUserId(userId: str) -> Set[tuple]:
    '''
    根据摩点用户id获取用户已拥有的卡牌情况
    返回已拥有卡牌的哈希集
    :param userId: 用户的摩点id
    :returns: 用户已经拥有的卡牌集合 (已去重)
    '''
    sql = """
    SELECT
        c.id, c.level, c.name, c.pic_dir
    FROM
        lottery_record l
            INNER JOIN
        cards c ON l.card_id = c.id
    WHERE
        l.user_id = %s
    GROUP BY c.id
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, userId)
            cards = await cursor.fetchall()
            return set(cards)


async def updateScore(userId: str, score: int):
    '''
    更新用户积分信息
    无用户记录则创建
    有则更新积分
    :param userId: 摩点用户id
    :param score: 本次获得的积分
    '''
    sql = """
    insert into user
        (modian_id, score)
    values
        (%s, %s)
    on duplicate key update
        score = score + %s
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute(sql, (userId, score, score))
                await conn.commit()
            except Exception as e:
                print(e.with_traceback())
                await conn.rollback()


async def bindModianUserAndQQ(userId: str, qqNum: str):
    '''
    绑定摩点id与QQ号
    '''
    sql = """
    UPDATE user
    SET
        qq = %s
    WHERE
        modian_id = %s
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute(sql, (qqNum, userId))
                await conn.commit()
            except Exception as e:
                print(e.with_traceback())
                conn.rollback()


async def checkCardsByQQNum(qqNum: str) -> List[tuple]:
    '''
    根据qq号码查询卡牌收集情况
    :returns: 卡列表 (id, level, name)
    '''
    sql = """
    SELECT
        c.id, c.level, c.name
    FROM
        lottery_record l
            INNER JOIN
        cards c ON l.card_id = c.id
    WHERE
        l.user_id = (SELECT
                modian_id
            FROM
                user
            WHERE
                qq = %s)
            AND version = %s
    GROUP BY c.id , c.level
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, (qqNum, config['version']))
            return await cursor.fetchall()


def lotteryDataRowsBuilder(
        orderInfo: Dict[str, Any],
        cards: List[tuple]) -> List[tuple]:
    '''
    利用订单信息与卡牌信息
    构建插入数据库的数据行
    '''
    '''
    订单信息
    {
        "user_id": ,
        "nickname": "",
        "order_time": "2019-05-11 10:44:13",
        "pay_success_time": "2019-05-11 10:44:20",
        "backer_money":
    }
    卡牌元组信息 (id,level,name,pic_dir)
    数据行信息 (user_id, card_id, pay_date_time, insert_time, card_version)
    '''
    # rows: List[tuple] = []
    # for card in cards:
    #     cardId = card[0]
    #     row = (orderInfo['user_id'], cardId,
    #            orderInfo['pay_success_time'], config['version'])
    #     rows.append(row)
    rows = [(orderInfo['user_id'],
             card[0],
             orderInfo['pay_success_time'],
             config['version']) for card in cards]
    return rows
