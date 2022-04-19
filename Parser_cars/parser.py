import requests
from bs4 import BeautifulSoup
from Parser_cars.config import HEADERS, HOST, URL


def get_html(url, params=None):
	return requests.get(url, headers=HEADERS, params=params)


def update_cars(cars, item):
	uah_price = item.find('span', class_="size16")

	cars.append({
		'title': item.find('div', class_="proposition_title").get_text(strip=True),
		'href': HOST + item.find('a', class_="proposition_link").get('href'),
		'usd_price': item.find('span', class_="green").get_text(strip=True),
		'uah_price': uah_price.get_text(strip=True) if uah_price else "price not found",
		'city': item.find('span', class_="item region").get_text(strip=True)
	})


def parse_items(items, cars):
	for item in items:
		update_cars(cars, item)


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_="proposition")
	cars = []
	parse_items(items, cars)
	return cars


def update_cars_list_txt(cars):
	with open('cars_list.txt', 'a', encoding='utf-8') as file:
		for line in cars:
			file.write(f'{line}\n')


def parse():
	html = get_html(URL)
	if html.status_code == 200:
		cars = get_content(html.text)
		update_cars_list_txt(cars)
	else:
		print("Error")


if __name__ == "__main__":
	parse()
