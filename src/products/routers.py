from typing import List

from fastapi import APIRouter, Depends

from src.dependencies.get_product_service import get_product_service
from src.products.schemas import Product

products_router = APIRouter()


@products_router.get("/all_products/")
async def get_all_products(product_service=Depends(get_product_service)):
    return await product_service.get_all_products()
