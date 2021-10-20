import pandas as pd
import requests
from lxml import etree
import math
import csv
import crawleByProxyIP as proxy
import time
import tushare as ts

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}


# 获取股票评论的总页数
def sum_stock_pages(stock):

    daima = stock  # 定义爬取的股票

    url = 'http://guba.eastmoney.com/list,' + daima + '.html'
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)

    # 页数是动态的，不可以直接获取，但是pagernums是后面的data说明了全部评论的数量和每页个数，相除就可得出总页数

    # 获取页面数量
    total_nums_contents = tree.xpath('//*[@class="pager"]/span/@data-pager')
    print(total_nums_contents)
    # 变成str
    total_nums_contents_str = total_nums_contents[0]
    # 用 | 分割
    total_nums_contents_list = total_nums_contents_str.split("|")
    # 取总评论数和每页数量，相除得到总页数
    total_pages = math.ceil(int(total_nums_contents_list[1]) / int(total_nums_contents_list[2]))
    print("评论总页数："+str(total_pages))
    return total_pages,total_nums_contents_list[1]

def data_to_csv(filename,res):
    with open(filename, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('阅读', '评论', '标题', '链接', '作者', '最后更新','日期'))
        writer.writerows(res)

def data_to_txt(filename,res):
    with open(filename, 'a', newline='') as txtfile:
        txtfile.write(res + '\n')

def crawl_comments(stock,total_pages):
    data = []
    toal_page = total_pages  # 定义爬取的页面
    daima = stock  # 定义爬取的股票
    if toal_page <= 100:

        for page in range(1, toal_page):
            time.sleep(5)
            url = 'http://guba.eastmoney.com/list,' + daima + '_' + str(page) + '.html'
            res = requests.get(url=url, headers=headers)
            res.encoding ='utf-8'

            # res = proxy.getHtml(url)
            # while(res is None):
            #     res = proxy.getHtml(url)

            print("获取第{}页面，进行分析...".format(page))
            tree = etree.HTML(res.text)
            # print(tree)
            li1 = tree.xpath('//*[@id="articlelistnew"]/div/span[1]/text()')
            # print(li1)
            li1.remove('阅读')
            li2 = tree.xpath('//*[@id="articlelistnew"]/div/span[2]/text()')
            li2.remove('评论')
            #     li3 = tree.xpath('//*[@id="articlelistnew"]/div/span[3]/a/text()')
            li3 = tree.xpath('//*[@id="articlelistnew"]/div/span[3]/a/@title')  # 取标题里内容，会比text（）多一些内容
            li3a = tree.xpath('//*[@id="articlelistnew"]/div/span[3]/a/@href')  # 网址链接
            li4 = tree.xpath('//*[@id="articlelistnew"]/div/span[4]/a/font/text()')
            li5 = tree.xpath('//*[@id="articlelistnew"]/div/span[5]/text()')
            li5.remove('最后更新')

            for i in range(len(li1)):
                detial_url = 'http://guba.eastmoney.com' + li3a[i]
                date = comments_date(detial_url)
                list1 = [li1[i], li2[i], li3[i], detial_url, li4[i], li5[i],date]
                data.append(list1)
            print(print("第{}页面，分析结束！".format(page)))
        filename = daima + '.csv'
        print(filename)
        data_to_csv(filename, data)


def comments_date(detial_url):
    # 获取评论日期
    # print(detial_url)
    detial_page = requests.get(url=detial_url, headers=headers)
    detial_page.encoding = 'utf-8'
    tree = etree.HTML(detial_page.text)
    date_info = tree.xpath('//*[@id="zwconttb"]/div[2]/text()')
    if len(date_info) == 0:
        date = 0
    else:
        date = date_info[0].split(' ')[1]
    # print(date)
    return date



def crawl_proxy(stock,total_pages):
    toal_page = total_pages  # 定义爬取的页面
    daima = stock  # 定义爬取的股票

    for page in range(1, toal_page):
        time.sleep(1)
        url = 'http://guba.eastmoney.com/list,' + daima + '_' + str(page) + '.html'
        #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        #     res = requests.get(url=url,headers=headers)
        #     res.encoding ='utf-8'
        res = proxy.getHtml(url)
        page_text = res.text
        page_file_name = stock + '_' +str(page)+'.txt'
        data_to_txt('page_file_name', page_text)


def fech_stocks():

    ts.set_token('1fef74d4a1bc37072b480af3f8b51514abfc38855ac4c5848c4e99d3')
    pro = ts.pro_api()
    kcb_stocks = pro.query('stock_basic', list_status='L', market='科创板',fields='symbol')
    # print(data)
    return kcb_stocks



if __name__ == '__main__':
    # stock= "688001"
    stocks = fech_stocks()
    for i in range(30, len(stocks)):
        print(stocks.loc[i][0])
        stock = stocks.loc[i][0]
        pages,count = sum_stock_pages(stock)
        # print(pages)
        # print(count)
        crawl_comments(stock, pages)
        # summary = 'NO' + str(i) + stock + ": 总页数：" + str(pages) + " ; 总评论数："+str(count)
        summary = 'No {} {}: 总页数: {} ; 总评论数: {}'.format(i+1, stock, pages, count)
        data_to_txt("stockCommentsSummary.text", summary)
        print(summary +" is over!")


