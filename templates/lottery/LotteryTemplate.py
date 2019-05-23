from typing import Dict


def lotteryResultTemplate(card: tuple, cardsResult: str, score: int) -> str:
    '''
    抽卡结果模板
    :param card: 抽选中以显示信息的卡牌
    :param cardsResult: 整个抽卡结果信息
    :param score: 获得的积分
    '''
    '''
    数据示例
    card: (id, level, name, pic_dir)
    '''
    msg = "----------------\n"\
        + "恭喜获得新卡!\n"\
        + f"[CQ:image,file={card[3]}]\n"\
        + f"本次积分: {score} 获得卡牌:\n"\
        + f"{cardsResult}\n"\
        + "----------------\n"
    return msg


def cardTemplate(cardDict: Dict[str, int]) -> str:
    '''
    卡牌(抽中)信息模板
    '''
    '''
    数据示例
    cardDict:
    {
        "name1": count,
        "name2": count
    }
    '''
    msg = '\n'.join(
        [f"{name} × {count}"
         for name, count in cardDict.items()])
    return msg
