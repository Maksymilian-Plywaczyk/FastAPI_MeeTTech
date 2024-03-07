from fastapi.testclient import TestClient
from fastapi import status
import pytest

from ..local_database import pizza_database
from ..main import app


class TestAPI:
    @staticmethod
    @pytest.fixture(scope="class")
    def client():
        return TestClient(app=app)

    def test_get_pizza_success(self, client):
        response = client.get("/pizzas/b4871a56-0996-42bd-a79d-9018d72ba092")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "pizza_type": "MARGHERITA",
            "size": "S",
            "additional_info": None,
            "pizza_id": "b4871a56-0996-42bd-a79d-9018d72ba092",
            "price": 5.99,
            "user_id": 1,
            "status": "Undone",
        }

    def test_get_pizza_not_found(self, client):
        response = client.get("/pizzas/1202333-sdss-as2-223")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "That pizza is not in our database!"}

    def test_get_user_pizzas_success(self, client):
        response = client.get(
            "/pizzas/", headers={"Authorization": "Bearer user1@example.com"}
        )
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data[0]["user_id"] == 1

    def test_get_user_pizzas_unauthorized(self, client):
        response = client.get(
            "/pizzas/", headers={"Authorization": "Bearer example token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Invalid authentication credentials"}

    def test_create_pizza_success(self, client):
        response = client.post(
            "/pizzas/",
            json={
                "pizza_type": "MARGHERITA",
                "size": "S",
                "additional_info": None,
            },
            headers={"Authorization": "Bearer user1@example.com"},
        )
        data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert data in pizza_database

    def test_create_pizza_unauthorized(self, client):
        response = client.post(
            "/pizzas/",
            json={
                "pizza_type": "MARGHERITA",
                "size": "S",
                "additional_info": None,
            },
            headers={"Authorization": "Bearer example token"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Invalid authentication credentials"}

    def test_create_pizza_bad_request(self, client):
        response = client.post(
            "/pizzas/",
            json={
                "pizza_type": "DIAVOLA",
                "size": "S",
                "additional_info": None,
            },
            headers={"Authorization": "Bearer user1@example.com"},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_status_pizza_success(self, client):
        pizza_in_database = next(
            pizza
            for pizza in pizza_database
            if pizza["pizza_id"] == "b4871a56-0996-42bd-a79d-9018d72ba092"
        )
        assert pizza_in_database["status"] == "Undone"
        response = client.put(
            "/pizzas/b4871a56-0996-42bd-a79d-9018d72ba092",
            headers={"Authorization": "Bearer user1@example.com"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert pizza_in_database["status"] == "Done"

    def test_update_status_pizza_failed(self, client):
        response = client.put(
            "/pizzas/1233", headers={"Authorization": "Bearer user1@example.com"}
        )
        data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "That pizza is not in our database!"}

    def test_delete_user_pizza_success(self, client):
        response = client.delete(
            "/pizzas/b4871a56-0996-42bd-a79d-9018d72ba092",
            headers={"Authorization": "Bearer user1@example.com"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_user_pizza_failed(self, client):
        response = client.delete(
            "/pizzas/b4871a56-0996",
            headers={"Authorization": "Bearer user1@example.com"},
        )
        data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "That pizza is not in our database!"}
