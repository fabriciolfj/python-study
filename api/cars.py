from fastapi import HTTPException, APIRouter
from model.Car import Car


router = APIRouter(prefix="/api/v1", tags=["cars"])

db: dict[int, Car] = {}
count = 1


@router.get("/car", response_model=list[Car])
def get_cars():
    return db.values()

@router.get("/car/{id}", response_model=Car)
def get_car(id: int):
    car = db.get(id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.post("/car", response_model=Car)
def create_car(car: Car):
    global count
    car.id = count
    db[count] = car
    count += 1
    return car