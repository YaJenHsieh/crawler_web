import requests
from bs4 import BeautifulSoup
import time

#定義資料
url = 'https://tip.railway.gov.tw/tra-tip-web/tip'
sta_dic = {} #設變數放等等找到的火車站名稱、代碼
today = time.strftime('%Y/%m/%d') #設今天的日期
s_time = '06:00' # s 起始時間
e_time = '12:00' # e 結束時間

def get_trip():   #定義函式，以下爬蟲都會在函式執行
	resp = requests.get(url) #設變數resp接，主機回傳的response
	if resp.status_code != 200:  #先確認代碼是否回傳成功
		print(f'URL發生錯誤:{url}') #如果不等於200，則印出錯誤警示
		return  #如果成功就返回

	#將HTML原始碼解析後，取得一個BeautifulSoup物件
	soup = BeautifulSoup(resp.text,'lxml') #將解析後的物件，開始擷取資料
	stations = soup.select('#cityHot > ul > li') #取得車站代碼
	for station in stations: #跑每一個 li 裡面的車站
		station_name = station.button.get_text() #車站包在button裡面
		station_id = station.button['title'] #[ ]取得屬性的值！！！
		sta_dic[station_name] = station_id #車站名稱放在字典變數的key值，車站名稱對應車站代碼的字典
		# print(f'>>>>>{stationName}<<<<<')

	csrf = soup.select('#queryForm > input')[0].get('value')
	# print(f">>>>>{csrf}<<<<<")

	form_data = {    #回傳表單字典型態的變數
		'trainTypeList' : 'ALL',
		'transfer' : 'ONE',
		'startOrEndTime' : 'true',
		'startStation' : sta_dic['臺北'],
		'endStation' : sta_dic['新竹'],
		'rideDate' : today,
		'startTime' : s_time,
		'endTime' : e_time,
		}
	# print(f'>>>>>{formData}<<<<<')

	query_url = soup.select('#queryForm')[0].get('action') #傳送表單的網址
	# print(f'>>>>>{queryUrl}<<<<<')
	q_resp = requests.post('https://tip.railway.gov.tw'+query_url , data = form_data) #使用requests傳送表單給台鐵主機（post)，使用台鐵domain結合剛剛找到的網址(傳送表單查詢車次的網址,表單資訊)
	q_soup = BeautifulSoup(q_resp.text,'lxml') #將解析後的物件
	trs = q_soup.select('.trip-column')
	# print(f'>>>>>{trs}<<<<<')
	for tr in trs:
		td = tr.select('td')
		# print(f'>>>>>{td}<<<<<')
		print(f'{td[0].ul.li.a.get_text()} : {td[1].get_text()} - {td[2].get_text()}')

if __name__ == '__main__':#程式碼在程式被引用時"不會"執行，只要自己在執行的時候會呼叫，這樣就可以"避免呼叫別的檔案的函式時又被執行"。__name__ 是 python 中內建、隱含的變數。
	get_trip()

