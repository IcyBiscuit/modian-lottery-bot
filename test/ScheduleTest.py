from setup import setup
setup()
import modian.Schedule as Schedule
import asyncio


loop = asyncio.get_event_loop()


def dailySchedule():
    loop.run_until_complete(Schedule.dailySchedule())


def initLatestTime():
    r = loop.run_until_complete(Schedule.initLatestTime())

    print(r)


def vsSchedule():
    loop.run_until_complete(Schedule.pkSchedule())


dailySchedule()
# initLatestTime()
# vsSchedule()