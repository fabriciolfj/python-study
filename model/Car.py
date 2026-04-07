from pydantic import BaseModel
from typing import Optional


class Car(BaseModel):
    id: Optional[str] = None
    name: str
    price: float
    available: bool = True