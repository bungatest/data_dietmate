from collections.abc import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.db.database import Base
from app.main import app
from app.models.recipe import Recipe


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Membuat database SQLite in-memory terisolasi beserta sample resep untuk testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    sample_recipes = [
        Recipe(
            recipe_id="RCP_0001",
            nama_masakan="Toge Telur",
            kategori="Makanan Pembuka",
            jumlah_porsi=1,
            basis_porsi="1 porsi",
            kalori_kkal=252.0,
            protein_g=21.9,
            karbohidrat_g=26.73,
            lemak_g=6.84,
            bahan_bahan="- 1 besar egg - 150 gram sprouts - 50 g bakso daging sapi",
        ),
        Recipe(
            recipe_id="RCP_0002",
            nama_masakan="Tumis Labu Siam",
            kategori="Makanan Pembuka",
            jumlah_porsi=5,
            basis_porsi="1 porsi",
            kalori_kkal=600.0,
            protein_g=25.0,
            karbohidrat_g=80.0,
            lemak_g=20.0,
            bahan_bahan="- 329 gram labu siam - 27 gram bawang merah - 5 gram bawang putih",
        ),
        Recipe(
            recipe_id="RCP_0003",
            nama_masakan="Dimsum Ayam Udang",
            kategori="Makanan Pembuka",
            jumlah_porsi=27,
            basis_porsi="1 porsi",
            kalori_kkal=500.0,
            protein_g=35.0,
            karbohidrat_g=50.0,
            lemak_g=16.0,
            bahan_bahan="- 100 gram udang - 200 gram paha ayam - 68 gram telur",
        ),
        Recipe(
            recipe_id="RCP_0073",
            nama_masakan="Ayam Teriyaki",
            kategori="Hidangan Utama",
            jumlah_porsi=2,
            basis_porsi="1 porsi",
            kalori_kkal=700.0,
            protein_g=40.0,
            karbohidrat_g=85.0,
            lemak_g=22.0,
            bahan_bahan="- 250 gram dada ayam - 2 sdm saus teriyaki - 1 siung bawang putih",
        ),
        Recipe(
            recipe_id="RCP_0100",
            nama_masakan="Nasi Ayam Panggang Sayur",
            kategori="Hidangan Utama",
            jumlah_porsi=1,
            basis_porsi="1 porsi",
            kalori_kkal=700.0,
            protein_g=35.0,
            karbohidrat_g=85.0,
            lemak_g=24.0,
            bahan_bahan="- 150 gram nasi putih - 150 gram dada ayam - 100 gram brokoli",
        ),
    ]
    session.add_all(sample_recipes)
    session.commit()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    """Menyediakan FastAPI TestClient yang memakai session database SQLite pengujian."""
    monkeypatch.setattr("app.main.init_db", lambda: None)

    def _override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

