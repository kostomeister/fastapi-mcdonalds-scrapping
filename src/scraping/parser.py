import logging, re
from typing import Dict, List
from bs4 import BeautifulSoup, Tag
from src.scraping.interfaces import IParser

logger = logging.getLogger(__name__)


class McdParser(IParser):
    _NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")

    def extract_links(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, "lxml")
        links = [a["href"] for a in soup.select("li.cmp-category__item a[href]")]
        logger.info("Extracted %d product links", len(links))
        return links

    @staticmethod
    def _clean(text: str) -> str:
        return text.replace("\u00a0", " ").strip().rstrip(":")

    def _val(self, node: Tag) -> str:
        raw = node.get_text(strip=True).replace(",", ".")
        m = self._NUM_RE.search(raw)
        return m.group(1) if m else ""

    def parse(self, html: str) -> Dict[str, str]:
        soup = BeautifulSoup(html, "lxml")
        right = soup.select_one("div.cmp-product-details-main__right-rail")
        nutri = soup.select_one("#pdp-nutrition-summary")

        name = right.select_one(
            "span.cmp-product-details-main__heading-title"
        ).text.strip()
        desc = right.select_one("div.cmp-text").text.strip()

        data: Dict[str, str] = {}

        for li in nutri.select("ul.cmp-nutrition-summary__heading-primary li"):
            key = self._clean(li.select_one("span.metric").text.split("(")[0])
            val = self._val(li.select_one('span.value [aria-hidden="true"]'))
            data[key] = val

        for li in nutri.select(
            "div.cmp-nutrition-summary__details-column-view-desktop li"
        ):
            key = self._clean(li.select_one("span.metric").text)
            val = self._val(li.select_one('span.value [aria-hidden="true"]'))
            data[key] = val

        logger.debug("Parsed %s → %s", name, data)
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
