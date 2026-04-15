def generate_code(length=6):
    """
    生成指定长度的随机验证码
    :param length: 验证码长度
    :return: 验证码字符串
    """
    import random
    import string
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return code
