from fastapi import FastAPI
from api.cars import router as car_router


app = FastAPI(
    title="seller car",
    version="1.0",
    description="A fastapi app for seller car",
)

app.include_router(car_router)
@app.get("/")
def read_root():
    return {"Hello": "World"}