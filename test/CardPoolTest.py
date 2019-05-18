from setup import setup
setup()
from lottery.CardPool import initCardPool
from lottery.cache.CardCache import cardCache


print(initCardPool())
print(cardCache)
