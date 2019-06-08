>>> import json
>>> from multiprocessing import Pool
>>> import requests
>>> from bs4 import BeautifulSoup
>>> import re
>>> import pandas as pd
>>> import pymongo
>>> import openpyxl

>>> class lianjia():
	def __init__(self,city,num,headers):
		self.city=city
		self.num=num
		self.headers=headers
	def pc(self):
		pages=['https://'+self.city+'.lianjia.com/ershoufang/pg{}/'.format(x) for x in range(1,int(self.num)+1)]
		re_gets=[]
		for page in pages:
			get_url = requests.get(page, headers=self.headers)
			re_set = re.compile(r'https://'+self.city+'.lianjia.com/ershoufang/\d\d\d\d\d\d\d\d\d\d\d\d.html',re.I)
			re_get = re_set.findall(get_url.text)
			re_gets.append(re_get)
		e=[]
		for t in range(0,int(self.num)):
			q=list(set(re_gets[t]))
			e+=q
		infos=[]
		for item in e:
			info={}
			res = requests.get(item,headers=self.headers)
			if res.status_code == 200:
				soup = BeautifulSoup(res.text)
				info['标题'] = soup.select('.main')[0].text
				info['总价'] = soup.select('.total')[0].text + '万'
				info['每平方售价'] = soup.select('.unitPriceValue')[0].text
				info['参考总价'] = soup.select('.taxtext')[0].text
				info['建造时间'] = soup.select('.subInfo')[2].text
				info['小区名称'] = soup.select('.info')[0].text
				info['所在区域'] = soup.select('.info a')[0].text + ':' + soup.select('.info a')[1].text
				info['链家编号'] = str(item)[33:].rsplit('.html')[0]
				infos.append(info)
		pd_look = pd.DataFrame(infos)
		pd_look.to_excel('链家二手房.xlsx', sheet_name='链家二手房')
>>> my_problem=lianjia('gz',5,{
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
	})
>>> my_problem.pc()
