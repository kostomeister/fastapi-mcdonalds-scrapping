from fastapi import FastAPI

from src.products.routers import products_router

app = FastAPI(description="McDonalds Scrapping")

app.include_router(products_router)
