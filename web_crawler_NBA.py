import requests
from bs4 import BeautifulSoup
import time

today = time.strftime('%m/%d').lstrip('0')

def pttNBA(url):
	resp = requests.get(url)
	if resp.status_code != 200:  #先確認代碼是否回傳成功，再進行下去
		print(f'URL發生錯誤{url}')
		return

	#將HTML原始碼解析後，取得一個BeautifulSoup物件
	soup = BeautifulSoup(resp.text,'lxml')
	paging = soup.select('.btn.wide')[1].get('href') #上頁連結

	articles = []
	rents = soup.select('.r-ent')
	for rent in rents:
		title = rent.select('.title')[0].get_text().strip() #strip()去掉空白字元
		count = rent.select('.nrec')[0].get_text().strip()
		date = rent.select('.date')[0].get_text().strip()
		article = f'{date} {count}:{title}'

		try:
			if today == date and int(count) > 10:
				articles.append(article)
		except:
			if today == date and count =='爆':
				articles.append(article)

	if len(articles) != 0:
		for article in articles:
			print(article)
		pttNBA(f'https://www.ptt.cc{paging}') #呼叫同一個函式pttNBA（ ）繼續找前面的文章
	else:
		return

if __name__ == '__main__':
	#程式碼在程式被引用時"不會"執行，只要自己在執行的時候會呼叫，這樣就可以"避免呼叫別的檔案的函式時又被執行"。__name__ 是 python 中內建、隱含的變數。
	url='https://www.ptt.cc/bbs/NBA/index.html'
	pttNBA(url)