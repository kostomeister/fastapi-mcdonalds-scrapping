import logging

from playwright.async_api import async_playwright

from src.scraping.interfaces import IFetcher
from src.core.settings import settings

logger = logging.getLogger(__name__)


class PlaywrightFetcher(IFetcher):
    def __init__(self, timeout_ms: int = settings.scraper_timeout_ms):
        self._timeout = timeout_ms

    async def fetch(self, url: str) -> str:
        logger.info("Fetching %s", url)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=settings.headless)
            page = await browser.new_page(user_agent=settings.user_agent)
            await page.goto(url, timeout=self._timeout)
            await page.wait_for_load_state("networkidle")
            html = await page.content()
            await browser.close()
            logger.debug("Fetched %d characters from %s", len(html), url)
            return html
