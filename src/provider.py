import logging
from functools import lru_cache

from src.core.settings import settings
from src.data.file_repo import JSONRepo
from src.services.product_service import ProductService
from src.scraping.fetcher import PlaywrightFetcher
from src.scraping.parser import McdParser
from src.scraping.pipeline import McdScraper

logger = logging.getLogger(__name__)


@lru_cache
def get_repo() -> JSONRepo:
    repo = JSONRepo(settings.json_path)
    logger.info("JSON repository created")
    return repo


@lru_cache
def get_product_service() -> ProductService:
    svc = ProductService(get_repo())
    logger.info("Product service instantiated")
    return svc


def get_scraper() -> McdScraper:
    logger.info("Creating scraper")
    return McdScraper(
        fetcher=PlaywrightFetcher(timeout_ms=settings.scraper_timeout_ms),
        parser=McdParser(),
        file_path=settings.json_path,
    )
