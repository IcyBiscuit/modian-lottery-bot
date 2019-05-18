from setup import setup
setup()

import modian.utils.SignUtil as SignUtil

sign = SignUtil.getSign({
    'page': 1,
    'pro_id': '422422'
})
print(sign)