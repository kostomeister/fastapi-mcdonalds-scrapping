from typing import List

from fastapi import APIRouter, Depends

from src.dependencies.get_product_service import get_product_service
from src.products.schemas import Product

products_router = APIRouter(prefix="/api/v1")


@products_router.get("/all_products/", response_model=List[Product])
async def get_all_products(product_service=Depends(get_product_service)):
    return await product_service.get_all_products()


@products_router.get("/products/{product_name}", response_model=Product)
async def get_product_by_name(product_name: str, product_service=Depends(get_product_service)):
    return await product_service.get_product(product_name)


@products_router.get("/products/{product_name}/{product_field}")
async def get_product_field(product_name: str, product_field: str, product_service=Depends(get_product_service)):
    return await product_service.get_product_field(product_name, product_field)
