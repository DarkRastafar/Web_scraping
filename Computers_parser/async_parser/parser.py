import json
import asyncio
import aiohttp
import requests
from datetime import datetime as dt
from loguru import logger
from bs4 import BeautifulSoup


total_pages = 51
count_pages = 0

HEADERS = {
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
	}
DOMAIN = "https://www.xcomspb.ru"
data_list_collection = []


def logger_get_data():
	global count_pages
	global total_pages
	count_pages += 1
	total_pages -= 1
	if total_pages != 0:	
		return logger.info(f"Страниц обработано ->>{count_pages}, страниц осталось ->>{total_pages}")
	else:
		return logger.info("Сбор данных окончен!")


def check_time(func):
	def wrapper(*args, **kwargs):
		start = dt.now()
		func(*args, **kwargs)
		end = dt.now() - start
		return logger.info(f"Время работы скрапера составило: {end}")
	return wrapper


async def get_page_data(session, number_page):
	url = f"https://www.xcomspb.ru/search/kompyuter_i_kompyuternaya_platforma/?o=n&s=%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80&search_page={number_page}"
	

	async with session.get(url=url, headers=HEADERS) as responce:
		responce_text = await responce.text()

		soup = BeautifulSoup(responce_text, "lxml")
		items_collection = soup.find_all("div", class_="item border-gray")
		items_collection_urls = [DOMAIN + item.find("div", class_="name").find("a").get("href")[:-5] for item in items_collection]
		counter_items = 0
		logger.info(f"{number_page} страница обрабатывается")

		for urls in items_collection_urls:
			async with session.get(url=urls, headers=HEADERS) as responce:
				responce_text = await responce.text()
			
				soup = BeautifulSoup(responce_text, "lxml")

				try:
					item_data = soup.find("div", class_="catalog cart")
					counter_items += 1
					logger.info(f"{counter_items} позиция обработана")
				except Exception:
					print("404_Page_not_found")


				try:
					manufacturer_item = item_data.find("h1").find("span").text
					#logger.info("Производитель получен")
				except Exception:
					manufacturer_item = "no field"

				try:
					model_item = item_data.find("h1").find("span").find_next("span").text
					#logger.info("Модель получена")
				except Exception:
					model_item = "no field"

				try:
					price_item = item_data.find("p", class_="price").text
					#logger.info("Цена получена")
				except Exception:
					price_item = "no field"

				try:
					bonus_points = item_data.find("div", class_="block-universal border-gray bg-gray gray right center").find("span", class_="green tx16 bold").text
					#logger.info("Бонусные баллы получены")
				except Exception:
					bonus_points = "no field"

				try:
					part_number = item_data.find("div", class_="clear").find("div", class_="prop-value").text.strip()
					#logger.info("Артикул производителя получен")
				except Exception:
					part_number = "no field"
				
				data_list_collection.append(
						{
							"Производитель": manufacturer_item,
							"Модель": model_item,
							"Цена": price_item,
							"Бонусные баллы": bonus_points,
							"Артикул производителя": part_number
						}
					)
		logger_get_data()



async def gather_data():
	async with aiohttp.ClientSession() as session:
		tasks = []

		for number_page in range(1, 2):
			task = asyncio.create_task(get_page_data(session, number_page))
			tasks.append(task)

		await asyncio.gather(*tasks)


def write_data(data_list_collection):
	with open("data_result/data_list.json", "a", encoding="utf-8") as file:
		json.dump(data_list_collection, file, indent=4, ensure_ascii=False)


@check_time
def facad_parser():
	asyncio.run(gather_data())
	write_data(data_list_collection)


if __name__ == "__main__":
	facad_parser()