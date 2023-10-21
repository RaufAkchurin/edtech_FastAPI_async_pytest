import json
import uuid


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
    user_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(user_from_db) == 1
    user_from_db = dict(user_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_create_user_duplicate_email_error(client, get_user_from_database):
    user_data = {
        "name": "Nikoliai",
        "surname": "Sviridov",
        "email": "sad@dsa.com"
    }
    user_data_same_email = {
        "name": "Koshi",
        "surname": "Shvalov",
        "email": "sad@dsa.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    user_from_db = await get_user_from_database(data_from_resp["user_id"])
    user_from_db = dict(user_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True

    resp = client.post("/user/", data=json.dumps(user_data_same_email))
    assert resp.status_code == 503
    assert 'violates unique constraint "users_email_key"' in resp.json()["detail"]
