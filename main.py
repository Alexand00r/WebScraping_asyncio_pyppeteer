import asyncio
from selenium import webdriver
import csv
import time
from pyppeteer import launch

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(
    executable_path="chromedriver.exe",
    options=options
)


def process_page(hotel_code_row, browser):
    hotel_code_bytes = hotel_code_row[0].encode()
    hotel_code = hotel_code_bytes.decode()
    url = "https://ostrovok.ru/rooms/" + hotel_code

    driver.get(url=url)

    try:
        value = driver.find_element_by_class_name("zenroomspageperks-rating-info-total-value")
        result_text = hotel_code + "; " + value.text + "\n"
    except:
        result_text = hotel_code + "; " + "null\n"

    with open("code_with_rating_async.txt", "a", encoding='utf-8') as file:
        file.write(result_text)


async def main():
    browser = await launch()
    with open("maps_collection_async.csv", 'r', encoding="utf-8-sig") as fd:
        hotel_code_rows = csv.reader(fd)

        loop = asyncio.get_event_loop()
        tasks = [process_page(hotel_code_row, browser) for hotel_code_row in hotel_code_rows]
        print("Here we go!")
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
