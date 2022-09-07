from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def get_crawler_ptt_stock():
	url = 'https://www.ptt.cc/bbs/Stock/index.html'
	soup = get_soup(url)
	previous_page = soup.select('.action-bar .btn-group-paging a')[1]['href']
	previous_page_num = int(previous_page.replace('/bbs/Stock/index','').replace('.html',''))
	print(previous_page)

	###當前頁數:上一頁的頁數+1
	current_page_num = previous_page_num +1

	###抓取 前5頁 文章列表的資料	output = []
	for i in range(5):
		page_num = current_page_num -i
		crawler_url = f'https://www.ptt.cc/bbs/Stock/index{page_num}.html'
		crawler_soup = get_soup(crawler_url) 
		result = get_parsing_data(crawler_soup)
		output += result

	###輸出儲存檔案
	df = pd.DataFrame(output)
	# df.to_excel('ptt_stock_Jenny_01.xlsx') #儲存excel檔，不適用api傳輸格式
	# df.to_csv('ptt_stock_Jenny_01.csv') #儲存csv檔，api傳輸格式
	# print('-'*20)
	# print('successfully exported into Excel File')

def get_parsing_data(soup):
	data = soup.select('div.r-ent')
	result = []
	for sample in data:
		title = sample.select('.title')[0].get_text().strip() # 標題

		if '公告' in title or '閒聊' in title or '刪除' in title or '爆' in title: 
			continue

		time = sample.select('.date')[0].get_text().strip() # 時間

		push_num = sample.select('.hl')[0].get_text() if len(sample.select('.hl')) > 0 else 0 # 推文

		#連結:多判斷式，假如抓得到節點 a 才會執行，不然會為空值，避免error
		link = 'No link'
		raw_link = sample.select('div.title a')
		if raw_link:
			raw_link = raw_link[0]['href']
			domain_link = 'https://www.ptt.cc'
			link = domain_link + raw_link
			
		result_dict = {
			'title' : title,
			'time' : time,
			'push_num' : push_num,
			'link' : link,
		}
		# print(result_dict)
		# result.append(result_dict)
	return result

def get_soup(url):
	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
	}
	res = requests.get(url,headers = headers)
	soup = bs(res.text,'lxml')
	return soup

if __name__ == '__main__':
	get_crawler_ptt_stock()