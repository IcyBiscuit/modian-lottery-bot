try:
    from setup import setup
    setup()
except Exception:
    pass

import asyncio
import modian.utils.MessageHandler as MessageHandler


loop = asyncio.get_event_loop()


def getActiveOrders():
    task = loop.run_until_complete(
        MessageHandler.getActiveOrders(['57958', '60611']))
    print(task)


def getRanks():
    task = loop.run_until_complete(MessageHandler.getRanks('57958'))
    print(task)


def getNewOrders():
    task = loop.run_until_complete(
        MessageHandler.getNewOrders('57958', "2019-05-12 18:31:47"))
    print(task)


getActiveOrders()
# getRanks()
# getNewOrders()
