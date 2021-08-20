import tushare as ts


def fetch_stock_basic_info():
    ts.set_token('1fef74d4a1bc37072b480af3f8b51514abfc38855ac4c5848c4e99d3')
    pro = ts.pro_api()

    data = pro.query('stock_basic',  list_status='L',market = '科创板',  fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_date')
    print(data)