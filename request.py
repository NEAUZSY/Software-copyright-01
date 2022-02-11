import os
from lxml import etree
import time
import requests
from utils.header import get_headers

BASE_URL = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/'


def get(base_url):
    # 获取请求头
    header = get_headers()
    # 判断本地是否已经存在之前爬取的网页
    html = ''
    if os.path.exists('stock.html'):
        # 如果已经存在之前爬取的网页便将其赋值给html
        with open('stock.html', encoding='GBK') as f:
            html = f.read()
    else:
        # 否则在网络上进行爬取，并存储在html变量中
        for i in range(1, 21):
            # 获取真正的url
            url = base_url.format(i)

            # 进行请求
            resp = requests.get(url, headers=header)
            # print(resp.status_cod)
            # assert resp.status_code == 200

            # 获取请求内容
            html += resp.text

            # 暂停一会反爬
            print('完成了{}页抓取'.format(i))
            time.sleep(0.1)

        with open('stock.html', 'w', encoding='GBK') as f:
            f.write(html)
    # 返回网页文件
    return html


def parse(html):
    # 创建根节点
    root = etree.HTML(html)
    # 找到今日个股行情信息
    tbody = root.xpath('//table/tbody/tr')
    data = []
    for tr in tbody:
        # 初始化每一行的列表
        row = [str(tr.xpath('./td[1]/text()')[0]),
               str(tr.xpath('./td[2]/a/text()')[0]),
               str(tr.xpath('./td[3]/a/text()')[0])]
        for i in range(4, 15):
            target = r'./td[{}]/text()'.format(i)
            row.append(str(tr.xpath(target)[0]))
        data.append(row)
    # print(data)
    return data


def main():
    html = get(BASE_URL)
    data = parse(html)
    print(data)


if __name__ == '__main__':
    main()
