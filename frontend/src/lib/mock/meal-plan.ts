import { calculateNutritionPreview } from "@/lib/nutrition/preview";
import { GOAL_OPTIONS } from "@/lib/constants";
import type {
  GenerateMealPlanRequest,
  MealPlanDay,
  MealPlanResponse,
  NutritionValues,
  Recipe
} from "@/types/dietmate";

const RECIPES: Recipe[] = [
  {
    id: "demo-oat-banana",
    name: "Overnight Oat Pisang",
    description: "Oat, pisang, dan yogurt untuk sarapan praktis.",
    prep_time_minutes: 10,
    servings: 1,
    ingredients: ["50 g rolled oat", "1 buah pisang", "100 g yogurt plain", "1 sdt chia seed"],
    instructions: [
      "Campurkan oat, yogurt, dan chia seed dalam wadah.",
      "Simpan di kulkas minimal 2 jam atau semalaman.",
      "Tambahkan irisan pisang sebelum disajikan."
    ],
    tags: ["Sarapan", "Praktis"]
  },
  {
    id: "demo-chicken-rice",
    name: "Nasi Ayam Panggang",
    description: "Ayam panggang dengan nasi dan sayuran.",
    prep_time_minutes: 30,
    servings: 1,
    ingredients: ["100 g dada ayam", "150 g nasi matang", "100 g brokoli", "Bawang putih dan lada secukupnya"],
    instructions: [
      "Bumbui ayam dengan bawang putih dan lada.",
      "Panggang ayam hingga matang sempurna.",
      "Sajikan bersama nasi dan brokoli kukus."
    ],
    tags: ["Makan siang", "Tinggi protein"]
  },
  {
    id: "demo-tofu-soup",
    name: "Sup Tahu Sayuran",
    description: "Sup hangat dengan tahu, wortel, dan sawi.",
    prep_time_minutes: 25,
    servings: 1,
    ingredients: ["100 g tahu", "1 buah wortel", "50 g sawi", "300 ml kaldu sayur"],
    instructions: [
      "Didihkan kaldu sayur.",
      "Masukkan wortel hingga mulai empuk.",
      "Tambahkan tahu dan sawi, masak hingga matang."
    ],
    tags: ["Makan malam", "Sayuran"]
  },
  {
    id: "demo-egg-toast",
    name: "Roti Telur Alpukat",
    description: "Roti gandum dengan telur dan alpukat.",
    prep_time_minutes: 15,
    servings: 1,
    ingredients: ["2 lembar roti gandum", "1 butir telur", "¼ buah alpukat"],
    instructions: [
      "Panggang roti hingga kecokelatan.",
      "Masak telur sesuai tingkat kematangan yang diinginkan.",
      "Tambahkan alpukat dan telur di atas roti."
    ],
    tags: ["Sarapan", "Praktis"]
  },
  {
    id: "demo-tempe-bowl",
    name: "Bowl Tempe dan Sayur",
    description: "Tempe panggang dengan nasi dan sayuran segar.",
    prep_time_minutes: 25,
    servings: 1,
    ingredients: ["100 g tempe", "120 g nasi matang", "100 g sayuran campur", "1 sdt minyak"],
    instructions: [
      "Potong tempe dan bumbui secukupnya.",
      "Panggang tempe dengan sedikit minyak.",
      "Susun nasi, sayuran, dan tempe dalam mangkuk."
    ],
    tags: ["Makan siang", "Plant-based"]
  },
  {
    id: "demo-fish-vegetables",
    name: "Ikan Kukus Sayuran",
    description: "Ikan kukus dengan sayuran dan kentang.",
    prep_time_minutes: 30,
    servings: 1,
    ingredients: ["120 g ikan fillet", "100 g kentang", "100 g buncis", "Jeruk nipis dan rempah"],
    instructions: [
      "Lumuri ikan dengan jeruk nipis dan rempah.",
      "Kukus ikan hingga matang.",
      "Sajikan dengan kentang rebus dan buncis."
    ],
    tags: ["Makan malam", "Protein"]
  }
];

const BASE_NUTRITION: Record<string, NutritionValues> = {
  "demo-oat-banana": { calories_kcal: 320, protein_g: 15, carbs_g: 52, fat_g: 7 },
  "demo-chicken-rice": { calories_kcal: 485, protein_g: 38, carbs_g: 58, fat_g: 10 },
  "demo-tofu-soup": { calories_kcal: 285, protein_g: 19, carbs_g: 22, fat_g: 12 },
  "demo-egg-toast": { calories_kcal: 310, protein_g: 17, carbs_g: 34, fat_g: 11 },
  "demo-tempe-bowl": { calories_kcal: 440, protein_g: 23, carbs_g: 54, fat_g: 14 },
  "demo-fish-vegetables": { calories_kcal: 365, protein_g: 32, carbs_g: 34, fat_g: 10 }
};

function sumNutrition(items: NutritionValues[]): NutritionValues {
  return items.reduce(
    (total, item) => ({
      calories_kcal: total.calories_kcal + item.calories_kcal,
      protein_g: total.protein_g + item.protein_g,
      carbs_g: total.carbs_g + item.carbs_g,
      fat_g: total.fat_g + item.fat_g
    }),
    { calories_kcal: 0, protein_g: 0, carbs_g: 0, fat_g: 0 }
  );
}

export async function createMockMealPlan(
  request: GenerateMealPlanRequest
): Promise<MealPlanResponse> {
  await new Promise((resolve) => setTimeout(resolve, 1100));

  const preview = calculateNutritionPreview(request.profile);
  const goal = GOAL_OPTIONS.find(
    (option) => option.value === request.preferences.goal
  );
  const targetCalories = Math.max(0, preview.tdee + (goal?.adjustment ?? 0));
  const macroTargets = {
    carbs_g: Math.round((targetCalories * 0.55) / 4),
    protein_g: Math.round((targetCalories * 0.15) / 4),
    fat_g: Math.round((targetCalories * 0.3) / 9)
  };

  const mealOrder = [
    ["demo-oat-banana", "demo-chicken-rice", "demo-tofu-soup"],
    ["demo-egg-toast", "demo-tempe-bowl", "demo-fish-vegetables"],
    ["demo-oat-banana", "demo-tempe-bowl", "demo-tofu-soup"]
  ];

  const days: MealPlanDay[] = Array.from(
    { length: request.preferences.duration_days },
    (_, dayIndex) => {
      const ids = mealOrder[dayIndex % mealOrder.length];
      const meals = ids.map((id, mealIndex) => {
        const recipe = RECIPES.find((item) => item.id === id)!;
        return {
          meal_type: (["breakfast", "lunch", "dinner"] as const)[mealIndex],
          servings: 1,
          recipe,
          nutrition: BASE_NUTRITION[id]
        };
      });

      return {
        day_number: dayIndex + 1,
        meals,
        totals: sumNutrition(meals.map((meal) => meal.nutrition))
      };
    }
  );

  return {
    plan_id: `demo-${Date.now()}`,
    source: "mock",
    generated_at: new Date().toISOString(),
    nutrition_summary: {
      bmi: preview.bmi,
      bmi_category: preview.bmiCategory,
      bmr_kcal: preview.bmr,
      tdee_kcal: preview.tdee,
      target_calories_kcal: Math.round(targetCalories),
      calories_kcal: Math.round(targetCalories),
      protein_g: macroTargets.protein_g,
      carbs_g: macroTargets.carbs_g,
      fat_g: macroTargets.fat_g
    },
    days,
    validation: {
      passed: false,
      warnings: [
        "Ini adalah data demo untuk menguji antarmuka, bukan hasil retrieval RAG.",
        "Nilai nutrisi contoh belum divalidasi terhadap dataset resep DietMate."
      ]
    }
  };
}
