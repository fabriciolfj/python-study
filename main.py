from contextlib import asynccontextmanager

from fastapi import FastAPI
from api.cars import router as car_router
from database import connect, disconnect

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()

app = FastAPI(
    title="seller car",
    version="1.0",
    description="A fastapi app for seller car",
    lifespan=lifespan
)

app.include_router(car_router)
@app.get("/")
def read_root():
    return {"Hello": "World"}