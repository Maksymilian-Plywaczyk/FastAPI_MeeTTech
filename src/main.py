import random
from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Depends

from .schemas import Pizza, PizzaCreate, User, PizzaStatus
from .local_database import pizza_database
from .helpers import get_pizza_by_id, get_user_pizza_by_id
from .auth import auth_route, get_user

app = FastAPI(title="Pizza delivery API")
app.include_router(auth_route)


@app.get("/pizzas/{pizza_id}", status_code=status.HTTP_200_OK, response_model=Pizza)
def get_pizza(pizza: Annotated[Pizza, Depends(get_pizza_by_id)]):
    try:
        return pizza
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="That pizza is not in our database!",
        )


@app.get(
    "/pizzas/", status_code=status.HTTP_200_OK, response_model=list[Pizza]
)
def get_user_pizzas(user: Annotated[User, Depends(get_user)]):
    try:
        return list(filter(lambda pizza: pizza["user_id"] == user.id, pizza_database))
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@app.post("/pizzas/", status_code=status.HTTP_201_CREATED, response_model=Pizza)
def create_pizza(pizza_create: PizzaCreate, user: Annotated[User, Depends(get_user)]):
    try:
        pizza_id = random.randint(0, 100)
        price = round(random.uniform(0.00, 10.00), 2)
        new_pizza = Pizza(
            pizza_id=pizza_id, price=price, user_id=user.id, **pizza_create.dict()
        )
        pizza_database.append(new_pizza)
        return new_pizza
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@app.put("/pizzas/{pizza_id}", status_code=status.HTTP_200_OK)
def update_status_pizza(pizza: Annotated[Pizza, Depends(get_user_pizza_by_id)]):
    try:
        index_pizza = pizza_database.index(pizza.dict())
        pizza_database[index_pizza]["status"] = PizzaStatus.DONE.value
        return {"message": f"Successfully update pizza with id {pizza.pizza_id}"}
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong"
        )


@app.delete("/pizzas/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_pizza(pizza: Annotated[Pizza, Depends(get_user_pizza_by_id)]):
    try:
        pizza_database.remove(pizza.dict())
        return None
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong"
        )
