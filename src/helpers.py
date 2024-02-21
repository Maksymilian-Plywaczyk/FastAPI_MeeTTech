from .schemas import Pizza
from .local_database import pizza_database


def get_pizza_by_id(pizza_id: int) -> Pizza | None:
    pizza = next(
        filter(lambda pizza: pizza["pizza_id"] == pizza_id, pizza_database), None
    )
    if not pizza:
        raise TypeError
    return pizza


def get_user_pizza_by_id(pizza_id: int, user_id: int) -> Pizza | None:
    pizza = next(
        filter(
            lambda pizza: pizza["pizza_id"] == pizza_id and pizza["user_id"] == user_id,
            pizza_database,
        ),
        None,
    )
    if not pizza:
        raise TypeError
    return pizza
