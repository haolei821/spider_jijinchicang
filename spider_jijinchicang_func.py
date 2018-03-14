# coding: utf-8

import requests
from lxml import etree
import pandas as pd


url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code=340007&topline=10&year=2017&month=&rt=0.7842498698601414'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'ASP.NET_SessionId=mi3zqipweqet3lesdaa1cff4; st_pvi=18984940597277; st_si=15225452272297; _adsame_fullscreen_12706=1; EMFUND0=null; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND9=03-13 23:45:14@#$%u5174%u5168%u793E%u4F1A%u8D23%u4EFB%u6DF7%u5408@%23%24340007',
    'Host':'fund.eastmoney.com',
    'If-Modified-Since':'Tue, 13 Mar 2018 15:40:00 GMT',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
# 请求网站，得到四个季度的全部数据
def get_resources(url,headers):
    response = requests.get(url,headers=headers).text
    html = etree.HTML(response)
    boxs = html.xpath('/html/body/div[@class="box"]')
    return boxs


# 2017年n季度股票投资明细
def tzmx(n):
    n = 4 - n
    boxs = get_resources(url,headers)
    gpda = boxs[n].xpath('div/table/tbody/tr/td[2]/a/text()')                  # 股票代码
    gpmc = boxs[n].xpath('div/table/tbody/tr/td[3]/a/text()')                  # 股票名称
    data = boxs[n].xpath('div/table/tbody/tr/td[@class="tor"]/text()')         # 占净值比例、持股数（万股）、持仓市值（万元）
    zjzbl = [data[i] for i in range(0,30,3)]                                   # 占净值比例
    cgs = [data[i] for i in range(1,30,3)]                                     # 持股数（万股）
    ccsz = [data[i] for i in range(2,30,3)]                                    # 持仓市值（万元）
    result = [gpda,gpmc,zjzbl,cgs,ccsz]
    df = pd.DataFrame(result,index=['股票代码','股票名称','占净值比例','持股数（万股）','持仓市值（万元）'])
    return df.T


# 2017年4季度股票投资明细
tzmx(4)


# 2017年3季度股票投资明细
tzmx(3)


# 2017年2季度股票投资明细
tzmx(2)


# 2017年1季度股票投资明细
tzmx(1)

