from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.api.dependencies import get_current_user, get_current_user_optional, get_db
from app.models.user import User
from app.schemas.mealplan import MealPlanResponse, UnifiedMealPlanRequest
from app.services.mealplan_service import (
    generate_meal_plan as run_generate_meal_plan,
    get_latest_meal_plan,
    get_meal_plan_by_id,
)

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
    current_user: User | None = Depends(get_current_user_optional),
) -> MealPlanResponse:
    user_id = current_user.id if current_user else None
    try:
        return await run_in_threadpool(run_generate_meal_plan, db, request, user_id)
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
    "/latest",
    response_model=MealPlanResponse,
    summary="Ambil meal plan terbaru milik user aktif",
)
async def get_latest_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MealPlanResponse:
    plan = await run_in_threadpool(get_latest_meal_plan, db, current_user.id)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Belum ada meal plan untuk akun ini.",
        )
    return plan


@router.get(
    "/{plan_id}",
    response_model=MealPlanResponse,
    summary="Ambil meal plan berdasarkan ID",
)
async def get_meal_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> MealPlanResponse:
    user_id = current_user.id if current_user else None
    plan = await run_in_threadpool(get_meal_plan_by_id, db, plan_id, user_id)
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal plan dengan id '{plan_id}' tidak ditemukan.",
        )
    return plan