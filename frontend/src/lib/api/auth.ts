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
  getAccessToken,
  saveAccessToken,
  saveCurrentUser,
  saveMockAccount,
  clearAuthSession,
  clearDietMateSession
} from "@/lib/storage/session";
import { hydrateAccountData } from "@/lib/api/profile";

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

function buildAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const token = getAccessToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function postAuth<T>(path: string, payload?: unknown): Promise<T> {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL belum diatur.");
  }

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: buildAuthHeaders(),
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
  result: AuthResult | { user: DietMateUser; onboarding_status?: AccountProgress; access_token?: string }
): AuthResult {
  const progress = "progress" in result
    ? result.progress
    : result.onboarding_status ?? getLocalAccountProgress();
  return { user: result.user, progress, access_token: result.access_token };
}

export async function registerAccount(payload: RegisterPayload): Promise<DietMateUser> {
  let user: DietMateUser;

  if (USE_MOCK_API) {
    // Mode demo hanya menyimpan identitas non-rahasia. Password tidak disimpan.
    user = getMockUser(payload.email, payload.name);
    saveMockAccount(user);
  } else {
    const result = await postAuth<{ user: DietMateUser; access_token?: string }>(
      "/api/v1/auth/register",
      payload
    );
    clearDietMateSession();
    user = result.user;
    if (result.access_token) saveAccessToken(result.access_token);
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
    // Hapus data akun sebelumnya di tab ini agar tidak terbawa ke akun yang baru login.
    clearDietMateSession();
    if (result.access_token) saveAccessToken(result.access_token);
    saveCurrentUser(result.user);
    try {
      await hydrateAccountData();
    } catch (err) {
      // Login tetap berhasil; data akun akan diisi ulang saat user melengkapi form.
      console.warn("Gagal memuat data akun dari server:", err);
    }
    return result;
  }

  saveCurrentUser(result.user);
  return result;
}

export async function logoutAccount(): Promise<void> {
  try {
    if (!USE_MOCK_API) {
      await postAuth<{ message?: string }>("/api/v1/auth/logout");
    }
  } finally {
    // Token stateless: sesi lokal selalu dihapus walaupun request logout gagal.
    // Mode backend: data akun ada di server, jadi seluruh cache sesi ikut dihapus.
    if (USE_MOCK_API) clearAuthSession();
    else clearDietMateSession();
  }
}

export function getRouteAfterLogin(progress: AccountProgress): string {
  if (progress.has_meal_plan) return "/dashboard";
  if (progress.profile_completed) return "/preferensi";
  return "/profil";
}

export function isMockAuthMode(): boolean {
  return USE_MOCK_API;
}
