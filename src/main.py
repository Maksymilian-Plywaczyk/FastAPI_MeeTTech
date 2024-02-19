import random

from fastapi import FastAPI, status, HTTPException
from .schemas import Pizza, PizzaCreate, Message

app = FastAPI()

pizza_database = {
    1: {
        "pizza_id": 1,
        "pizza_type": "MARGHERITA",
        "size": "S",
        "price": 5.99,
        "user_id": 1,
    },
    2: {
        "pizza_id": 2,
        "pizza_type": "PEPERONI",
        "size": "M",
        "price": 7.99,
        "user_id": 2,
    },
    3: {
        "pizza_id": 3,
        "pizza_type": "CAPRICCIOSA",
        "size": "L",
        "price": 9.99,
        "user_id": 1,
    },
    4: {
        "pizza_id": 4,
        "pizza_type": "MARGHERITA",
        "size": "L",
        "price": 8.99,
        "user_id": 1,
    },
    5: {
        "pizza_id": 5,
        "pizza_type": "PEPERONI",
        "size": "S",
        "price": 6.99,
        "user_id": 2,
    },
}

user_database = {
    1: {
        "fullname": "Jan Kowalski",
        "email": "jan.kowalski@gmail.com",
        "password": "",
        "pizzas": [],
    },
    2: {
        "fullname": "Adam Nowak",
        "email": "adam.nowak@gmail.com",
        "password": "",
        "pizzas": [],
    },
}


@app.get("/pizzas/{pizza_id}", status_code=status.HTTP_200_OK, response_model=Pizza)
def get_pizza(pizza_id: int):
    if pizza_database.get(pizza_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="That pizza is not in our database!",
        )
    return Pizza(**pizza_database.get(pizza_id))


@app.post("/pizzas/", status_code=status.HTTP_201_CREATED, response_model=Pizza)
def create_pizza(pizza_create: PizzaCreate):
    pizza_id = random.randint(0, 100)
    price = round(random.uniform(0.00, 10.00), 2)
    new_pizza = Pizza(pizza_id=pizza_id, price=price, user_id=1, **pizza_create.dict())
    try:
        pizza_database.update({pizza_id: new_pizza.dict()})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )
    return new_pizza


@app.delete(
    "pizzas/{user_id}/{pizza_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=Message,
)
def delete_user_pizza(user_id: int, pizza_id: int):
    if not (
        pizza_database.get(pizza_id)
        and pizza_database.get(pizza_id)["user_id"] == user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong"
        )
    pizza_database.pop(pizza_id)
    return Message(message=f"Successfully deleted pizza with id: {pizza_id}")


@app.get(
    "/{user_id}/pizzas/", status_code=status.HTTP_200_OK, response_model=list[Pizza]
)
def get_user_pizzas(user_id: int):
    return [
        Pizza(**pizza)
        for pizza in pizza_database.values()
        if pizza["user_id"] == user_id
    ]
