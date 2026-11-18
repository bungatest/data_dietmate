import type { ActivityOption, DietGoal } from "@/types/dietmate";

export const ACTIVITY_OPTIONS: ActivityOption[] = [
  {
    value: "sedentary",
    title: "Mayoritas duduk",
    description: "Sedikit atau hampir tidak berolahraga",
    pal: 1.2
  },
  {
    value: "light",
    title: "Aktivitas ringan",
    description: "Olahraga ringan 1–3 hari/minggu",
    pal: 1.375
  },
  {
    value: "moderate",
    title: "Aktivitas sedang",
    description: "Olahraga 3–5 hari/minggu",
    pal: 1.55
  },
  {
    value: "active",
    title: "Aktif",
    description: "Olahraga intensif 6–7 hari/minggu",
    pal: 1.725
  },
  {
    value: "very_active",
    title: "Sangat aktif",
    description: "Aktivitas fisik berat atau latihan 2 kali/hari",
    pal: 1.9
  }
];

export const GOAL_OPTIONS: {
  value: DietGoal;
  title: string;
  description: string;
  adjustment: number;
}[] = [
  {
    value: "weight_loss",
    title: "Menurunkan berat badan",
    description: "Simulasi defisit 500 kkal dari TDEE",
    adjustment: -500
  },
  {
    value: "maintenance",
    title: "Menjaga berat badan",
    description: "Mengikuti estimasi kebutuhan energi harian",
    adjustment: 0
  },
  {
    value: "muscle_gain",
    title: "Meningkatkan massa otot",
    description: "Simulasi surplus 300 kkal dari TDEE",
    adjustment: 300
  }
];

export const ALLERGY_OPTIONS = [
  { value: "nut_free", label: "Tanpa kacang" },
  { value: "shellfish_free", label: "Tanpa kerang/udang" },
  { value: "dairy_free", label: "Tanpa susu" },
  { value: "gluten_free", label: "Bebas gluten" }
];

export const FOOD_PREFERENCE_OPTIONS = [
  { value: "vegetarian", label: "Vegetarian" },
  { value: "high_protein", label: "Tinggi protein" },
  { value: "low_spicy", label: "Tidak pedas" },
  { value: "simple_meals", label: "Menu praktis" }
];
