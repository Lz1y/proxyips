"""
由cleviry修改：
1.更换了可用的代理源（有需要可自行拓展）
2.更换了可用的代理有效性验证

"""
# -*- coding:utf-8 -*-
import json
import requests
import signal
import sys
import os


def handler(signal_num, frame):
    Goduplicate()
    print("\nDone,the available ip have been put in 'proxy_ips.txt'...")
    print("\nSucceed to exit.")
    sys.exit(signal_num)


# 获取可用IP
def proxy_spider():
    url = "https://sunny9577.github.io/proxy-scraper/proxies.json"
    response_data = requests.get(url).text
    json_data = json.loads(response_data)
    update_time = json_data['lastUpdated']
    print(update_time)
    proxynova = json_data['proxynova']
    usproxy = json_data['usproxy']
    for i in proxynova:
        print(i)
        proxy_check(i['ip'], i['port'], 'http')
    for i in usproxy:
        print(i)
        proxy_check(i['ip'], i['port'], 'http')


# IP有效性检测并做持久化
def proxy_check(ip, port, protocol):
    proxy = ip + ":" + port
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
    }
    print(proxies)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    try:
        r = requests.get(url="https://api.ipify.org/?format=json", headers=headers, proxies=proxies, timeout=5)  #
        ip_available = r.json().get("ip")
        if ip_available == ip:
            print(str(proxy) + 'is ok')
            with open("proxy_ip.txt", 'a', encoding="utf-8") as ip:
                ip.write(ip_available + ':' + port + '\n')

    except Exception as e:
        # print e
        pass


# ip去重
def Goduplicate():
    with open("proxy_ip.txt", encoding='utf-8') as urls:
        url = urls.readlines()
    news_url = []
    for id in url:
        if id not in news_url:
            news_url.append(id)
    for i in range(len(news_url)):
        with open("proxy_ips.txt", 'a') as edu:
            edu.write(news_url[i])
    os.remove("proxy_ip.txt")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    proxy_spider()
