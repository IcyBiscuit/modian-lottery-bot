from setup import setup
setup()
import re
import lottery.Core as Core
from decimal import Decimal
import matplotlib.pyplot as pyplot

# result = {}

# for i in range(100000):
#     cards = Core.lottery(Decimal("13.14"))
#     for card in cards:
#         id = str(card[2])
#         level = card[1]
#         if id not in result:
#             result[id] = 1
#         else:
#             result[id] = result[id]+1
#         if level not in result:
#             result[level] = 1
#         else:
#             result[level] += 1

# print(result)

# for i in sort:
#     x.append(i[0])
#     y.append(i[1])
res = {'R15': 1259, 'R': 27453, 'N15': 2705, 'N': 59071, 'R21': 1268, 'N25': 2605, 'N17': 2751, 'R20': 1287, 'SR7': 952, 'SR': 9178, 'N28': 2669, 'N24': 2627, 'N18': 2791, 'R14': 1219, 'SSR3': 744, 'SSR': 3702, 'R22': 1225, 'N1': 2774, 'R25': 1197, 'N22': 2624, 'N19': 2692, 'N21': 2627, 'R10': 1197, 'N29': 2741, 'R23': 1216, 'N11': 2731, 'N12': 2711, 'N13': 2662, 'SR8': 904, 'R27': 1233, 'N16': 2693, 'R1': 1252, 'R26': 1278,
       'N10': 2619, 'R28': 1298, 'SR4': 888, 'R29': 1245, 'SR1': 962, 'R19': 1308, 'R16': 1241, 'N20': 2608, 'SR5': 902, 'R2': 1267, 'N14': 2637, 'R18': 1183, 'R11': 1256, 'R17': 1280, 'SR3': 907, 'UR1': 279, 'UR': 596, 'N2': 2673, 'N23': 2682, 'R24': 1222, 'N27': 2700, 'R12': 1271, 'SR9': 906, 'SR2': 931, 'SR6': 897, 'N26': 2749, 'SSR2': 780, 'SSR5': 694, 'SR10': 929, 'R13': 1251, 'SSR4': 754, 'SSR1': 730, 'UR2': 317}
del res['N']
del res['R']
del res['SR']
del res['SSR']
del res['UR']
sort = sorted(res.items(), key=lambda item: item[0])
x = []
y = []

for i in sort:
    x.append(re.sub("\\d+", "", i[0]))
    y.append(i[1])
# pyplot.plot(x, y)
pyplot.bar(x, y)
pyplot.show()
