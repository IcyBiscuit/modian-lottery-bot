from setup import setup
setup()
from lottery.CardPool import init_card_pool
from lottery.cache.CardCache import cardCache


print(init_card_pool())
print(cardCache)
