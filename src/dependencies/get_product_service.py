from src.products.services import ProductService
from src.repositories.json_repository import JSONRepository


def get_product_service():
    return ProductService(JSONRepository)

