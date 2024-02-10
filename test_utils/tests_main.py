from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_success():
    test_name = "example_item"
    response = client.get(f"/api/item/{test_name}")
    assert response.status_code == 200
    assert response.json()["name"] == test_name

def test_get_item_not_found():
    test_name = "non_existing_item"
    response = client.get(f"/api/item/{test_name}")
    assert response.status_code == 404

def test_create_multiple_items_success():
    items_data = [{"name": "item1", "description": "test item 1"}, {"name": "item2", "description": "test item 2"}]
    response = client.post("/api/insert/", json=items_data)
    assert response.status_code == 201
    assert "Items added successfully" in response.json()["message"]

def test_create_multiple_items_failure():
    invalid_items_data = [{"name": "item1"}, {"name": "item2"}]
    response = client.post("/api/insert/", json=invalid_items_data)
    assert response.status_code == 400
