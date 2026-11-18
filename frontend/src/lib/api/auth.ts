import type {
  AccountProgress,
  AuthResult,
  DietMateUser,
  LoginPayload,
  RegisterPayload
} from "@/types/auth";
import {
  getLocalAccountProgress,
  getCurrentUser,
  getMockAccount,
  saveCurrentUser,
  saveMockAccount,
  clearAuthSession
} from "@/lib/storage/session";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/+$/, "");
const USE_MOCK_API = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";

function getMockUser(email: string, name?: string): DietMateUser {
  const previous = getCurrentUser() ?? getMockAccount();
  const normalizedEmail = email.trim().toLowerCase();
  return {
    id: `demo-${normalizedEmail}`,
    name: name?.trim() || (previous?.email === normalizedEmail
      ? previous.name
      : normalizedEmail.split("@")[0]),
    email: normalizedEmail
  };
}

async function postAuth<T>(path: string, payload?: unknown): Promise<T> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL belum diatur.");
  }

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: payload ? JSON.stringify(payload) : undefined,
      cache: "no-store"
    });
  } catch {
    throw new Error("Tidak dapat terhubung ke server DietMate. Periksa koneksi backend.");
  }

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = typeof body?.detail === "string"
      ? body.detail
      : typeof body?.message === "string"
        ? body.message
        : `Permintaan gagal (HTTP ${response.status}).`;
    throw new Error(message);
  }
  return body as T;
}

function normalizeAuthResult(
  result: AuthResult | { user: DietMateUser; onboarding_status?: AccountProgress }
): AuthResult {
  const progress = "progress" in result
    ? result.progress
    : result.onboarding_status ?? getLocalAccountProgress();
  return { user: result.user, progress };
}

export async function registerAccount(payload: RegisterPayload): Promise<DietMateUser> {
  let user: DietMateUser;

  if (USE_MOCK_API) {
    // Mode demo hanya menyimpan identitas non-rahasia. Password tidak disimpan.
    user = getMockUser(payload.email, payload.name);
    saveMockAccount(user);
  } else {
    const result = await postAuth<{ user: DietMateUser }>("/api/v1/auth/register", payload);
    user = result.user;
  }

  saveCurrentUser(user);
  return user;
}

export async function loginAccount(payload: LoginPayload): Promise<AuthResult> {
  let result: AuthResult;

  if (USE_MOCK_API) {
    // Mode demo hanya mengizinkan akun yang dibuat melalui form Daftar pada sesi ini.
    // Password tidak disimpan/diperiksa; ini bukan autentikasi sungguhan.
    const demoAccount = getMockAccount();
    if (!demoAccount || demoAccount.email !== payload.email.trim().toLowerCase()) {
      throw new Error("Akun demo belum terdaftar. Silakan daftar terlebih dahulu.");
    }
    const user = getMockUser(payload.email, demoAccount.name);
    result = { user, progress: getLocalAccountProgress() };
  } else {
    const response = await postAuth<AuthResult | { user: DietMateUser; onboarding_status?: AccountProgress }>(
      "/api/v1/auth/login",
      payload
    );
    result = normalizeAuthResult(response);
  }

  saveCurrentUser(result.user);
  return result;
}

export async function logoutAccount(): Promise<void> {
  if (!USE_MOCK_API) {
    await postAuth<{ message?: string }>("/api/v1/auth/logout");
  }
  clearAuthSession();
}

export function getRouteAfterLogin(progress: AccountProgress): string {
  if (progress.has_meal_plan) return "/dashboard";
  if (progress.profile_completed) return "/preferensi";
  return "/profil";
}

export function isMockAuthMode(): boolean {
  return USE_MOCK_API;
}
