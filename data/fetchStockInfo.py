import tushare as ts


def fetch_stock_basic_info():
    ts.set_token('1fef74d4a1bc37072b480af3f8b51514abfc38855ac4c5848c4e99d3')
    pro = ts.pro_api()
    data = pro.query('stock_basic',  list_status='L',market = '科创板',  fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_date')
    # print(data)
    # 转换顺序
    data = data.loc[:,
           ['exchange', 'symbol', 'ts_code', 'market', 'name', 'fullname', 'enname', 'cnspell', 'curr_type', 'area',
            'industry', 'list_date']]

    # 插入数据
    sql = "INSERT INTO stockprediction.stock_basic_info(exchid, stock_code, ts_stock_code, stock_type, stock_name, stock_full_name, stcok_en_name, stock_spell_name, curr_type, area, industry, list_date) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        for i in range(0, len(data)):
            str = '\"' # 用" 因为英文那么有'
            for j in range(0, data.shape[1]-1):
                str = str + data.iloc[i][data.columns[j]]+'\",\"'
            str = str + data.iloc[i][data.shape[1]-1] + '\"'
            # 因为用%时，必须时一个元组，所以这里要把str转换成元组
            # values = (str,) # 这个不行，结果是只有str的元组
            val = eval(str) # 使用这个可以换成元组
            # print(val)
            cursor.execute(sql, val)
        mydb.commit()
        print('成功插入', cursor.rowcount, '条数据')
    except Exception as e:
        print(e)
        mydb.rollback()