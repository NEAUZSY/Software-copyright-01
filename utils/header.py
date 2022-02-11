import random
from . import user_agents


def get_ua():
    # 随机选择一个用户代理
    return random.choice(user_agents)


def get_headers(cookie=None):
    if cookie is not None:
        headers = {
            'User-Agent': get_ua(),
            'Cookie': cookie
        }
    else:
        headers = {
            'User-Agent': get_ua()
        }
    return headers

