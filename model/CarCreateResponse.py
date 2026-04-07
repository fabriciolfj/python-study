from pydantic import BaseModel


class CarCreateResponse(BaseModel):
    id: str