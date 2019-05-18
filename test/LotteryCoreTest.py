from setup import setup
setup()

import lottery.Core as Core
from lottery.enum.CardType import CardType


def pickCard():
    res = Core.pickCard(CardType.N)
    print(res)
