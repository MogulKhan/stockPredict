import requests


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml(page_url):
    # ....
    # retry_count = 5
    proxy = get_proxy().get("proxy")

    while 1:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
            html = requests.get(url=page_url, headers=headers, proxies={"http": "http://{}".format(proxy)})
            html.encoding = 'utf-8'
            # 使用代理访问
            print(proxy + "有效")
            return html
        except Exception:
            # retry_count -= 1
            print(proxy + "无效")
            # 删除代理池中代理
            delete_proxy(proxy)
            # 重新获取IP
            proxy = get_proxy().get("proxy")
    return None