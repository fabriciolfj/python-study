from bson import ObjectId
from fastapi import HTTPException, APIRouter
from model.Car import Car
from model.CarCreateResponse import CarCreateResponse
from model.CarResponse import CarResponse
from database import get_collection

router = APIRouter(prefix="/api/v1", tags=["cars"])

@router.get("/car", response_model=list[CarResponse])
async def get_cars():
    collection = get_collection("cars")
    cars = []
    async for doc in collection.find():
        cars.append(CarResponse(
            id=str(doc["_id"]),
            name=doc["name"],
        ))

    return cars

@router.get("/car/{id}", response_model=Car)
async def get_car(id: str):
    collection = get_collection("cars")

    car = await collection.find_one({"_id": ObjectId(id)})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car["id"] = str(car["_id"])
    return car


@router.post("/car", response_model=CarCreateResponse)
async def create_car(car: Car):
    collection = get_collection("cars")

    doc = {
        **car.model_dump()
    }

    result = await collection.insert_one(doc)
    return CarCreateResponse(
        id=str(result.inserted_id),
    )