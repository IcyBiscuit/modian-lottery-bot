from setup import setup
setup()
import modian.utils.DBUtil as DBUtil
import asyncio


loop = asyncio.get_event_loop()


def insertNewOrders():
    pro_id = '57958'
    orders = [
        {
            "user_id": 1295449,
            "nickname": "猫鏡",
            "order_time": "2019-05-12 19:21:18",
            "pay_success_time": "2019-05-12 19:21:29",
            "backer_money": 52
        },
        {
            "user_id": 1179171,
            "nickname": "拔拔拔拔",
            "order_time": "2019-05-12 18:31:41",
            "pay_success_time": "2019-05-12 18:31:47",
            "backer_money": 13.14
        },
        {
            "user_id": 989790,
            "nickname": "ljh",
            "order_time": "2019-05-12 17:08:40",
            "pay_success_time": "2019-05-12 17:08:51",
            "backer_money": 13.14
        }
    ]
    loop.run_until_complete(DBUtil.insertNewOrders(pro_id, orders))


# insertNewOrders()


def getLatestTime():
    r = loop.run_until_complete(DBUtil.getLatestTime())
    print(r)


getLatestTime()