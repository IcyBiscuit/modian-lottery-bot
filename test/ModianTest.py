import asyncio
import aiohttp
from setup import setup
setup()

import modian.utils.ModianUtil as modian

loop = asyncio.get_event_loop()


def getDetailTest():
    task = loop.run_until_complete(modian.getDetail(['57958', '60611']))
    print(task)


def getDetailOneTest():
    task = loop.run_until_complete(modian.getDetailOne('60611'))
    print(task)


def getRankingTest():
    task = loop.run_until_complete(modian.getRankings('57958', 1))
    print(task)


def orderTest():
    task = loop.run_until_complete(modian.getSortedOrders('57958'))
    print(task)


# getDetailOneTest()
# getRankingTest()
# orderTest()
