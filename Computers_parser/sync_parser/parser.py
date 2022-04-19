import requests
from loguru import logger
from bs4 import BeautifulSoup
from Computers_parser.sync_parser.functions import check_time, reset_global_count_and_total, exception_wrapper, \
	update_data_list_json, return_data_dict
from Computers_parser.sync_parser.logger_methods import logger_get_pages
from config import HEADERS, DOMAIN, PAGINATE_URL

total_pages = 51
count_pages = 0
data_list_collection = []


@logger.catch
@check_time
def get_pages(url):
	for number_page in range(1, 52):
		url = f"{url}&search_page={number_page}"
		req = requests.get(url, HEADERS)

		with open(f"pages/page{number_page}.html", "w", encoding="utf-8") as f:
			f.write(req.text)
		logger_get_pages()
	reset_global_count_and_total()


def parse_collection_urls(items_collection_urls, counter_items):
	for urls in items_collection_urls:
		req = requests.get(urls, HEADERS)
		item_name = urls.split("/")[-1]

		with open(f"pages/data/{item_name}.html", "w", encoding="utf-8") as file:
			file.write(req.text)

		with open(f"pages/data/{item_name}.html", encoding="utf-8") as file:
			soup = BeautifulSoup(file.read(), "lxml")
			try:
				item_data = soup.find("div", class_="catalog cart")
				counter_items += 1
				logger.info(f"{counter_items} позиция обработана")

				data_dict = return_data_dict(item_data)

				data_list_collection.append(
					{
						"Производитель": data_dict['manufacturer_item'],
						"Модель": data_dict['model_item'],
						"Цена": data_dict['price_item'],
						"Бонусные баллы": data_dict['bonus_points'],
						"Артикул производителя": data_dict['article_number']
					}
				)
			except Exception:
				logger.info("404_Page_not_found")


@logger.catch
@check_time
def get_data():
	for number_page in range(1, 52):
		with open(f"pages/page{number_page}.html", encoding="utf-8") as f:
			counter_items = 0
			soup = BeautifulSoup(f.read(), "lxml")

			items_collection = soup.find_all("div", class_="item border-gray")
			items_collection_urls = [DOMAIN + item.find("div", class_="name").find("a").get("href")[:-5]
									 for item in items_collection]
			parse_collection_urls(items_collection_urls, counter_items)
			update_data_list_json(data_list_collection)


@logger.catch
@check_time
def main():
	get_pages(PAGINATE_URL)
	get_data()


if __name__ == "__main__":
	main()
