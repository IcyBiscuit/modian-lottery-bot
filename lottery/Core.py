import random
from decimal import ROUND_HALF_UP, Decimal
from random import normalvariate
from typing import List

from lottery.CardPool import cardPool
from lottery.configs.config import config
from lottery.enum.CardType import CardType

# 单次抽卡的金额基数
base: Decimal = Decimal(config['baseMoney']).quantize(
    Decimal('.01'), rounding=ROUND_HALF_UP)


def lottery(money: Decimal) -> List[tuple]:
    '''
    根据金额抽卡
    返回抽卡结果列表
    :param money: 集资金额
    :returns: 抽取卡牌的结果列表
    '''
    times = int(money//base)
    cards: List[tuple] = []

    # 十连抽先保底一张SR
    if(times >= 10):
        cards.append(pickCard(CardType.SR))
        times -= 1

    # 抽取剩余的卡牌
    cards += [pickCard(pickCardLevel(money)) for i in range(times)]
    # for i in range(times):
    #     level = pickCardLevel(money)
    #     card = pickCard(level)
    #     cards.append(card)
    return cards


def pickCard(level: CardType) -> tuple:
    '''
    从对应级别卡池中随机抽取一张卡牌
    返回对应卡牌信息
    :param level: 卡牌等级
    :returns: 对应等级的卡牌
    '''
    cardList: List[tuple] = cardPool[level.value]
    random.shuffle(cardList)
    return random.choice(cardList)


def pickCardLevel(money: Decimal) -> CardType:
    '''
    选取卡牌级别
    TODO 可根据集资金额动态调整概率
    :param money: 集资金额
    :returns: 抽取卡牌的等级
    '''
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
