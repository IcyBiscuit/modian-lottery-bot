from lottery.CardPool import cardPool
from typing import Dict

cardCache: Dict[str, tuple] = {}

for cards in cardPool.values():
    for card in cards:
        id, level, name, pic_dir = card
        cardCache[str(id)] = card
