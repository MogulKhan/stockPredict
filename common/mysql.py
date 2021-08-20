import pymysql

def connectDB():
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='wpf', charset='utf8')
    except ee :
        print('数据库链接失败！', str(ee))
    else:#try没有异常的时候才会执行
        print("数据库连接sucessfully!")
        return conn