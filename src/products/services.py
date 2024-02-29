from typing_extensions import Dict, Optional

from src.repositories.json_repository import JSONRepository


class ProductService:
    def __init__(self, product_repo: JSONRepository) -> None:
        self.product_repo: JSONRepository = product_repo

    async def get_product(self, product_name: str) -> Optional[Dict[str, str]]:
        return await self.product_repo.get_one(product_name)

    async def get_all_products(self) -> dict[str, dict]:
        return await self.product_repo.get_all()

    async def get_product_field(self, product_name: str, product_field: str) -> Optional[str]:
        product = await self.get_product(product_name)
        if product is not None:
            return product.get(product_field)
        return None
