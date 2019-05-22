try:
    from setup import setup
    setup()
except Exception:
    pass

import asyncio
import lottery.cache.LotteryResultCache as LotteryResultCache
from lottery.CardPool import cardPool

loop = asyncio.get_event_loop()

t = (268, 'N', 'N9', 'cardpool/N/N9.png')


def initUserRecord():

    f = LotteryResultCache.initUserRecord('6037792')
    r = loop.run_until_complete(f)
    print(r)
    print(LotteryResultCache.lotteryCache)
    print(cardPool)


initUserRecord()
