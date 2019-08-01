try:
    from setup import setup
    setup()
except ModuleNotFoundError:
    pass

import modian.utils.SignUtil as SignUtil

sign = SignUtil.get_sign({
    'page': 1,
    'pro_id': '422422'
})
print(sign)
