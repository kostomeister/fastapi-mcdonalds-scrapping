import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.mcdonalds.com/"
FILE_PATH = "..\\..\\mcdonalds_menu.json"
DETAIL_LINK = "#accordion-29309a7a60-item-9ea8a10642"


def parse_product(product):
    product_link = BASE_URL + product.find("a")["href"] + DETAIL_LINK
    driver.get(product_link)

    time.sleep(0.25)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pdp-nutrition-summary")))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    main_info = soup.find("div", class_="cmp-product-details-main__right-rail")
    nutrition_info = soup.find("div", id="pdp-nutrition-summary")

    name = main_info.find("span", class_="cmp-product-details-main__heading-title").text.strip()
    description = main_info.find("div", class_="cmp-text").text.strip()

    nutrition_data = {}
    primary_nutrients = nutrition_info.find("ul", class_="cmp-nutrition-summary__heading-primary")
    secondary_nutrients = nutrition_info.find("div", class_="cmp-nutrition-summary__details-column-view-desktop").find("ul")

    for nutrient in primary_nutrients.find_all("li"):
        nutrient_text = nutrient.find("span", class_="sr-only sr-only-pd").text.strip()
        nutrient_split = nutrient_text.split(" ")
        nutrient_value = nutrient_split[0].strip(':')
        nutrient_name = nutrient_split[1].strip()
        nutrition_data[nutrient_name] = nutrient_value

    for nutrient in secondary_nutrients.find_all("li"):
        nutrient_name = nutrient.find("span", class_="metric").text.strip().strip(':')
        nutrient_value = nutrient.find("span", class_="value").find("span").text.strip()
        nutrient_split = nutrient_value.split()
        nutrition_data[nutrient_name] = nutrient_split[0]

    return {
        "name": name,
        "description": description,
        "calories": nutrition_data.get('Калорійність', ''),
        "fats": nutrition_data.get('Жири', ''),
        "carbs": nutrition_data.get('Вуглеводи', ''),
        "proteins": nutrition_data.get('Білки', ''),
        "unsaturated_fats": nutrition_data.get('НЖК', ''),
        "sugar": nutrition_data.get('Цукор', ''),
        "salt": nutrition_data.get('Сіль', ''),
        "portion": nutrition_data.get('Порція', '')
    }


def parse_page():
    driver.get(BASE_URL + "ua/uk-ua/eat/fullmenu.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cmp-category__item")))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_soups = soup.find_all("li", class_="cmp-category__item")
    products_data = []

    for product_soup in product_soups:
        products_data.append(parse_product(product_soup))

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(products_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    parse_page()
    driver.quit()
