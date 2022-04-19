import json

from loguru import logger
from datetime import datetime as dt

from Computers_parser.sync_parser.logger_methods import logger_get_data


def exception_wrapper(function, variable: str):
    try:
        return function
    except Exception:
        return variable


@logger.catch
def reset_global_count_and_total():
    global count_pages
    global total_pages
    total_pages = 51
    count_pages = 0


@logger.catch
def check_time(func):
    def wrapper(*args, **kwargs):
        start = dt.now()
        func(*args, **kwargs)
        return logger.info(dt.now() - start)

    return wrapper


def return_data_dict(item_data):
    manufacturer_item = exception_wrapper(item_data.find("h1").find("span").text, "no field")
    model_item = exception_wrapper(item_data.find("h1").find("span").find_next("span").text, 'no field')
    price_item = exception_wrapper(item_data.find("p", class_="price").text, "no field")
    bonus_points = exception_wrapper(
        item_data.find("div", class_="block-universal border-gray bg-gray gray right center").find("span",
                                                                                                   class_="green tx16 bold").text,
        "no field")
    article_number = item_data.find("div", class_="clear").find("div", class_="prop-value").text.strip()

    data_dict = {'manufacturer_item': manufacturer_item,
                 'model_item': model_item,
                 'price_item': price_item,
                 'bonus_points': bonus_points,
                 'article_number': article_number}
    return data_dict


def update_data_list_json(data_list_collection: list):
    with open("data_result/data_list.json", "a", encoding="utf-8") as file:
        json.dump(data_list_collection, file, indent=4, ensure_ascii=False)
    logger_get_data()
