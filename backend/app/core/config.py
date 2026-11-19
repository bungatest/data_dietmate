from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    """Konfigurasi aplikasi backend yang dibaca dari environment / file .env."""

    APP_NAME: str = "DietMate AI Backend"
    APP_VERSION: str = "0.1.0"

    # Database: mendukung DATABASE_URL langsung maupun komponen DB_* dari notebook
    DATABASE_URL: str | None = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "dietmate_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS (integrasi frontend Next.js)
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Standar BMI:
    # - "kemenkes" (default): klasifikasi IMT Kementerian Kesehatan RI
    # - "who": klasifikasi BMI WHO global (Underweight/Normal/Overweight/Obese)
    # Catatan: Untuk mengubah standar, cukup ubah nilai BMI_STANDARD di file .env
    # atau ubah nilai default di bawah ini.
    BMI_STANDARD: Literal["kemenkes", "who"] = "kemenkes"

    # Parameter validasi meal plan
    NUTRITION_TOLERANCE_PCT: float = 10.0
    MAX_RECIPE_REPEATS: int = 2

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def effective_database_url(self) -> str:
        """Mengembalikan URL koneksi database aktif untuk SQLAlchemy."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()

