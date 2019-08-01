from typing import Any, Dict, List

import templates.modian.ModianTemplate as templates
from modian.handlers.AbstractOrderHandler import AbstractOrderHandler
from modian.utils.DBUtil import insert_new_orders


class ModianDailyHaldler(AbstractOrderHandler):
    """
    集资播报处理类
    """
    async def handle(self, pro_id: str, orders: List[Dict[str, Any]],
                     detail: Dict[str, Any], ranking: str = '') -> List[str]:
        """
        处理并构建日常集资播报信息
        并将订单信息写入数据库
        """
        await insert_new_orders(pro_id, orders)

        return [templates.order_template(order) +
                templates.programme_detail_template(detail) +
                ranking for order in orders]
