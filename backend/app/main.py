from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import health, mealplan, nutrition
from app.core.config import settings
from app.db.database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Inisialisasi tabel yang belum ada (seperti meal_plans) saat aplikasi dijalankan."""
    try:
        init_db()
    except SQLAlchemyError as exc:
        logger.warning("Gagal menginisialisasi tabel database saat startup: %s", exc)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Backend FastAPI DietMate AI untuk perhitungan kebutuhan nutrisi, "
        "validasi resep & alergi, serta orkestrasi rekomendasi meal plan."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(nutrition.router)
app.include_router(mealplan.router)

