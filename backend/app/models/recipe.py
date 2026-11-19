from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Recipe(Base):
    """Model ORM tabel `recipes` sesuai skema dataset cleaned_recipes.csv dan PostgreSQL."""

    __tablename__ = "recipes"

    recipe_id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    nama_masakan: Mapped[str] = mapped_column(String(255), nullable=False)
    kategori: Mapped[str | None] = mapped_column(String(100), nullable=True)
    jumlah_porsi: Mapped[int] = mapped_column(Integer, default=1)
    basis_porsi: Mapped[str] = mapped_column(String(50), default="1 porsi")
    kalori_kkal: Mapped[float | None] = mapped_column(Float, default=0.0)
    protein_g: Mapped[float | None] = mapped_column(Float, default=0.0)
    karbohidrat_g: Mapped[float | None] = mapped_column(Float, default=0.0)
    lemak_g: Mapped[float | None] = mapped_column(Float, default=0.0)
    bahan_bahan: Mapped[str | None] = mapped_column(Text, nullable=True)
    cara_memasak: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

