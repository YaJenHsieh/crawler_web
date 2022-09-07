from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd

'''成人商品，目前先跳過，之後再教'''
# https://www.zeczec.com//projects/siangcup


def get_crawler_zeczec():
	url = 'https://www.zeczec.com/'
	soup = get_soup(url)

	page_list = soup.select('.container .container .button')
	last_page = int(page_list[-2].get_text()) # 找出動態頁數的最後一頁，目前最後一頁是11

	output = []
	for page_num in range(1,last_page+1)[0:1]: # 先限制第一頁
		page_url = f'https://www.zeczec.com/?page={page_num}'
		page_soup = get_soup(page_url)

		# 找出當前頁面所有的募資項目網址，1頁有15個項目（所以要有15個網址）
		projects_href_list = page_soup.select('.container .container .block')
		for projects_href in projects_href_list[0:1]:
			projects_url = url + projects_href.get('href')
			result = get_parsing_data(projects_url)
			output.append(result)

	df = pd.DataFrame(output)

	now = pd.Timestamp('now').normalize() # 現在時間
	today_30 = pd.offsets.Day(30) # 30天的時間
	dt = df['開始時間'].between(now - today_30,now) #計算30天的時間
	df = df[dt] # 計算從今天到30天前，以內的資料

	df = df.sort_values(by=['目前募資金額'],ascending=False) # 金額由大排到小
	df.to_csv('./data/zeczec_new_projects_Jenny.csv',index=False)
	print(df)
	
	
def get_parsing_data(projects_url):
	soup = get_soup(projects_url)

	title = soup.select('.w-full a h2')[0].get_text().strip() if len(soup.select('.w-full a h2')) > 0 else ''
	# 斷點寫法，如果出現 "projects_url:https://www.zeczec.com//projects/siangcup, title:    "，就是出現問題
	# print(f'projects_url:{projects_url}, title:{title}')

	money = soup.select('.text-2xl.font-bold.js-sum-raised')  
	money_text = money[0].text.strip() if money else ''  # 空值無法使用int()
	current_money = int(money_text.replace('NT$','').replace(',','')) if money_text else ''

	sponsor_num = int(soup.select('.js-backers-count')[0].text.strip()) if len(soup.select('.js-backers-count')) else ''
	
	time_limit = soup.select('.mb-2.text-xs.leading-relaxed')[0].text.strip() if len(soup.select('.mb-2.text-xs.leading-relaxed')) > 0 else ''
	time_range = time_limit.replace('時程\n', '').replace('開始於\n','').split('–')
	start_time = time_range[0].strip().replace('/','-') if len(time_range) > 0 else ''
	end_time = time_range[1].strip().replace('/','-') if len(time_range) > 1 else ''


	dateFormatter = "%Y-%m-%d %H:%M"  # 時間改成 datetime 格式
	if len(start_time) > 0:
		start_time = datetime.strptime(start_time,dateFormatter)
	if len(end_time) > 0:
		end_time = datetime.strptime(end_time,dateFormatter)
	
	result_dict = {
		'募資項目名稱' : title,
		'募資項目網址' : projects_url,
		'目前募資金額' : current_money,
		'贊助人數' : sponsor_num,
		'開始時間' : start_time,
		'結束時間' : end_time,
	}
	# print(result_dict) # print出來，確定跑出來的進度
	time.sleep(6)
	return result_dict

def get_soup(url):
	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
	}
	res = requests.get(url,headers = headers)
	soup = bs(res.text,'lxml')
	return soup

if __name__ == '__main__':
	get_crawler_zeczec()
