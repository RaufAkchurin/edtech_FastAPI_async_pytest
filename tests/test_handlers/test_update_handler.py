import json
from uuid import uuid4

from db.dals import PortalRole
from tests.conftest import create_test_auth_headers_for_user


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.ru",
        "is_active": True,
        "hashed_password": "$2b$12$XrOiXxxFh7avj5.dYUEC.OLURxFojtSn05TEE5WZOYe3NjVnSI0.u",
        "roles":[PortalRole.ROLE_PORTAL_USER, ]
    }
    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "cheburek@kek.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    users_from_db = dict(users_from_db[0])
    assert users_from_db["name"] == user_data_updated["name"]
    assert users_from_db["surname"] == user_data_updated["surname"]
    assert users_from_db["email"] == user_data_updated["email"]
    assert users_from_db["is_active"] == True
    assert users_from_db["user_id"] == user_data["user_id"]
