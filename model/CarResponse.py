from pydantic import BaseModel


class CarResponse(BaseModel):
    id: str
    name: str