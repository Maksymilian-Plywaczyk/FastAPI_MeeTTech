import random
from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Body, Depends

from .schemas import Pizza, PizzaCreate
from .local_database import pizza_database
from .helpers import get_pizza_by_id, get_user_pizza_by_id

app = FastAPI(title="Pizza delivery API")


@app.get("/pizzas/", status_code=status.HTTP_200_OK, response_model=Pizza)
def get_pizza(pizza: Annotated[Pizza, Depends(get_pizza_by_id)]):
    try:
        return pizza
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="That pizza is not in our database!",
        )


@app.get(
    "/{user_id}/pizzas/", status_code=status.HTTP_200_OK, response_model=list[Pizza]
)
def get_user_pizzas(user_id: int):
    try:
        return list(filter(lambda pizza: pizza["user_id"] == user_id, pizza_database))
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@app.post("/pizzas/", status_code=status.HTTP_201_CREATED, response_model=Pizza)
def create_pizza(pizza_create: PizzaCreate):
    try:
        pizza_id = random.randint(0, 100)
        price = round(random.uniform(0.00, 10.00), 2)
        new_pizza = Pizza(
            pizza_id=pizza_id, price=price, user_id=1, **pizza_create.dict()
        )
        pizza_database.append(new_pizza)
        return new_pizza
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@app.put("/pizzas/{user_id}/{pizza_id}", status_code=status.HTTP_200_OK)
def update_status_pizza(
    pizza: Annotated[Pizza, Depends(get_user_pizza_by_id)],
    status_pizza=Body(embed=True),
):
    try:
        pizza["status"] = status_pizza
        return {"message": f"Successfully update pizza with id {pizza.pizza_id}"}
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong"
        )


@app.delete("/pizzas/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_pizza(pizza: Annotated[Pizza, Depends(get_user_pizza_by_id)]):
    try:
        pizza_database.remove(pizza)
        return None
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong"
        )
