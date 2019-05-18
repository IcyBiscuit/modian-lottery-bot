from typing import Dict, List, Set

from lottery.utils.DBUtil import getCardsByUserId

lotteryCache: Dict[str, Set[tuple]] = {}


async def initUserRecord(userId: str):
    '''
    根据用户id, 从数据库中读取已拥有的卡牌数据
    将获得的结果初始化对应用户抽卡的结果缓存
    :param userID: 用户的摩点id
    '''
    cards: Set[tuple] = await getCardsByUserId(userId)
    lotteryCache[userId] = cards
    return cards


def updateCache(userId: str, cards: List[tuple]):
    '''
    根据抽卡结果与用户id更新缓存的已拥有的卡牌信息
    :param userId: 用户的摩点id
    :param cards: 抽卡结果列表
    '''
    lotteryCache[userId].update(cards)
