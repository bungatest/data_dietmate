from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UserProfileRecord(Base):
    """Tabel `user_profiles`: profil antropometri + preferensi diet terkini milik satu user.

    Satu baris per user. Riwayat profil pada saat meal plan dibuat tetap tersimpan
    sebagai snapshot di `meal_plans.user_profile`.
    """

    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    # Profil (halaman /profil)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    activity_level: Mapped[str] = mapped_column(String(20), nullable=False)
    pal: Mapped[float] = mapped_column(Float, nullable=False)

    # Preferensi (halaman /preferensi); NULL sampai user mengisi halaman preferensi
    goal: Mapped[str | None] = mapped_column(String(20), nullable=True)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allergies: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    food_preferences: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
