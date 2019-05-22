import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ModuleNotFoundError:
    pass

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import modian.Schedule as modianSchedule
from modian.configs.ModianConfig import config


if __name__ == "__main__":

    sche = AsyncIOScheduler()
    if "dailyInterval"in config and config['dailyInterval'] != 0:
        dailyInterval = config['dailyInterval']
    else:
        dailyInterval = 25
    if "pkInterval" in config and config['pkInterval'] != 0:
        pkInterval = config['pkInterval']
    else:
        pkInterval = 30

    if "daily" in config:
        sche.add_job(modianSchedule.dailySchedule, 'interval',
                     seconds=dailyInterval, max_instances=3)

    if "pk" in config:
        sche.add_job(modianSchedule.pkSchedule, 'interval',
                     seconds=pkInterval, max_instances=3)
    sche.start()
    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        loop.stop()
