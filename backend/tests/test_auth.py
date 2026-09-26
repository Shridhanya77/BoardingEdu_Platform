"""Authentication API tests."""

from tests.conftest import auth_header


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.get_json()
    assert body["success"] is True
    assert body["database"] == "connected"


def test_register_parent_success(client):
    res = client.post(
        "/api/auth/register",
        json={
            "name": "New Parent",
            "email": "newparent@test.demo",
            "phone": "+91-9000099999",
            "password": "SecurePass1",
            "role": "parent",
        },
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["success"] is True
    assert body["data"]["user"]["email"] == "newparent@test.demo"
    assert body["data"]["access_token"]


def test_register_rejects_admin_role(client):
    res = client.post(
        "/api/auth/register",
        json={
            "name": "Hacker",
            "email": "hacker@test.demo",
            "password": "SecurePass1",
            "role": "admin",
        },
    )
    assert res.status_code == 400
    assert res.get_json()["success"] is False


def test_register_duplicate_email(client):
    res = client.post(
        "/api/auth/register",
        json={
            "name": "Dup",
            "email": "parent@test.demo",
            "password": "SecurePass1",
            "role": "parent",
        },
    )
    assert res.status_code == 409


def test_login_success_and_me(client, parent_token):
    res = client.get("/api/auth/me", headers=auth_header(parent_token))
    assert res.status_code == 200
    assert res.get_json()["data"]["user"]["role"] == "parent"


def test_login_invalid_password(client):
    res = client.post(
        "/api/auth/login",
        json={"email": "parent@test.demo", "password": "wrong-password"},
    )
    assert res.status_code == 401


def test_me_requires_auth(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401
