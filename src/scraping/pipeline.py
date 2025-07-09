import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict

from src.scraping.interfaces import IScraper, IFetcher, IParser
from src.core.settings import settings

logger = logging.getLogger(__name__)


class McdScraper(IScraper):

    def __init__(self, fetcher: IFetcher, parser: IParser, file_path: Path):
        self._fetcher, self._parser, self._file = fetcher, parser, file_path
        self._sem = asyncio.Semaphore(settings.scraper_concurrency)

    async def _fetch_parse_one(self, href: str, base: str, detail: str) -> Dict:
        async with self._sem:
            html = await self._fetcher.fetch(f"{base}{href}{detail}")
        return self._parser.parse(html)

    async def scrape(self) -> List[Dict]:
        base, detail = settings.base_url, settings.detail_anchor
        logger.info("Scraping index page")
        index_html = await self._fetcher.fetch(f"{base}ua/uk-ua/eat/fullmenu.html")
        links = self._parser.extract_links(index_html)
        logger.info("Found %d product links", len(links))

        tasks = [self._fetch_parse_one(href, base, detail) for href in links]
        products = await asyncio.gather(*tasks)

        self._file.write_text(json.dumps(products, ensure_ascii=False, indent=4))
        logger.info("Saved %d products to %s", len(products), self._file)
        return products


if __name__ == "__main__":
    from src.scraping.fetcher import PlaywrightFetcher
    from src.scraping.parser import McdParser

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    scraper = McdScraper(PlaywrightFetcher(), McdParser(), settings.json_path)
    asyncio.run(scraper.scrape())
