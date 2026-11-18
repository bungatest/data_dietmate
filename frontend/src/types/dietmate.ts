export type Gender = "female" | "male";

export type ActivityLevel =
  | "sedentary"
  | "light"
  | "moderate"
  | "active"
  | "very_active";

export type DietGoal = "weight_loss" | "maintenance" | "muscle_gain";

export interface UserProfile {
  age: number;
  gender: Gender;
  height_cm: number;
  weight_kg: number;
  activity_level: ActivityLevel;
  pal: number;
}

export interface DietPreferences {
  goal: DietGoal;
  duration_days: number;
  allergies: string[];
  food_preferences: string[];
}

export interface GenerateMealPlanRequest {
  profile: UserProfile;
  preferences: DietPreferences;
}

export interface NutritionValues {
  calories_kcal: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
}

export interface NutritionSummary extends NutritionValues {
  bmi: number;
  bmi_category: string;
  bmr_kcal: number;
  tdee_kcal: number;
  target_calories_kcal: number;
}

export type MealType = "breakfast" | "lunch" | "dinner";

export interface Recipe {
  id: string;
  name: string;
  description: string;
  prep_time_minutes: number;
  servings: number;
  ingredients: string[];
  instructions: string[];
  tags: string[];
}

export interface PlannedMeal {
  meal_type: MealType;
  servings: number;
  recipe: Recipe;
  nutrition: NutritionValues;
}

export interface MealPlanDay {
  day_number: number;
  meals: PlannedMeal[];
  totals: NutritionValues;
}

export interface MealPlanResponse {
  plan_id: string;
  source: "mock" | "rag";
  generated_at: string;
  nutrition_summary: NutritionSummary;
  days: MealPlanDay[];
  validation: {
    passed: boolean;
    warnings: string[];
  };
}

export interface ActivityOption {
  value: ActivityLevel;
  title: string;
  description: string;
  pal: number;
}
