from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.nutrition import MealType, NutritionResult
from app.schemas.user import HeightCm, UserProfile, WeightKg

class FrontendUserProfile(BaseModel):
    age: int = Field(..., ge=18, le=100)
    gender: Literal["male", "female"]
    height_cm: HeightCm
    weight_kg: WeightKg
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"]
    pal: float = Field(default=1.55)


class FrontendPreferences(BaseModel):
    goal: Literal["weight_loss", "maintenance", "muscle_gain", "lose_weight", "maintain", "gain_muscle"] = "maintenance"
    duration_days: int = Field(default=7, ge=1, le=30)
    allergies: list[str] = Field(default_factory=list)
    food_preferences: list[str] = Field(default_factory=list)


class UnifiedMealPlanRequest(BaseModel):
    """Menerima request dari Frontend dan format legacy dari unit test"""
    profile: FrontendUserProfile | None = None
    preferences: FrontendPreferences | None = None

    user_profile: UserProfile | None = None
    duration_days: int = Field(default=7, ge=1, le=30)

    model_config = ConfigDict(extra="ignore")

MealPlanRequest = UnifiedMealPlanRequest

class RecipeDetail(BaseModel):
    id: str
    name: str
    description: str = ""
    prep_time_minutes: int = 20
    servings: int = 1
    ingredients: list[str] = Field(default_factory=list)
    instructions: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class NutritionValues(BaseModel):
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float


class NutritionSummary(NutritionValues):
    bmi: float
    bmi_category: str
    bmr_kcal: float
    tdee_kcal: float
    target_calories_kcal: float


class PlannedMeal(BaseModel):
    meal_type: MealType
    servings: float
    recipe: RecipeDetail
    nutrition: NutritionValues


class MealPlanDay(BaseModel):
    day_number: int
    meals: list[PlannedMeal]
    totals: NutritionValues


class ValidationSummary(BaseModel):
    passed: bool
    warnings: list[str] = Field(default_factory=list)


class MealItem(BaseModel):
    """Kompatibilitas legacy untuk test lama."""
    recipe_id: str
    recipe_name: str
    servings: float
    meal_type: MealType


class DayPlan(BaseModel):
    """Kompatibilitas legacy untuk test lama."""
    day: int
    meals: list[MealItem]
    total_calories: float
    total_carbs_g: float
    total_protein_g: float
    total_fat_g: float


class MealPlanResponse(BaseModel):
    """Response terpadu yang memenuhi kebutuhan rendering Frontend dan unit test backend lama"""
    plan_id: str
    source: str = "stub"
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    nutrition_summary: NutritionSummary
    days: list[MealPlanDay]
    validation: ValidationSummary

    # Field kompatibilitas untuk unit test backend lama
    user_target: NutritionResult | None = None
    validation_status: str = "valid"
    warnings: list[str] = Field(default_factory=list)