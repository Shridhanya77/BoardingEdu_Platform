"""Shortlist and enquiry API tests."""

from tests.conftest import auth_header


def _first_school_id(client):
    return client.get("/api/schools").get_json()["data"]["items"][0]["id"]


def test_shortlist_flow(client, parent_token):
    school_id = _first_school_id(client)
    headers = auth_header(parent_token)

    add = client.post("/api/shortlists", headers=headers, json={"school_id": school_id})
    assert add.status_code == 201

    dup = client.post("/api/shortlists", headers=headers, json={"school_id": school_id})
    assert dup.status_code == 409

    listing = client.get("/api/shortlists", headers=headers)
    assert listing.status_code == 200
    assert len(listing.get_json()["data"]["items"]) >= 1

    remove = client.delete(f"/api/shortlists/{school_id}", headers=headers)
    assert remove.status_code == 200


def test_shortlist_requires_auth(client):
    res = client.get("/api/shortlists")
    assert res.status_code == 401


def test_enquiry_flow(client, parent_token, admin_token):
    school_id = _first_school_id(client)
    parent_headers = auth_header(parent_token)

    create = client.post(
        "/api/enquiries",
        headers=parent_headers,
        json={
            "school_id": school_id,
            "student_name": "Aarav Test",
            "parent_name": "Test Parent",
            "class_name": "Class 5",
            "academic_year": "2026-27",
            "phone": "+91-9000000002",
            "email": "parent@test.demo",
            "message": "Demo enquiry",
        },
    )
    assert create.status_code == 201
    enquiry_id = create.get_json()["data"]["enquiry"]["id"]

    mine = client.get("/api/enquiries", headers=parent_headers)
    assert mine.status_code == 200
    assert any(e["id"] == enquiry_id for e in mine.get_json()["data"]["items"])

    admin_headers = auth_header(admin_token)
    dashboard = client.get("/api/admin/dashboard", headers=admin_headers)
    assert dashboard.status_code == 200
    assert dashboard.get_json()["data"]["stats"]["total_enquiries"] >= 1

    update = client.put(
        f"/api/admin/enquiries/{enquiry_id}/status",
        headers=admin_headers,
        json={"status": "Contacted"},
    )
    assert update.status_code == 200
    assert update.get_json()["data"]["enquiry"]["status"] == "Contacted"


def test_parent_cannot_access_admin(client, parent_token):
    res = client.get("/api/admin/dashboard", headers=auth_header(parent_token))
    assert res.status_code == 403
