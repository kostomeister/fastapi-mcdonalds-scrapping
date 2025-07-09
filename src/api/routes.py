import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import ProductDTO
from src.provider import get_product_service
from src.services.interfaces import IProductService


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["products"])


@router.get("/products", response_model=List[ProductDTO])
async def list_products(svc: IProductService = Depends(get_product_service)):
    logger.info("Listing all products")
    return await svc.list_all()


@router.get("/products/{name}", response_model=ProductDTO)
async def product(name: str, svc: IProductService = Depends(get_product_service)):
    try:
        logger.info("Getting product by name %s", name)
        return await svc.by_name(name)
    except ValueError as exc:
        logger.warning("Product %s not found", name)
        raise HTTPException(404, str(exc))


@router.get("/products/{name}/{field}")
async def product_field(
    name: str, field: str, svc: IProductService = Depends(get_product_service)
):
    try:
        logger.info("Getting field %s for product %s", field, name)
        return {field: await svc.field(name, field)}
    except ValueError as exc:
        logger.warning("Field %s for product %s not found", field, name)
        raise HTTPException(404, str(exc))
