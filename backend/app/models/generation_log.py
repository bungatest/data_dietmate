from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class GenerationLog(Base):
    """Tabel `generation_logs`: jejak setiap proses generate meal plan.

    Dipakai untuk evaluasi pipeline RAG (PRD Phase 4): apa yang di-retrieve, prompt yang
    dikirim, output mentah LLM, berapa kali retry, hasil validasi, dan waktu proses.
    Kolom RAG/LLM bernilai NULL untuk generator `stub`.
    """

    __tablename__ = "generation_logs"

    log_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    # Tanpa foreign key: log tetap disimpan walaupun user/plan dihapus atau generate gagal.
    user_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    plan_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    source: Mapped[str] = mapped_column(String(20), nullable=False)  # "stub" | "rag"
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "success" | "fallback" | "failed"
    request_payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Retrieval (ChromaDB)
    retrieval_query: Mapped[str | None] = mapped_column(Text, nullable=True)
    retrieved_recipes: Mapped[list | None] = mapped_column(JSON, nullable=True)  # [{recipe_id, score}]

    # Generasi (LLM)
    llm_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    llm_raw_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Hasil
    selected_recipe_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    validation_passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    validation_warnings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
