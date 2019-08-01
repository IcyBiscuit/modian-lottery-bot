from typing import Dict


def lottery_result_template(card: tuple, cards_result: str, score: int) -> str:
    """
    抽卡结果模板
    :param card: 抽选中以显示信息的卡牌
    :param cards_result: 整个抽卡结果信息
    :param score: 获得的积分
    """
    """
    数据示例
    card: (id, level, name, pic_dir)
    """
    msg = "----------------\n"\
        + "恭喜获得新卡!\n"\
        + f"[CQ:image,file={card[3]}]\n"\
        + f"本次积分: {score} 获得卡牌:\n"\
        + f"{cards_result}\n"\
        + "----------------\n"
    return msg


def card_template(card_dict: Dict[str, int]) -> str:
    """
    卡牌(抽中)信息模板
    """
    """
    数据示例
    card_dict:
    {
        "name1": count,
        "name2": count
    }
    """
    msg = '\n'.join(
        [f"{name} × {count}"
         for name, count in card_dict.items()])
    return msg
