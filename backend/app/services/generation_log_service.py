from dataclasses import dataclass, field
import logging
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.generation_log import GenerationLog

logger = logging.getLogger(__name__)


@dataclass
class GenerationTrace:
    """Informasi yang dikumpulkan selama satu proses generate, diisi bertahap oleh generator.

    Generator stub hanya mengisi `selected_recipe_ids`; generator RAG nantinya mengisi
    juga retrieval_query, retrieved_recipes, llm_model, prompt, llm_raw_output, dan attempts.
    """

    source: str = "stub"
    retrieval_query: str | None = None
    retrieved_recipes: list[dict] | None = None
    llm_model: str | None = None
    prompt: str | None = None
    llm_raw_output: str | None = None
    attempts: int = 1
    selected_recipe_ids: list[str] = field(default_factory=list)


def record_generation(
    db: Session,
    *,
    trace: GenerationTrace,
    status: str,
    request_payload: dict,
    latency_ms: int,
    user_id: str | None = None,
    plan_id: str | None = None,
    validation_passed: bool | None = None,
    validation_warnings: list[str] | None = None,
    error_message: str | None = None,
) -> GenerationLog | None:
    """Menyimpan satu baris generation_logs. Kegagalan logging tidak boleh menggagalkan request."""
    log = GenerationLog(
        log_id=f"GL_{uuid4().hex[:12]}",
        user_id=user_id,
        plan_id=plan_id,
        source=trace.source,
        status=status,
        request_payload=request_payload,
        retrieval_query=trace.retrieval_query,
        retrieved_recipes=trace.retrieved_recipes,
        llm_model=trace.llm_model,
        prompt=trace.prompt,
        llm_raw_output=trace.llm_raw_output,
        attempts=trace.attempts,
        selected_recipe_ids=list(trace.selected_recipe_ids),
        validation_passed=validation_passed,
        validation_warnings=list(validation_warnings or []),
        error_message=error_message,
        latency_ms=latency_ms,
    )
    try:
        db.add(log)
        db.commit()
        return log
    except SQLAlchemyError as exc:
        db.rollback()
        logger.warning("Gagal menyimpan generation log: %s", exc)
        return None
