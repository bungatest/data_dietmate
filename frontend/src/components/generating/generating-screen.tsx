"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { BrandLogo } from "@/components/brand/brand-logo";
import { Icon } from "@/components/ui/icon";
import { PrimaryButton } from "@/components/ui/primary-button";
import { generateMealPlan, isMockMode } from "@/lib/api/client";
import {
  getCurrentUser,
  getPreferences,
  getProfile,
  saveMealPlan
} from "@/lib/storage/session";

export function GeneratingScreen() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const requestStarted = useRef(false);

  const run = useCallback(async () => {
    if (requestStarted.current) return;
    requestStarted.current = true;
    setError("");
    if (!getCurrentUser()) {
      router.replace("/register");
      return;
    }
    const profile = getProfile();
    const preferences = getPreferences();

    if (!profile) {
      router.replace("/profil");
      return;
    }
    if (!preferences) {
      router.replace("/preferensi");
      return;
    }

    try {
      const result = await generateMealPlan({ profile, preferences });
      saveMealPlan(result);
      router.replace("/dashboard");
    } catch (err) {
      requestStarted.current = false;
      setError(err instanceof Error ? err.message : "Terjadi kesalahan saat membuat meal plan.");
    }
  }, [router]);

  useEffect(() => {
    void run();
  }, [run, attempt]);

  return (
    <main className="flex min-h-dvh flex-col items-center justify-center bg-white px-7 py-10 text-center">
      <BrandLogo />
      <div className="mt-14 flex h-28 w-28 items-center justify-center rounded-full bg-dietmate-light text-dietmate-dark">
        {error ? <Icon name="alert" size={48} /> : <Icon name="sparkles" size={48} />}
      </div>

      {error ? (
        <>
          <h1 className="mt-8 text-xl font-bold text-dietmate-deep">Meal plan belum berhasil dibuat</h1>
          <p role="alert" className="mt-3 max-w-[300px] text-sm leading-6 text-gray-500">{error}</p>
          <div className="mt-8 w-full space-y-3">
            <PrimaryButton onClick={() => setAttempt((value) => value + 1)}>
              <Icon name="refresh" size={16} /> Coba Lagi
            </PrimaryButton>
            <button
              type="button"
              onClick={() => router.push("/preferensi")}
              className="w-full py-2 text-xs font-semibold text-dietmate-dark"
            >
              Kembali ke Preferensi
            </button>
          </div>
        </>
      ) : (
        <>
          <h1 className="mt-8 text-xl font-bold text-dietmate-deep">Menyiapkan Meal Plan-mu</h1>
          <p className="mt-3 max-w-[290px] text-sm leading-6 text-gray-500">
            DietMate sedang menyiapkan rekomendasi berdasarkan profil, tujuan, dan preferensimu.
          </p>
          <div className="mt-8 h-1.5 w-full max-w-[250px] overflow-hidden rounded-full bg-gray-100">
            <div className="h-full w-2/3 animate-pulse rounded-full bg-dietmate-accent" />
          </div>
          <p className="mt-5 text-[10px] text-gray-400">
            {isMockMode()
              ? "Mode demo: menggunakan data contoh, bukan hasil RAG."
              : "Menghubungi backend DietMate..."}
          </p>
        </>
      )}
    </main>
  );
}
