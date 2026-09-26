"""
Create the boardingedu PostgreSQL database if missing, then verify connectivity.

Usage (from backend/ with venv active):
  python setup_postgres.py

Requires DATABASE_URL in .env with your real postgres password, e.g.:
  DATABASE_URL=postgresql://postgres:YOUR_REAL_PASSWORD@localhost:5432/boardingedu
"""

from urllib.parse import urlparse, urlunparse

from dotenv import load_dotenv
import os
from pathlib import Path

from sqlalchemy import create_engine, text

load_dotenv(Path(__file__).resolve().parent / ".env")


def _normalize(url: str) -> str:
    if not url:
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


def main():
    raw = os.getenv("DATABASE_URL", "").strip()
    if not raw:
        print("ERROR: DATABASE_URL is not set in backend/.env")
        return 1
    if "YOUR_PASSWORD" in raw:
        print("ERROR: Replace YOUR_PASSWORD in backend/.env with your real PostgreSQL password.")
        print("Example:")
        print("  DATABASE_URL=postgresql://postgres:MySecretPass@localhost:5432/boardingedu")
        return 1
    if raw.startswith("sqlite"):
        print("ERROR: DATABASE_URL is still SQLite. Set a PostgreSQL URL instead.")
        return 1

    url = _normalize(raw)
    parsed = urlparse(url.replace("postgresql+psycopg2://", "postgresql://", 1))
    db_name = (parsed.path or "").lstrip("/") or "boardingedu"

    # Connect to default 'postgres' maintenance DB to create target DB if needed
    admin_parsed = parsed._replace(path="/postgres")
    admin_url = urlunparse(admin_parsed).replace(
        "postgresql://", "postgresql+psycopg2://", 1
    )

    print(f"Connecting as user '{parsed.username}' to localhost...")
    try:
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": db_name},
            ).scalar()
            if exists:
                print(f"Database '{db_name}' already exists.")
            else:
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"Created database '{db_name}'.")
    except Exception as exc:
        print(f"ERROR connecting to PostgreSQL: {exc.__class__.__name__}: {exc}")
        print("Check that PostgreSQL is running and DATABASE_URL password is correct.")
        return 1

    try:
        app_engine = create_engine(url)
        with app_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"SUCCESS: Connected to PostgreSQL database '{db_name}'.")
        print("Next: python seed.py")
        print("Then:  python app.py")
        print("Check: http://localhost:5000/api/health  -> database should be 'connected'")
        return 0
    except Exception as exc:
        print(f"ERROR opening '{db_name}': {exc.__class__.__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
