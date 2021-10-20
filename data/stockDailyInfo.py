import tushare as ts
import pandas as pd
import pymysql

ts.set_token('1fef74d4a1bc37072b480af3f8b51514abfc38855ac4c5848c4e99d3')
pro = ts.pro_api()


def insertIntoDB(stock_his_data):
    # 获取游标
    mydb = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='stockprediction', charset='utf8')
    cursor = mydb.cursor()

    # 插入数据
    for i in range(0, len(stock_his_data)):
        sql = " INSERT INTO stockprediction.stock_daily_info(trd_date,  ts_stock_code, open, high, low, close, vol, amount, price_change, p_change, turn_over, volume_ratio, ma5, v_ma5, ma10, v_ma10, ma20, v_ma20, ma30, v_ma30, ma60, v_ma60)\
                VALUES ('{}','{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})" \
            .format(stock_his_data.loc[i][0], stock_his_data.loc[i][1], stock_his_data.loc[i][2],stock_his_data.loc[i][3], stock_his_data.loc[i][4], stock_his_data.loc[i][5],\
                    stock_his_data.loc[i][6], stock_his_data.loc[i][7], stock_his_data.loc[i][8],stock_his_data.loc[i][9], stock_his_data.loc[i][10],\
                    stock_his_data.loc[i][11], stock_his_data.loc[i][12], stock_his_data.loc[i][13],stock_his_data.loc[i][14], stock_his_data.loc[i][15], stock_his_data.loc[i][16],\
                    stock_his_data.loc[i][17], stock_his_data.loc[i][18], stock_his_data.loc[i][19],stock_his_data.loc[i][20], stock_his_data.loc[i][21])

        #         print(sql)
        cursor.execute(sql)
    mydb.commit()


# 获取科创版股票代码
stock_codes = pro.query('stock_basic', exchange='SSE', market='科创板', list_status='L', fields='ts_code')
# stock_codes.ts_code

for stock in stock_codes.ts_code:
    # 获取每只股票的行情信息
    df = ts.pro_bar(ts_code=stock, ma=[5, 10, 20, 30, 60], factors=['tor', 'vr'], adj='qfq')
    # 取固定列，切换成和sql一样的位置
    stock_data = df.loc[:,
                 ['trade_date', 'ts_code', 'open', 'high', 'low', 'close', 'vol', 'amount', 'change', 'pct_chg',
                  'turnover_rate', 'volume_ratio', 'ma5', 'ma_v_5', 'ma10', 'ma_v_10', 'ma20', 'ma_v_20', 'ma30',
                  'ma_v_30', 'ma60', 'ma_v_60']]
    # 均线为null,填充为0
    stock_data.fillna(value=0, inplace=True)
    # 插入数据库
    insertIntoDB(stock_data)


## tips
    # 构建sql时，有3种方法：
    # 1、拼接sql，但是要求插入的数据类型一致,参考stockBasicIn.py
    # 2、使用format，用{}占位，但是如果这个值中有‘.’,例如'688001.sh',pymysql不识别，需要将整个作为一个字符串，就需要在{}加单引号‘’，如下
    #  sql = " INSERT INTO stockprediction.stock_daily_info(trd_date,  ts_stock_code, open) VALUES ({},  '{}', {})".format(aa,bb,cc)
    # 3、%d，%s,代表数字和字符串的占位符,但是如果这个值中有‘.’,例如'688001.sh',pymysql不识别，需要将整个作为一个字符串，就需要变成'%s'，如下
    #   sql = " INSERT INTO stockprediction.stock_daily_info(trd_date,  ts_stock_code, open) VALUES (%s,  '%s', %d)"%(aa,bb,cc)
    # 4、以上还是解决不了，就用sql = '''insert into aaa() values (%s,'%s',"%s")''',有单引号的就用”“括起来就可以！推荐！