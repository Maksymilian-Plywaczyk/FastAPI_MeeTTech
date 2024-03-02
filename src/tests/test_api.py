from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..main import app


class TestAPI:
    @staticmethod
    @pytest.fixture(scope="function")
    def client():
        return TestClient(app=app)

    def test_get_pizza_success(self, client):
        response = client.get("/pizzas/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "pizza_type": "MARGHERITA",
            "size": "S",
            "additional_info": None,
            "pizza_id": 1,
            "price": 5.99,
            "user_id": 1,
            "status": "Undone",
        }

    def test_get_pizza_not_found(self, client):
        response = client.get("/pizzas/1202333")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "That pizza is not in our database!"}

    def test_get_user_pizzas_success(self, client):
        response = client.get(
            "/pizzas/", headers={"Authorization": "Bearer user1@example.com"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) != 0

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
        assert {
            "pizza_id",
            "price",
            "user_id",
            "pizza_type",
            "size",
            "additional_info",
            "status",
        } == set(data.keys())

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
        response = client.put(
            "/pizzas/1", headers={"Authorization": "Bearer user1@example.com"}
        )
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data == {"message": "Successfully update pizza with id 1"}

    def test_update_status_pizza_failed(self, client):
        response = client.put(
            "/pizzas/1233", headers={"Authorization": "Bearer user1@example.com"}
        )
        data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "That pizza is not in our database!"}

    def test_delete_user_pizza_success(self, client):
        response = client.delete(
            "/pizzas/",
            params={"pizza_id": 1},
            headers={"Authorization": "Bearer user1@example.com"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_user_pizza_failed(self, client):
        response = client.delete(
            "/pizzas/",
            params={"pizza_id": 1231231},
            headers={"Authorization": "Bearer user1@example.com"},
        )
        data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "That pizza is not in our database!"}
