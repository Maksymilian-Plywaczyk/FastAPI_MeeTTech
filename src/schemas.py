from pydantic import BaseModel
from enum import Enum


class PizzaType(str, Enum):
    MARGHERITA: str = "MARGHERITA"
    PEPPERONI: str = "PEPPERONI"
    CAPRICCIOSA: str = "CAPRICCIOSA"


class PizzaSize(str, Enum):
    SMALL: str = "S"
    MEDIUM: str = "M"
    LARGE: str = "L"


class PizzaStatus(str, Enum):
    DONE: str = "Done"
    UNDONE: str = "Undone"


class PizzaBase(BaseModel):
    pizza_type: PizzaType
    size: PizzaSize
    additional_info: str | None = None


class PizzaCreate(PizzaBase):
    ...


class Pizza(PizzaBase):
    pizza_id: int
    price: float
    user_id: int
    status: str = PizzaStatus.UNDONE.value


class User(BaseModel):
    id: int
    fullname: str
    email: str
    hashed_password: str
    pizzas: list[Pizza]
