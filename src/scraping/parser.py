import logging
from typing import List, Dict

from bs4 import BeautifulSoup

from src.scraping.interfaces import IParser

logger = logging.getLogger(__name__)


class McdParser(IParser):
    def extract_links(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, "lxml")
        links = [a["href"] for a in soup.select("li.cmp-category__item a[href]")]
        logger.info("Extracted %d product links", len(links))
        return links

    def parse(self, html: str) -> Dict:
        soup = BeautifulSoup(html, "lxml")
        right = soup.select_one("div.cmp-product-details-main__right-rail")
        nutri = soup.select_one("#pdp-nutrition-summary")

        name = right.select_one(
            "span.cmp-product-details-main__heading-title"
        ).text.strip()
        desc = right.select_one("div.cmp-text").text.strip()

        data = {}
        for li in nutri.select("ul.cmp-nutrition-summary__heading-primary li"):
            val, key = li.select_one("span.sr-only.sr-only-pd").text.split(maxsplit=1)
            data[key.strip()] = val.strip(":")
        for li in nutri.select(
            "div.cmp-nutrition-summary__details-column-view-desktop li"
        ):
            key = li.select_one("span.metric").text.strip(":")
            val = li.select_one("span.value span").text.split()[0]
            data[key] = val

        logger.debug("Parsed product %s", name)
        return {
            "name": name,
            "description": desc,
            "calories": data.get("Калорійність", ""),
            "fats": data.get("Жири", ""),
            "carbs": data.get("Вуглеводи", ""),
            "proteins": data.get("Білки", ""),
            "unsaturated_fats": data.get("НЖК", ""),
            "sugar": data.get("Цукор", ""),
            "salt": data.get("Сіль", ""),
            "portion": data.get("Порція", ""),
        }
