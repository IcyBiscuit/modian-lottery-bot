from typing import Dict, List, Set

from lottery.utils.DBUtil import get_cards_by_user_id

lotteryCache: Dict[str, Set[tuple]] = {}


async def init_user_record(user_id: str) -> Set[tuple]:
    """
    根据用户id, 从数据库中读取已拥有的卡牌数据
    将获得的结果初始化对应用户抽卡的结果缓存
    :param userID: 用户的摩点id
    """
    # 数据库读取已经拥有的卡牌数据
    cards: Set[tuple] = await get_cards_by_user_id(user_id)

    # 双重判断
    # 避免在缓存初始化时期
    # 同一个用户多个订单进行处理时
    # 协程在等待期间其他协程已经初始化缓存
    # 导致缓存重复初始化, 造成数据不一致
    if user_id not in lotteryCache:
        lotteryCache[user_id] = cards
    else:
        cards = lotteryCache[user_id]
    return cards


def update_cache(user_id: str, cards: List[tuple]):
    """
    根据抽卡结果与用户id更新缓存的已拥有的卡牌信息
    :param user_id: 用户的摩点id
    :param cards: 抽卡结果列表
    """
    lotteryCache[user_id].update(cards)
