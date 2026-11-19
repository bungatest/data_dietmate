from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check server",
    response_model=dict[str, str],
)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

