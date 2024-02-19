from pydantic import BaseModel
from enum import Enum


class PizzaType(str, Enum):
    margherita: str = "MARGHERITA"
    peperoni: str = "PEPERONI"
    capricciosa: str = "CAPRICCIOSA"


class PizzaSize(str, Enum):
    small: str = "S"
    medium: str = "M"
    large: str = "L"


class PizzaBase(BaseModel):
    pizza_type: PizzaType
    size: PizzaSize


class PizzaCreate(PizzaBase):
    ...


class Pizza(PizzaBase):
    pizza_id: int
    price: float
    user_id: int


class Message(BaseModel):
    message: str
