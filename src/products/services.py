from fastapi import HTTPException
from typing_extensions import Dict, Optional

from src.repositories.json_repository import JSONRepository


class ProductService:
    def __init__(self, product_repo: JSONRepository) -> None:
        self.product_repo: JSONRepository = product_repo("..\\..\\mcdonalds_menu.json")

    async def get_product(self, product_name: str) -> Optional[Dict[str, str]]:
        product = await self.product_repo.get_one(product_name)

        if product:
            return product

        raise HTTPException(status_code=404, detail="Product with this name does not exist")

    async def get_all_products(self) -> dict[str, dict]:
        return await self.product_repo.get_all()

    async def get_product_field(self, product_name: str, product_field: str) -> Optional[str]:
        product = await self.get_product(product_name)
        if product:
            return {product_field: product.get(product_field)}
        raise HTTPException(status_code=404, detail="No such field in this product")
