from lottery.CardPool import card_pool
from typing import Dict

cardCache: Dict[str, tuple] = {}

for cards in card_pool.values():
    for card in cards:
        id, level, name, pic_dir = card
        cardCache[str(id)] = card
