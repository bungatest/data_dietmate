import type { UserProfile } from "@/types/dietmate";

export interface NutritionPreview {
  bmi: number;
  bmiCategory: string;
  bmr: number;
  tdee: number;
}

/**
 * Kalkulasi ini hanya untuk preview interaksi UI.
 * Backend FastAPI tetap menjadi sumber nilai final saat generate meal plan.
 * Rumus BMR mengikuti Mifflin-St Jeor dan faktor PAL pada proposal DietMate.
 */
export function calculateNutritionPreview(
  profile: UserProfile
): NutritionPreview {
  const heightInMeters = profile.height_cm / 100;
  const bmi = profile.weight_kg / (heightInMeters * heightInMeters);

  const bmr =
    10 * profile.weight_kg +
    6.25 * profile.height_cm -
    5 * profile.age +
    (profile.gender === "male" ? 5 : -161);

  const tdee = bmr * profile.pal;

  let bmiCategory = "Normal";
  if (bmi < 18.5) bmiCategory = "Berat badan kurang";
  else if (bmi < 25) bmiCategory = "Normal";
  else if (bmi < 30) bmiCategory = "Berat badan berlebih";
  else bmiCategory = "Obesitas";

  return {
    bmi: Number(bmi.toFixed(1)),
    bmiCategory,
    bmr: Math.round(bmr),
    tdee: Math.round(tdee)
  };
}
