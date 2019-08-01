from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List


class AbstractOrderHandler(metaclass=ABCMeta):
    """
    集资消息处理抽象类

    自定义处理集资播报信息的具体流程请继承该类
    并覆写handle方法
    """
    @abstractmethod
    async def handle(self, pro_id: str, orders: List[Dict[str, Any]],
                     detail: Dict[str, Any], ranking: str = '') -> List[str]:
        """
        此方法为抽象方法, 必须在子类中覆写
        在此方法中可以自行编写对于集资订单的处理逻辑, 并构建集资播报消息

        :param order: 需要进行播报的订单列表
        :param detail: 集资项目的详情信息
        :param ranking: 集资的榜单排名信息
        :returns: 处理后的集资文字消息列表
        """
        raise NotImplementedError
