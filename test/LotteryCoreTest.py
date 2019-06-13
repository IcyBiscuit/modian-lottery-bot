from setup import setup
setup()

import lottery.Core as Core
from lottery.enum.CardType import CardType


def pickCard():
    res = Core.pick_card(CardType.N)
    print(res)
