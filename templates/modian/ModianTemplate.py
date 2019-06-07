from typing import Any, Dict, List

url_prefix = "https://m.modian.com/project/"


def rankingTemplate(rankingList: List[Dict[str, Any]],
                    type: int = 1) -> str:
    '''
    集资排名消息模板
    :param rankingList: 排名JSON列表
    :param type
    type = 1 聚聚榜
    type = 2 打卡榜
    :param limit: 排名名额限制
    '''
    '''
    JSON数据示例
    集资榜单:
    {
        "user_id": "000000",
        "nickname": "",
        "rank": 1,
        "backer_money": "4220"
    }
    打卡榜单:
    {
        "user_id": "000000",
        "nickname": "",
        "rank": 1,
        "support_days": 422
    }
    '''
    size = len(rankingList)
    if type == 1:
        msg = f"目前集资榜前{size}的聚聚是:\n" +\
            '\n'.join([f"{rank['nickname']}: {rank['backer_money']}元"
                       for rank in rankingList])
    elif type == 2:
        msg = f"目前打卡榜前{size}的聚聚是:\n" +\
            '\n'.join([f"{rank['nickname']}: {rank['support_days']}天"
                       for rank in rankingList])
    else:
        msg = ''
    return msg


def programmeDetailTemplate(detail: Dict[str, Any]) -> str:
    '''
    集资项目详情模板
    :param detail: 项目详情对象(JSON)
    '''
    '''
    数据示例
    detail:
    {
        "pro_id": "",
        "pro_name": "",
        "goal": "42200",
        "already_raised": 5902.46,
        "backer_count": 422,
        "success_order_count": 422,
        "end_time": "2019-06-01 00: 00: 00",
        "pc_cover": "https: //p.moimg.net/bbs_attachments/2019/04/24/20190424_1556069557_5997.jpg?imageMogr2/auto-orient/strip",
        "mobile_cover": "https://p.moimg.net/bbs_attachments/2019/04/22/20190422_1555900256_5600.jpg?imageMogr2/auto-orient/strip",
        "left_time": "距离结束还剩【X小时Y分钟Z秒】"
    }
    '''
    # 百分比
    percentage = round(detail['already_raised']/float(detail['goal'])*100, 2)

    msg = f"{detail['pro_name']}\n" \
        + f"{url_prefix}{detail['pro_id']}\n" \
        + f"进度: {detail['already_raised']}/{detail['goal']} | " \
        + f"({percentage}%)\n" \
        + f"支持人数: {detail['backer_count']}\n{detail['left_time']}\n"
    return msg


def orderTemplate(order: Dict[str, Any]) -> str:
    '''
    集资订单信息模板
    :param order: 支付订单对象(JSON)
    '''
    '''
    数据示例
    order:
    {
        "user_id": 000000,
        "nickname": "",
        "order_time": "2019-05-12 19:21:18",
        "pay_success_time": "2019-05-12 19:21:29",
        "backer_money": 422
    }
    '''
    msg = f"感谢 {order['nickname']} 支援了{order['backer_money']}元\n"
    return msg


def pkTemplate(order: str, vsInfo: str) -> str:
    msg = f"{order}\n"\
        + "----------------\n"\
        + "对家详情:\n"\
        + vsInfo
    return msg
