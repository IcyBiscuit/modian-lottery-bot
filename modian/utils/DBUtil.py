from typing import List

from db.Pooling import pool


async def insertNewOrders(pro_id: str, orders: list):
    '''
    向数据库写入新订单信息
    '''
    sql = """
    insert ignore into daily
        (user_id, pro_id, money, pay_date_time)
    values
        (%s,%s,%s,%s)
    """
    # data = []
    # for order in orders:
    #     row: tuple = (order['user_id'], pro_id, order['backer_money'],
    #                   order['pay_success_time'])
    #     data.append(row)
    data = [(order['user_id'],
             pro_id,
             order['backer_money'],
             order['pay_success_time'])
            for order in orders]
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.executemany(sql, data)
        await conn.commit()


async def getLatestTime() -> List[tuple]:
    '''
    取出已保存的最新订单时间
    根据pro_id分组
    '''
    sql = """
    select
        pro_id, max(pay_date_time) latest
    from
        daily
    group by
        pro_id
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql)
            return await cursor.fetchall()
