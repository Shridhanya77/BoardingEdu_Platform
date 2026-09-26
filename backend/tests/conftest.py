"""Pytest fixtures for BoardingEdu API tests (in-memory SQLite)."""

import pytest

from app import create_app
from config import TestingConfig
from extensions import db
from models import Facility, School, SchoolFacility, User


@pytest.fixture()
def app():
    application = create_app(TestingConfig)
    with application.app_context():
        db.create_all()
        _seed_minimal()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def _seed_minimal():
    admin = User(name="Test Admin", email="admin@test.demo", phone="9000000001", role="admin")
    admin.set_password("AdminTest12")
    parent = User(
        name="Test Parent", email="parent@test.demo", phone="9000000002", role="parent"
    )
    parent.set_password("ParentTest12")
    db.session.add_all([admin, parent])

    library = Facility(name="Library", description="Demo library")
    pool = Facility(name="Swimming Pool", description="Demo pool")
    db.session.add_all([library, pool])
    db.session.flush()

    school = School(
        name="Test Horizon School",
        city="Mumbai",
        state="Maharashtra",
        board="CBSE",
        school_type="Day School",
        gender="Co-ed",
        min_fee=100000,
        max_fee=200000,
        hostel_available=False,
        rating=4.5,
        description="Demo school for tests.",
    )
    boarding = School(
        name="Test Boarding Academy",
        city="Pune",
        state="Maharashtra",
        board="ICSE",
        school_type="Boarding",
        gender="Co-ed",
        min_fee=300000,
        max_fee=450000,
        hostel_available=True,
        rating=4.2,
        description="Demo boarding school for tests.",
    )
    db.session.add_all([school, boarding])
    db.session.flush()
    db.session.add(SchoolFacility(school_id=school.id, facility_id=library.id))
    db.session.add(SchoolFacility(school_id=boarding.id, facility_id=pool.id))
    db.session.commit()


@pytest.fixture()
def parent_token(client):
    res = client.post(
        "/api/auth/login",
        json={"email": "parent@test.demo", "password": "ParentTest12"},
    )
    assert res.status_code == 200
    return res.get_json()["data"]["access_token"]


@pytest.fixture()
def admin_token(client):
    res = client.post(
        "/api/auth/login",
        json={"email": "admin@test.demo", "password": "AdminTest12"},
    )
    assert res.status_code == 200
    return res.get_json()["data"]["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}
