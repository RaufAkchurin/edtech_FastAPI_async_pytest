from uuid import uuid4

from db.dals import PortalRole
from tests.conftest import create_test_auth_headers_for_user


async def test_get_user(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.ru",
        "is_active": True,
        "hashed_password": "hash",
        "roles": [PortalRole.ROLE_PORTAL_USER, ]
    }
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}",
                      headers=create_test_auth_headers_for_user(user_data["email"]))
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] == True
