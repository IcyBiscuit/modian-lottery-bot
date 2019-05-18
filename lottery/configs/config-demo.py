config = {
    # 卡牌存放的根目录(本地)
    "cardPoolFilePrefix": "/path/to/your/cardpoolfolder",
    # 卡牌文件在coolq所在的服务器存放的路径根目录(远端服务器, 如运行在同一个服务器, 则无需配置)
    "remoteFilePrefix": "cardpool",
    # 单次抽取卡牌的基数金额(为保证准确, 请使用字符串类型)
    "baseMoney": "13.14",
    # 卡牌的版本号
    "version": 2,
    # 重复抽卡后的累计积分
    # 计算代码在 lottery/Lottery.py#line26
    "score": {
        "N": 5,
        "R": 10,
        "SR": 20,
        "SSR": 50,
        "UR": 200
    }
}
