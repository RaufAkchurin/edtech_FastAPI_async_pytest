import json
import pytest


async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "Nikoliai",
        "surname": "Sviridov",
        "email": "sad@dsa.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
