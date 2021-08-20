# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tushare as ts

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def fetch_stock_basic_info():
    ts.set_token('1fef74d4a1bc37072b480af3f8b51514abfc38855ac4c5848c4e99d3')
    pro = ts.pro_api()
    data = pro.query('stock_basic',  list_status='L',market = '科创板',  fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_date')
    print(data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    fetch_stock_basic_info()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
