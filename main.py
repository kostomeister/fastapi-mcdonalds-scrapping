from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(description="McDonalds Scrapping")

app.include_router(router)
