import {
  getAccessToken,
  saveMealPlan,
  savePreferences,
  saveProfile
} from "@/lib/storage/session";
import type {
  DietPreferences,
  MealPlanResponse,
  UserProfile
} from "@/types/dietmate";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/+$/, "");
const USE_MOCK_API = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";

interface StoredProfileResponse {
  profile: UserProfile | null;
  preferences: DietPreferences | null;
  updated_at: string | null;
}

class ApiError extends Error {
  constructor(message: string, readonly status: number) {
    super(message);
  }
}

async function authorizedRequest<T>(
  path: string,
  init: { method?: string; body?: unknown } = {}
): Promise<T> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL belum diatur.");
  }
  const token = getAccessToken();
  if (!token) {
    throw new ApiError("Sesi login tidak ditemukan. Silakan login kembali.", 401);
  }

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: init.method ?? "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: init.body === undefined ? undefined : JSON.stringify(init.body),
      cache: "no-store"
    });
  } catch {
    throw new Error("Tidak dapat terhubung ke server DietMate. Periksa koneksi backend.");
  }

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = typeof body?.detail === "string"
      ? body.detail
      : `Permintaan gagal (HTTP ${response.status}).`;
    throw new ApiError(detail, response.status);
  }
  return body as T;
}

/** Simpan profil fisik ke backend (tabel user_profiles). No-op pada mode demo. */
export async function saveProfileRemote(profile: UserProfile): Promise<void> {
  if (USE_MOCK_API) return;
  await authorizedRequest<StoredProfileResponse>("/api/v1/users/me/profile", {
    method: "PUT",
    body: profile
  });
}

/** Simpan preferensi diet ke backend. No-op pada mode demo. */
export async function savePreferencesRemote(preferences: DietPreferences): Promise<void> {
  if (USE_MOCK_API) return;
  await authorizedRequest<StoredProfileResponse>("/api/v1/users/me/preferences", {
    method: "PUT",
    body: preferences
  });
}

/**
 * Memuat profil, preferensi, dan meal plan terakhir dari backend ke sessionStorage,
 * agar login di browser/perangkat lain langsung mendapat data akun yang sama.
 */
export async function hydrateAccountData(): Promise<void> {
  if (USE_MOCK_API) return;

  const stored = await authorizedRequest<StoredProfileResponse>("/api/v1/users/me/profile");
  if (stored.profile) saveProfile(stored.profile);
  if (stored.preferences) savePreferences(stored.preferences);

  try {
    const plan = await authorizedRequest<MealPlanResponse>("/api/v1/meal-plans/latest");
    saveMealPlan(plan);
  } catch (err) {
    // 404 = akun belum punya meal plan; bukan error.
    if (!(err instanceof ApiError && err.status === 404)) throw err;
  }
}
