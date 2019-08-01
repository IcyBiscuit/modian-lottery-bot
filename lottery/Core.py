import random
from decimal import ROUND_HALF_UP, Decimal
from random import normalvariate
from typing import List

from configs.LotteryConfig import config
from lottery.CardPool import card_pool
from lottery.enum.CardType import CardType

# 单次抽卡的金额基数
base: Decimal = Decimal(config['baseMoney']).quantize(
    Decimal('.01'), rounding=ROUND_HALF_UP)


def lottery(money: Decimal) -> List[tuple]:
    """
    根据金额抽卡
    返回抽卡结果列表
    :param money: 集资金额
    :returns: 抽取卡牌的结果列表
    """
    times = int(money//base)
    cards: List[tuple] = []

    # 十连抽先保底一张SR
    if(times >= 10):
        cards.append(pick_card(CardType.SR))
        times -= 1

    # 抽取剩余的卡牌
    cards += [pick_card(pick_card_level(money)) for i in range(times)]
    return cards


def pick_card(level: CardType) -> tuple:
    """
    从对应级别卡池中随机抽取一张卡牌
    返回对应卡牌信息
    :param level: 卡牌等级
    :returns: 对应等级的卡牌
    """
    card_list: List[tuple] = card_pool[level.value]
    random.shuffle(card_list)
    return random.choice(card_list)


def pick_card_level(money: Decimal) -> CardType:
    """
    选取卡牌级别
    TODO 可根据集资金额动态调整概率
    :param money: 集资金额
    :returns: 抽取卡牌的等级
    """
    seed = abs(normalvariate(0, 1))
    level: CardType = CardType.N

    # 86.64%
    # 抽取一张N R
    if seed <= 1.5:
        # 68.26% N
        if abs(normalvariate(0, 1)) <= 1:
            level = CardType.N
        else:
            # 31.74% R
            level = CardType.R
    # 13.36%
    # 抽取一张高级卡 SR-68.26% SSR-27.18% UR-4.56%
    else:
        seed = abs(normalvariate(0, 1))
        if seed <= 1:
            level = CardType.SR
        elif seed <= 2:
            level = CardType.SSR
        else:
            level = CardType.UR
    return level
