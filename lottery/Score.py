from typing import List, Set

import lottery.cache.LotteryResultCache as LotteryResultCache
from configs.LotteryConfig import config
from lottery.cache.LotteryResultCache import lotteryCache
from lottery.utils.DBUtil import updateScore


async def calculateScore(userId: str, cards: List[tuple]) -> int:
    '''
    计算积分
    若用户已拥有卡牌
    则计数值增加并累计积分
    更新数据库值
    :param userId: 用户摩点id
    :param cards: 卡牌列表
    '''
    userCardsSet: Set[tuple] = await getUserCards(userId)
    count = 0
    score = 0
    for card in cards:
        if card not in userCardsSet:
            userCardsSet.add(card)
        else:
            count += 1
            score += config['score'][card[1]]

    # 更新数据库积分
    await updateScore(userId, score)
    return score


async def getUserCards(userId: str) -> Set[tuple]:
    '''
    获取用户拥有的卡牌
    若缓存中未有用户数据
    则从数据库中获取数据
    并放入缓存中
    :param userId: 用户摩点id
    :returns: 用户已拥有卡牌的哈希集
    '''
    if userId not in lotteryCache:
        usercards = await LotteryResultCache.initUserRecord(userId)
    else:
        usercards = lotteryCache[userId]
    return usercards
