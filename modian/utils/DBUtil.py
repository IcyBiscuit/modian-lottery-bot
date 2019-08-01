from typing import Any, Dict, List

from db.Pooling import pool


async def insert_new_orders(pro_id: str, orders: List[Dict[str, Any]]):
    """
    向数据库写入新订单信息
    """
    sql = """
    insert ignore into daily
        (user_id, pro_id, money, pay_date_time)
    values
        (%s,%s,%s,%s)
    """
    data = [(order['user_id'],
             pro_id,
             order['backer_money'],
             order['pay_success_time'])
            for order in orders]
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.executemany(sql, data)
        await conn.commit()


async def get_latest_time() -> List[tuple]:
    """
    取出已保存的最新订单时间
    根据pro_id分组
    """
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
