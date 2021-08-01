import requests
import os
from bs4 import BeautifulSoup

# создаем две константные переменные. 1 - адрес страницы откуда будем тянуть инфу 
# 2 - вписываем чтобы сайт не заблочил нас, посчитав, что мы его ломаем.
URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
           'accept': '*/*'}
HOST = 'https://auto.ria.com'

def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_="proposition")

	cars = []

	for item in items:
		uah_price = item.find('span', class_="size16")
		if uah_price:
			uah_price = uah_price.get_text(strip=True)
		else:
			uah_price = "price not found"

		cars.append({
			         'title'    : item.find('div', class_="proposition_title").get_text(strip=True),
			         'href'     : HOST + item.find('a', class_="proposition_link").get('href'),
			         'usd_price': item.find('span', class_="green").get_text(strip=True),
			         'uah_price': uah_price,\
			         'city'     : item.find('span', class_="item region").get_text(strip=True)
			         })

	return cars

def parse():
	html = get_html(URL)
	if html.status_code == 200:
		cars = get_content(html.text)
		with open('cars_list.txt', 'a', encoding='utf-8') as file:
			for line in cars:
				file.write(f'{line}\n')	
	else:
		print("Error")


parse()