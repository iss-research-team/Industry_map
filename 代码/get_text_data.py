#-*- codeing = utf-8 -*-
#@Author :hcy
#@File ：txt_read
#@Time : 2022/2/24-17:35

import requests
from lxml import html

url='http://www.gov.cn/zhengce/content/2022-02/24/content_5675441.htm'

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}

def gettext(url):
    page = requests.Session().get(url,headers=header)
    tree = html.fromstring(page.text)
    result = tree.xpath('//td[@class="b12c"]/p/text()')
    print(result)
    print(result[1])


if __name__=='__main__':
    gettext(url)