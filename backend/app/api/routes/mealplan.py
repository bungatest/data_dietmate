from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.api.dependencies import get_db
from app.schemas.mealplan import MealPlanResponse, UnifiedMealPlanRequest
from app.services.mealplan_service import generate_meal_plan_stub, get_meal_plan_by_id

router = APIRouter(tags=["Meal Plan"])


@router.post(
    "/generate",
    response_model=MealPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate meal plan personal",
)
async def generate_meal_plan(
    request: UnifiedMealPlanRequest,
    db: Session = Depends(get_db),
) -> MealPlanResponse:
    try:
        return await run_in_threadpool(generate_meal_plan_stub, db, request)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get(
    "/{plan_id}",
    response_model=MealPlanResponse,
    summary="Ambil meal plan berdasarkan ID",
)
async def get_meal_plan(
    plan_id: str,
    db: Session = Depends(get_db),
) -> MealPlanResponse:
    plan = await run_in_threadpool(get_meal_plan_by_id, db, plan_id)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal plan dengan id '{plan_id}' tidak ditemukan.",
        )
    return plan