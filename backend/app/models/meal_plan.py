from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MealPlan(Base):
    """Model ORM tabel `meal_plans` untuk menyimpan riwayat dan hasil rekomendasi meal plan."""

    __tablename__ = "meal_plans"

    plan_id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    user_profile: Mapped[dict] = mapped_column(JSON, nullable=False)
    user_target: Mapped[dict] = mapped_column(JSON, nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    meals_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    days: Mapped[list] = mapped_column(JSON, nullable=False)
    validation_status: Mapped[str] = mapped_column(String(20), nullable=False)
    warnings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

