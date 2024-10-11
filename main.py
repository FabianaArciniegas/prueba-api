from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from api.products.controllers.products_controller import products_router
from api.users.controllers.users_controller import users_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting...")
    env = settings.ENV
    app.mongodb_client = AsyncIOMotorClient(settings.DB_CONNECTION)
    app.database = app.mongodb_client[settings.DB_NAME]
    print(f"Started successfully: {env}")
    yield
    print("Application closing...")
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix=settings.API_STR)
app.include_router(products_router, prefix=settings.API_STR)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
