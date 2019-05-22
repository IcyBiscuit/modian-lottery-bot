try:
    from setup import setup
    setup()
except Exception:
    pass

import lottery.Score as Score
import asyncio

loop = asyncio.get_event_loop()


def getUserCards():
    f = Score.getUserCards('6037792')
    r = loop.run_until_complete(f)
    print(r)


def calculateScore():
    f = Score.calculateScore(
        '6037792', [(294, 'SSR', 'SSR5', 'cardpool/SSR/SSR5.png'),
                    (8, 'R', 'R4', 'cardpool/R/R4.png'),
                    (8, 'R', 'R4', 'cardpool/R/R4.png')])
    r = loop.run_until_complete(f)
    print(r)


# getUserCards()

calculateScore()
