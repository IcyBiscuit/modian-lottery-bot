from typing import Any, Dict, List

import templates.modian.ModianTemplate as templates
from lottery.Lottery import lottery
from modian.handlers.AbstractOrderHandler import AbstractOrderHandler


class ModianDailyAndLotteryHandler(AbstractOrderHandler):
    '''
    集资以及抽卡处理类
    '''
    async def handle(self, orders: List[Dict[str, Any]],
                     detail: Dict[str, Any], ranking: str = '') -> List[str]:
        '''
        处理集资信息以及进行抽卡流程
        '''
        lottery_msgs: List[str] = await lottery(orders)
        msgs: List[str] = []
        for i in range(len(orders)):
            order = orders[i]
            cards = lottery_msgs[i]
            msg = templates.order_template(order)\
                + templates.programme_detail_template(detail)\
                + cards\
                + ranking
            msgs.append(msg)
        return msgs
