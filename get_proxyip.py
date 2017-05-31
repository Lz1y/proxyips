"""
由Lz1y修改：
1.由Python2修改为Python3
2.将ip写入txt文件中，并且去重复了
3.退出程序时更加优雅

请用python3执行
"""
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import signal
import sys
import os


def handler(signal_num,frame):
	Goduplicate()
	print ("\nDone,the available ip have been put in 'proxy_ips.txt'...")
	print ("\nSucceed to exit.")
	sys.exit(signal_num)


def proxy_spider():
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	for i in range(900):		
		url='http://www.xicidaili.com/wt/'+str(i)
	
		r=requests.get(url=url,headers=headers)
		html = r.text
		#print r.status_code
		soup= BeautifulSoup(html, "html.parser")
		datas=soup.find_all(name='tr',attrs={'class':re.compile('|[^odd]')})
		for data in datas:
			soup_proxy= BeautifulSoup(str(data) , "html.parser")	
			proxy_contents=soup_proxy.find_all(name='td')
			ip_org=str(proxy_contents[1].string)
			ip="http://"+ip_org
			port=str(proxy_contents[2].string)
			protocol=str(proxy_contents[5].string)
			proxy_check(ip,port,protocol)
	
def proxy_check(ip,port,protocol):
	proxy={}
	proxy[protocol.lower()]='%s:%s'%(ip,port)
	#print proxy
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	try:
		r=requests.get(url='http://1212.ip138.com/ic.asp',headers=headers,proxies=proxy,timeout=5) #
		ip_available=re.findall(r'\[(.*?)\]',r.text)[0]
		ip_availables="http://"+ip_available
		if ip_availables==ip:
			print (str(proxy)+'is ok')
			with open("proxy_ip.txt",'a',encoding="utf-8") as ip:
				ip.write(ip_available+':'+port + '\n')
				
	except Exception as e:
		#print e
		pass
		
def Goduplicate():
	with open("proxy_ip.txt",encoding = 'utf-8') as urls:
		url = urls.readlines()	
	news_url = []
	for id in url:
		if id not in news_url:
			news_url.append(id)
	for i in range(len(news_url)):
		with open("proxy_ips.txt",'a') as edu:
			edu.write(news_url[i])
	os.remove("proxy_ip.txt")
		
		
if __name__ == '__main__':
	signal.signal(signal.SIGINT, handler)
	proxy_spider()