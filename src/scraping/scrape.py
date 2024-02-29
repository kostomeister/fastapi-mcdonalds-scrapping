from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.mcdonalds.com/"
FILE_PATH = "..\\..\\mcdonalds_menu.json"
DETAIL_LINK = "#accordion-29309a7a60-item-9ea8a10642"


def parse_page():
    driver.get(BASE_URL + "ua/uk-ua/eat/fullmenu.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cmp-category__item")))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_soups = soup.find_all("li", class_="cmp-category__item")
    products_data = []

    for product_soup in product_soups:
        pass

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(products_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    parse_page()
    driver.quit()
