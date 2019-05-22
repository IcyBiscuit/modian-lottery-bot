import asyncio
from typing import Dict, List

from configs.LotteryConfig import config
from lottery.utils.DBUtil import getCardsByVersion

loop = asyncio.get_event_loop()
# cardPool: Dict[str, List[tuple]] = {}


def initCardPool() -> Dict[str, List[tuple]]:
    '''
    初始化卡池
    从数据库中读取设定卡牌版本号的卡牌
    按照卡牌等级构造卡池缓存
    :returns: 对应版本号的卡池缓存字典
    '''
    cardPool: Dict[str, List[tuple]] = {}
    cards: List[tuple] = loop.run_until_complete(
        getCardsByVersion(config['version']))
    for card in cards:
        id, level, name, pic_dir = card
        if level not in cardPool:
            cardPool[level] = []
        cardPool[level].append(card)
    return cardPool


cardPool = initCardPool()
