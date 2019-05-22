try:
    from setup import setup
    setup()
except Exception:
    pass

from lottery.cache.CardCache import cardCache
import lottery.utils.DBUtil as DBUtil
import asyncio
from lottery.CardPool import cardPool

loop = asyncio.get_event_loop()


def initCardPool():
    res = loop.run_until_complete(DBUtil.getCardsByVersion(0))
    print(res)


def lottery():
    # (id,level,name,pic_dir)
    f = DBUtil.insertLotteryData(
        {
            "user_id": 1295449,
            "nickname": "猫鏡",
            "order_time": "2019-05-12 19:21:18",
            "pay_success_time": "2019-05-12 19:21:29",
            "backer_money": 52
        },
        [(13, 'UR', 'UR 01demo', '/Users/icybiscuit/Documents/GitHub/modian-lottery-bot/cardpool/UR/UR 01demo.jpg', '0'),
         (13, 'UR', 'UR 01demo',
          '/Users/icybiscuit/Documents/GitHub/modian-lottery-bot/cardpool/UR/UR 01demo.jpg', '0'),
         (13, 'UR', 'UR 01demo', '/Users/icybiscuit/Documents/GitHub/modian-lottery-bot/cardpool/UR/UR 01demo.jpg', '0')])
    loop.run_until_complete(f)


def getOrders():
    f = DBUtil.getOrders()
    res = loop.run_until_complete(f)
    print(res)


def getCardsByUser():
    f = DBUtil.getCardsByUserId('6037792')
    s: set = loop.run_until_complete(f)
    print(s)
    # print(cardPool)
    print((268, 'N', 'N9', 'cardpool/N/N9.png') in s)
    # print(cardCache['13'] in s)


# initCardPool()
# lottery()
# getOrders()
getCardsByUser()
