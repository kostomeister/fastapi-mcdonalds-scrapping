import logging
from typing import List

from src.api.schemas import ProductDTO
from src.services.interfaces import IProductService
from src.data.interfaces import IProductRepository

logger = logging.getLogger(__name__)


class ProductService(IProductService):
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    async def list_all(self) -> List[ProductDTO]:
        logger.info("Reading all products from repository")
        return [ProductDTO(**p) for p in await self._repo.read_all()]

    async def by_name(self, name: str) -> ProductDTO:
        logger.info("Searching for product %s", name)
        for p in await self._repo.read_all():
            if p["name"].lower() == name.lower():
                logger.debug("Product %s found", name)
                return ProductDTO(**p)
        logger.debug("Product %s not found", name)
        raise ValueError("Product not found")

    async def field(self, name: str, field: str) -> str:
        prod = await self.by_name(name)
        if hasattr(prod, field):
            logger.debug("Returning field %s for product %s", field, name)
            return getattr(prod, field)
        logger.debug("Field %s not found in product %s", field, name)
        raise ValueError("No such field")
