from sqlalchemy import create_engine
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

    Base.metadata.create_all(bind=target_engine or engine, checkfirst=True)

