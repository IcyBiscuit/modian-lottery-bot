import asyncio
from typing import Dict, List

from configs.LotteryConfig import config
from lottery.utils.DBUtil import get_cards_by_version

loop = asyncio.get_event_loop()


def init_card_pool() -> Dict[str, List[tuple]]:
    """
    初始化卡池
    从数据库中读取设定卡牌版本号的卡牌
    按照卡牌等级构造卡池缓存
    :returns: 对应版本号的卡池缓存字典
    """
    card_pool: Dict[str, List[tuple]] = {}
    cards: List[tuple] = loop.run_until_complete(
        get_cards_by_version(config['version']))
    for card in cards:
        id, level, name, pic_dir = card
        if level not in card_pool:
            card_pool[level] = []
        card_pool[level].append(card)
    return card_pool


card_pool = init_card_pool()
