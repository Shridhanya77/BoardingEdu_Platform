"""School list/detail/filter and admin CRUD tests."""

from tests.conftest import auth_header


def test_list_schools(client):
    res = client.get("/api/schools")
    assert res.status_code == 200
    body = res.get_json()
    assert body["success"] is True
    assert body["data"]["pagination"]["total"] >= 2
    assert len(body["data"]["items"]) >= 2


def test_filter_schools_by_city(client):
    res = client.get("/api/schools?city=Mumbai")
    assert res.status_code == 200
    items = res.get_json()["data"]["items"]
    assert items
    assert all("Mumbai" in (s["city"] or "") for s in items)


def test_filter_boarding(client):
    res = client.get("/api/schools?hostel_available=true")
    assert res.status_code == 200
    items = res.get_json()["data"]["items"]
    assert items
    assert all(s["hostel_available"] is True for s in items)


def test_sort_fee_asc(client):
    res = client.get("/api/schools?sort=fee_asc")
    assert res.status_code == 200
    items = res.get_json()["data"]["items"]
    fees = [s["min_fee"] for s in items if s["min_fee"] is not None]
    assert fees == sorted(fees)


def test_school_detail(client):
    listing = client.get("/api/schools").get_json()["data"]["items"]
    school_id = listing[0]["id"]
    res = client.get(f"/api/schools/{school_id}")
    assert res.status_code == 200
    school = res.get_json()["data"]["school"]
    assert school["id"] == school_id
    assert "fees" in school


def test_school_not_found(client):
    res = client.get("/api/schools/999999")
    assert res.status_code == 404


def test_create_school_requires_admin(client, parent_token):
    res = client.post(
        "/api/schools",
        headers=auth_header(parent_token),
        json={"name": "Blocked School", "city": "Delhi"},
    )
    assert res.status_code == 403


def test_admin_create_school(client, admin_token):
    res = client.post(
        "/api/schools",
        headers=auth_header(admin_token),
        json={
            "name": "Admin Created School",
            "city": "Chennai",
            "board": "CBSE",
            "school_type": "Day School",
            "gender": "Co-ed",
            "min_fee": 50000,
            "max_fee": 90000,
            "hostel_available": False,
        },
    )
    assert res.status_code == 201
    assert res.get_json()["data"]["school"]["name"] == "Admin Created School"


def test_filter_options(client):
    res = client.get("/api/schools/filters")
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert "cities" in data
    assert "facilities" in data
