import type {
  DietPreferences,
  MealPlanResponse,
  UserProfile
} from "@/types/dietmate";
import type { DietMateUser } from "@/types/auth";

const KEYS = {
  currentUser: "dietmate:v1:current-user",
  mockAccount: "dietmate:v1:mock-account",
  profile: "dietmate:v1:profile",
  preferences: "dietmate:v1:preferences",
  mealPlan: "dietmate:v1:meal-plan"
} as const;

function readValue<T>(key: string): T | null {
  if (typeof window === "undefined") return null;

  try {
    const raw = window.sessionStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

function writeValue<T>(key: string, value: T): void {
  if (typeof window === "undefined") return;

  try {
    window.sessionStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Storage mungkin tidak tersedia pada mode private tertentu.
  }
}

export const getCurrentUser = () => readValue<DietMateUser>(KEYS.currentUser);
export const saveCurrentUser = (value: DietMateUser) =>
  writeValue(KEYS.currentUser, value);
export const getMockAccount = () => readValue<DietMateUser>(KEYS.mockAccount);
export const saveMockAccount = (value: DietMateUser) =>
  writeValue(KEYS.mockAccount, value);

export const getProfile = () => readValue<UserProfile>(KEYS.profile);
export const saveProfile = (value: UserProfile) =>
  writeValue(KEYS.profile, value);

export const getPreferences = () =>
  readValue<DietPreferences>(KEYS.preferences);
export const savePreferences = (value: DietPreferences) =>
  writeValue(KEYS.preferences, value);

export const getMealPlan = () =>
  readValue<MealPlanResponse>(KEYS.mealPlan);
export const saveMealPlan = (value: MealPlanResponse) =>
  writeValue(KEYS.mealPlan, value);

export function getLocalAccountProgress() {
  return {
    profile_completed: Boolean(getProfile()),
    preferences_completed: Boolean(getPreferences()),
    has_meal_plan: Boolean(getMealPlan())
  };
}

/**
 * Logout hanya menghapus identitas sesi aktif. Data profil dan meal plan
 * tetap ada pada sesi demo agar alur login ulang dapat diuji.
 * Pada production, data permanen harus dimuat dari backend per akun.
 */
export function clearAuthSession(): void {
  if (typeof window === "undefined") return;
  window.sessionStorage.removeItem(KEYS.currentUser);
}

export function clearDietMateSession(): void {
  if (typeof window === "undefined") return;
  Object.values(KEYS).forEach((key) => window.sessionStorage.removeItem(key));
}
