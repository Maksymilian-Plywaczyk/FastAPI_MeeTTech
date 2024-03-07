from .schemas import Pizza, User
from .local_database import pizza_database
from .auth import get_user
from fastapi import Depends, HTTPException, status
from typing import Annotated


def get_pizza_by_id(pizza_id: str) -> Pizza:
    pizza = next(
        filter(lambda pizza: pizza["pizza_id"] == pizza_id, pizza_database), None
    )
    if not pizza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="That pizza is not in our database!",
        )
    return pizza


def get_user_pizza_by_id(
    pizza_id: str, user: Annotated[User, Depends(get_user)]
) -> Pizza:
    try:
        pizza = next(
            filter(
                lambda pizza: pizza["pizza_id"] == pizza_id
                and pizza["user_id"] == user.id,
                pizza_database,
            ),
            None,
        )
        return Pizza(**pizza)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="That pizza is not in our database!",
        )
