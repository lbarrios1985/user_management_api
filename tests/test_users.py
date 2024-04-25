import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper for user payload
def user_payload(username="testuser", email="test@example.com"):
    return {
        "username": username,
        "email": email,
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "active": True
    }

def test_create_user():
    response = client.post("/users/", json=user_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["active"] is True

def test_create_duplicate_user():
    client.post("/users/", json=user_payload(username="dupuser", email="dup@example.com"))
    response = client.post("/users/", json=user_payload(username="dupuser", email="dup@example.com"))
    assert response.status_code == 400
    assert "already exists" in response.text

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_user():
    create = client.post("/users/", json=user_payload(username="readuser", email="read@example.com"))
    user_id = create.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "readuser"

def test_update_user():
    create = client.post("/users/", json=user_payload(username="updateuser", email="update@example.com"))
    user_id = create.json()["id"]
    response = client.put(f"/users/{user_id}", json={"first_name": "Updated"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"

def test_delete_user():
    create = client.post("/users/", json=user_payload(username="deluser", email="del@example.com"))
    user_id = create.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted."
    # Confirm user is gone
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404
