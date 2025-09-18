import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

recipe_data = {
              "dish_name": "Блинчики",
              "cooking_time": 35,
              "ingredients": "Мука блинная - 3 стакана, вода - 1 стакан.",
              "text_description": "Все смешать сахар и соль по вкусу."
              }


def test_create_recipe():
    response = client.post("/descriptions_recipe/", json=recipe_data)
    assert response.status_code == 200
    id = response.json()["id"]
    assert response.json() == {"id": id,
                              "dish_name": "Блинчики",
                              "cooking_time": 35,
                              "ingredients": "Мука блинная - 3 стакана, вода - 1 стакан.",
                              "text_description": "Все смешать сахар и соль по вкусу."
                              }

def test_get_id_recipe():
    response = client.get("/descriptions_recipe/2")
    assert response.status_code == 200
    assert response.json() == {"id": 2,
                              "dish_name": "Блинчики",
                              "cooking_time": 35,
                              "ingredients": "Мука блинная - 3 стакана, вода - 1 стакан.",
                              "text_description": "Все смешать сахар и соль по вкусу."
                              }

def test_get_user_not_found():
    response = client.get("/descriptions_recipe/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}

# Тесты запускаем из /hw_1$ pytest -v