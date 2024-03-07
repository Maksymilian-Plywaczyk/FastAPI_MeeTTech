from pydantic import BaseModel
from enum import Enum


class PizzaType(str, Enum):
    MARGHERITA = "MARGHERITA"
    PEPPERONI = "PEPPERONI"
    CAPRICCIOSA = "CAPRICCIOSA"


class PizzaSize(str, Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"


class PizzaStatus(str, Enum):
    DONE = "Done"
    UNDONE = "Undone"


class PizzaBase(BaseModel):
    pizza_type: PizzaType
    size: PizzaSize
    additional_info: str | None = None


class PizzaCreate(PizzaBase): ...


class Pizza(PizzaBase):
    pizza_id: str
    price: float
    user_id: int
    status: str = PizzaStatus.UNDONE.value


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    pizzas: list[Pizza]
