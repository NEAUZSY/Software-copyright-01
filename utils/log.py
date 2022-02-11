import sys

from datetime import datetime


# 输出调试信息，并及时刷新缓冲区
def log(content):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(dt + ' ' + str(content) + '...')
    sys.stdout.flush()
