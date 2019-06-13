from typing import List, Set

import lottery.cache.LotteryResultCache as LotteryResultCache
from configs.LotteryConfig import config
from lottery.cache.LotteryResultCache import lotteryCache
from lottery.utils.DBUtil import update_score


async def calculate_score(user_id: str, cards: List[tuple]) -> int:
    '''
    计算积分
    若用户已拥有卡牌
    则计数值增加并累计积分
    更新数据库值
    :param user_id: 用户摩点id
    :param cards: 卡牌列表
    '''
    user_cards_set: Set[tuple] = await get_user_cards(user_id)
    score = 0
    for card in cards:
        if card not in user_cards_set:
            user_cards_set.add(card)
        else:
            score += config['score'][card[1]]

    # 更新数据库积分
    await update_score(user_id, score)
    return score


async def get_user_cards(user_id: str) -> Set[tuple]:
    '''
    获取用户拥有的卡牌
    若缓存中未有用户数据
    则从数据库中获取数据
    并放入缓存中
    :param user_id: 用户摩点id
    :returns: 用户已拥有卡牌的哈希集
    '''
    if user_id not in lotteryCache:
        usercards = await LotteryResultCache.init_user_record(user_id)
    else:
        usercards = lotteryCache[user_id]
    return usercards
