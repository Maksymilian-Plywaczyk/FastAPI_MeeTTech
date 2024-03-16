import random
import uuid
from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Depends

from .schemas import Pizza, PizzaCreate, User, PizzaStatus
from .local_database import pizza_database
from .helpers import get_pizza_by_id, get_user_pizza_by_id
from .auth import auth_route, get_user

app = FastAPI(title="Pizza delivery API #MeeTTech")
app.include_router(auth_route)


@app.get("/pizzas/{pizza_id}", status_code=status.HTTP_200_OK, response_model=Pizza)
def get_pizza(pizza: Annotated[Pizza, Depends(get_pizza_by_id)]):
    return pizza


@app.get("/pizzas/", status_code=status.HTTP_200_OK, response_model=list[Pizza])
def get_user_pizzas(user: Annotated[User, Depends(get_user)]):
    return [pizza for pizza in pizza_database if pizza["user_id"] == user.id]


@app.post("/pizzas/", status_code=status.HTTP_201_CREATED, response_model=Pizza)
def create_pizza(pizza_create: PizzaCreate, user: Annotated[User, Depends(get_user)]):
    try:
        pizza_id = str(uuid.uuid4())
        price = round(random.uniform(0.00, 10.00), 2)
        new_pizza = Pizza(
            pizza_id=pizza_id, price=price, user_id=user.id, **pizza_create.dict()
        )
        pizza_database.append(new_pizza.dict())
        return new_pizza
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something went wrong",
        )


@app.put("/pizzas/{pizza_id}", status_code=status.HTTP_200_OK)
def update_status_pizza(pizza: Annotated[Pizza, Depends(get_user_pizza_by_id)]):
    index_pizza = pizza_database.index(pizza.dict())
    pizza_database[index_pizza]["status"] = PizzaStatus.DONE.value
    return {"message": f"Successfully update pizza with id {pizza.pizza_id}"}


@app.delete("/pizzas/{pizza_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_pizza(pizza: Annotated[Pizza, Depends(get_user_pizza_by_id)]):
    pizza_database.remove(pizza.dict())
    return None
