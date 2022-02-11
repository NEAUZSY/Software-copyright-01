"""
基于正则re模块解析数据
"""
import re
import os
from lxml import etree
import requests

from utils.header import get_ua, get_headers

URL = 'http://q.10jqka.com.cn/'


def get(url):
    # 获取请求头
    header = get_headers()
    # 判断本地是否已经存在之前爬取的网页
    if os.path.exists('store.html'):
        # 如果已经存在之前爬取的网页便将其赋值给html
        with open('store.html') as f:
            html = f.read()
    else:
        # 否则在网络上进行爬取，并存储在html变量中
        resp = requests.get(url, headers=header)
        assert resp.status_code == 200
        html = resp.text
        with open('store.html', 'w') as f:
            f.write(html)
    # 返回网页文件
    return html


def parse(html):
    # 创建根节点
    root = etree.HTML(html)
    # 找到今日个股行情信息
    tbody = root.xpath('//table/tbody/tr')
    for tr in tbody:
        ID = tr.xpath('./td[1]/text()')[0]
        print(ID)


    compile_ = re.compile(r'<img data-src="(.*)" alt="(.*)" class')


def main():
    html = get(URL)
    parse(html)


if __name__ == '__main__':
    main()
