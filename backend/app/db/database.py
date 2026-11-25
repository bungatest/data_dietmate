from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Base class untuk seluruh model ORM SQLAlchemy."""


def _build_engine():
    database_url = settings.effective_database_url
    is_sqlite = database_url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {"connect_timeout": 3}
    return create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=not is_sqlite,
    )


engine = _build_engine()


def init_db(target_engine=None) -> None:
    """Membuat tabel yang belum ada di database (mis. meal_plans) tanpa menimpa data lama."""
    import app.models  # noqa: F401 - pastikan seluruh model terdaftar di Base.metadata

    bind = target_engine or engine
    Base.metadata.create_all(bind=bind, checkfirst=True)
    _add_missing_columns(bind)


# Kolom yang ditambahkan setelah tabel pertama kali dibuat. create_all() tidak mengubah
# tabel yang sudah ada, jadi kolom baru ditambahkan manual (migrasi ringan tanpa Alembic).
_ADDED_COLUMNS: dict[str, dict[str, str]] = {
    "meal_plans": {
        "user_id": "VARCHAR(50)",
        "source": "VARCHAR(20) NOT NULL DEFAULT 'stub'",
    },
}


def _add_missing_columns(bind) -> None:
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())
    with bind.begin() as conn:
        for table, columns in _ADDED_COLUMNS.items():
            if table not in existing_tables:
                continue
            present = {col["name"] for col in inspector.get_columns(table)}
            for name, ddl in columns.items():
                if name not in present:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))

