from loguru import logger


@logger.catch
def logger_get_pages():
    global count_pages
    global total_pages
    count_pages += 1
    total_pages -= 1
    return logger.info(f"Страниц загружено ->>{count_pages}, страниц осталось ->>{total_pages}")


@logger.catch
def logger_get_data() -> object:
    global count_pages
    global total_pages
    count_pages += 1
    total_pages -= 1
    if total_pages != 0:
        return logger.info(f"Страниц обработано ->>{count_pages}, страниц осталось ->>{total_pages}")
    else:
        return logger.info("Сбор данных окончен!")
