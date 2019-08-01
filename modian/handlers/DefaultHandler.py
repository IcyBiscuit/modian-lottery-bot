from typing import Any, Dict, List

import templates.modian.ModianTemplate as templates
from modian.handlers.AbstractOrderHandler import AbstractOrderHandler


class DefaultHandler(AbstractOrderHandler):
    """
    集资播报处理类
    """
    async def handle(self, pro_id: str, orders: List[Dict[str, Any]],
                     detail: Dict[str, Any], ranking: str = '') -> List[str]:
        """
        处理并构建日常集资播报信息
        信息不写入数据库
        """
        return [templates.order_template(order) +
                templates.programme_detail_template(detail) +
                ranking for order in orders]
