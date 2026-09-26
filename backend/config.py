"""
Application configuration.

Values are loaded from environment variables. Never hardcode secrets here.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _normalize_database_url(url: str) -> str:
    """
    Normalize hosted/local database URLs for SQLAlchemy.

    - Render often provides postgres:// → postgresql://
    - SQLAlchemy 2.1+ maps bare postgresql:// to psycopg (v3); we pin
      postgresql+psycopg2:// to match requirements.txt.
    - SQLite URLs stored as relative paths (for example sqlite:///boardingedu.db)
      are resolved against the backend directory so they work from any launch path.
    """
    if not url:
        return url

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    if url.startswith("sqlite:///"):
        relative_path = url.replace("sqlite:///", "", 1)
        if relative_path and not os.path.isabs(relative_path):
            relative_path = str((BASE_DIR / relative_path).resolve())
            url = f"sqlite:///{relative_path}"

    return url


class Config:
    """Base configuration for BoardingEdu Flask API."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-jwt-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "24"))
    )

    SQLITE_DB_PATH = (BASE_DIR / "boardingedu.db").resolve().as_posix()
    # Prefer PostgreSQL for the product stack; override via DATABASE_URL in .env.
    # (pytest still uses TestingConfig → in-memory SQLite.)
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(
        os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres123@localhost:5432/boardingedu",
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:4173,http://127.0.0.1:4173,http://localhost:4175,http://127.0.0.1:4175,http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]

    # Seed-only credentials (never commit a real .env)
    DEMO_ADMIN_EMAIL = os.getenv("DEMO_ADMIN_EMAIL", "admin@boardingedu.demo")
    DEMO_ADMIN_PASSWORD = os.getenv("DEMO_ADMIN_PASSWORD", "AdminDemo@123")
    DEMO_PARENT_EMAIL = os.getenv("DEMO_PARENT_EMAIL", "parent@boardingedu.demo")
    DEMO_PARENT_PASSWORD = os.getenv("DEMO_PARENT_PASSWORD", "ParentDemo@123")


class TestingConfig(Config):
    """Isolated config for pytest (in-memory SQLite)."""

    TESTING = True
    SECRET_KEY = "test-secret-key-at-least-32-bytes-long!!"
    JWT_SECRET_KEY = "test-jwt-secret-key-at-least-32-bytes!!"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    CORS_ORIGINS = ["http://localhost:5173"]
