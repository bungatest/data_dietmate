import { createMockMealPlan } from "@/lib/mock/meal-plan";
import type {
  GenerateMealPlanRequest,
  MealPlanResponse
} from "@/types/dietmate";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/+$/, "");
const USE_MOCK_API = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";

/**
 * Kontrak endpoint yang direkomendasikan untuk disepakati bersama anggota backend:
 * POST {API_BASE_URL}/api/v1/meal-plans/generate
 *
 * Frontend hanya mengakses FastAPI. Frontend tidak boleh mengakses
 * PostgreSQL, ChromaDB, embedding model, atau LLM secara langsung.
 */
export async function generateMealPlan(
  payload: GenerateMealPlanRequest
): Promise<MealPlanResponse> {
  if (USE_MOCK_API) {
    return createMockMealPlan(payload);
  }

  if (!API_BASE_URL) {
    throw new Error(
      "NEXT_PUBLIC_API_BASE_URL belum diatur. Isi URL FastAPI atau aktifkan mode demo."
    );
  }

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/v1/meal-plans/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      cache: "no-store"
    });
  } catch {
    throw new Error(
      "Tidak dapat terhubung ke backend DietMate. Periksa URL API dan koneksi server."
    );
  }

  const contentType = response.headers.get("content-type") ?? "";
  const body = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail =
      typeof body === "object" && body !== null
        ? "detail" in body
          ? (body as { detail?: unknown }).detail
          : "message" in body
            ? (body as { message?: unknown }).message
            : undefined
        : body;

    throw new Error(
      typeof detail === "string"
        ? detail
        : `Backend mengembalikan HTTP ${response.status}.`
    );
  }

  // Backend harus mengembalikan bentuk MealPlanResponse sesuai README.
  return body as MealPlanResponse;
}

export function isMockMode(): boolean {
  return USE_MOCK_API;
}
