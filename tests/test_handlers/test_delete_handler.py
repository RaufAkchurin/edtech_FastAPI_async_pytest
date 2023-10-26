import uuid
from uuid import uuid4

from db.models import PortalRole
from tests.conftest import create_test_auth_headers_for_user


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.ru",
        "is_active": True,
        "hashed_password": "hash",
        "roles": ["ROLE_PORTAL_USER"],
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}",
                         headers=create_test_auth_headers_for_user(user_data["email"]))
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    user_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(user_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_not_found(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.ru",
        "is_active": True,
        "hashed_password": "hash",
        "roles": ["ROLE_PORTAL_USER"],
    }
    await create_user_in_database(**user_data)

    user_id = uuid.uuid4()
    resp = client.delete(f"/user/?user_id={user_id}",
                         headers=create_test_auth_headers_for_user(user_data["email"]))
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id} not found."}


async def test_delete_user_unauth(client, create_user_in_database):
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
    resp = client.delete(f"/user/?user_id={user_data['user_id']}",
                         headers=create_test_auth_headers_for_user(user_data["email"] + "a"))
    assert resp.status_code == 401
    assert resp.text == '{"detail":"Could not validate credentials"}'


async def test_reject_delete_superadmin(
        client,
        create_user_in_database,
        get_user_from_database,
):
    user_for_deletion = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "faefwq",
        "roles": [PortalRole.ROLE_PORTAL_SUPERADMIN]
    }

    await create_user_in_database(**user_for_deletion)
    resp = client.delete(
        f"/user/?user_id={user_for_deletion['user_id']}",
        headers=create_test_auth_headers_for_user(user_for_deletion["email"])
    )
    assert resp.status_code == 406
    assert resp.json() == {"detail": "Superadmin cannot be deleted via API"}
    user_from_database = await get_user_from_database(user_for_deletion["user_id"])
    assert PortalRole.ROLE_PORTAL_SUPERADMIN in dict(user_from_database[0])["roles"]

