from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.nutrition import NutritionResult
from app.schemas.user import UserProfile


class MealPlanRequest(BaseModel):
    """Request payload untuk memulai pembuatan meal plan."""

    user_profile: UserProfile
    duration_days: int = Field(default=7, ge=1, le=30, description="Durasi rencana makan (1–30 hari)")
    meals_per_day: int = Field(default=3, ge=1, le=5, description="Jumlah waktu makan per hari (1–5)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_profile": {
                    "age": 25,
                    "gender": "male",
                    "weight_kg": 70.0,
                    "height_cm": 175.0,
                    "activity_level": "moderate",
                    "diet_goal": "maintain",
                    "allergies": ["udang"],
                    "preferences": ["ayam"],
                },
                "duration_days": 7,
                "meals_per_day": 3,
            }
        }
    )


class MealItem(BaseModel):
    """Satu item hidangan dalam jadwal makan harian."""

    recipe_id: str
    recipe_name: str
    servings: float = Field(..., gt=0, le=10)
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"]


class DayPlan(BaseModel):
    """Rencana menu harian beserta total nutrisi tervalidasi dari database."""

    day: int
    meals: list[MealItem]
    total_calories: float
    total_carbs_g: float
    total_protein_g: float
    total_fat_g: float


class MealPlanResponse(BaseModel):
    """Response hasil generate atau pengambilan meal plan."""

    plan_id: str
    user_target: NutritionResult
    days: list[DayPlan]
    validation_status: Literal["valid", "adjusted", "failed"]
    warnings: list[str] = Field(default_factory=list)

