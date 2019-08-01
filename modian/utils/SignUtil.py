import hashlib
import urllib


def get_sign(form_data: dict) -> str:
    """
    摩点请求加签
    """
    # 将字典按键升序排列，返回一个元组tuple
    tuple = sorted(form_data.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(
        encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    # md5计算 & 十六进制转化 & 根据规则从第6位开始取16位
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign
