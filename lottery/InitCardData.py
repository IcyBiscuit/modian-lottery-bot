import asyncio
import os
import sys
import pathlib

try:
    BASE_PATH = pathlib.Path(__file__).parent.parent
    sys.path.append(BASE_PATH.absolute().as_posix())
except Exception:
    print('目录初始化失败')
    exit()


from configs.LotteryConfig import config
from lottery.utils.DBUtil import initCardTable
'''
从磁盘中读取卡牌信息
并将对应信息写入数据库中
'''
version = config['version']

prefix = config['cardPoolFilePrefix']

loop = asyncio.get_event_loop()

cards = []
for root, dirs, files in os.walk(prefix):
    for dir in dirs:
        absPath = os.path.join(root, dir)
        for card in os.listdir(absPath):
            # (level, name, pic_dir, version)
            if "remoteFilePrefix" in config\
                    and config['remoteFilePrefix'] != '':
                pic_dir = os.path.join(
                    f"{config['remoteFilePrefix']}/{dir}", card)
            else:
                pic_dir = os.path.join(absPath, card)
            row = (dir, card[:-4], pic_dir, version)
            print(row)
            cards.append(row)


loop.run_until_complete(initCardTable(cards))
