"use client";

import { useEffect, useMemo, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/ui/app-header";
import { Icon } from "@/components/ui/icon";
import { PrimaryButton } from "@/components/ui/primary-button";
import {
  ALLERGY_OPTIONS,
  FOOD_PREFERENCE_OPTIONS,
  GOAL_OPTIONS
} from "@/lib/constants";
import { calculateNutritionPreview } from "@/lib/nutrition/preview";
import { getCurrentUser, getPreferences, getProfile, savePreferences } from "@/lib/storage/session";
import type { DietGoal, UserProfile } from "@/types/dietmate";

export function PreferencesForm() {
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [goal, setGoal] = useState<DietGoal>("weight_loss");
  const [duration, setDuration] = useState(7);
  const [allergies, setAllergies] = useState<string[]>([]);
  const [foodPreferences, setFoodPreferences] = useState<string[]>([]);

  useEffect(() => {
    if (!getCurrentUser()) {
      router.replace("/register");
      return;
    }
    const savedPreferences = getPreferences();
    if (savedPreferences) {
      setGoal(savedPreferences.goal);
      setDuration(savedPreferences.duration_days);
      setAllergies(savedPreferences.allergies);
      setFoodPreferences(savedPreferences.food_preferences);
    }
    const savedProfile = getProfile();
    if (!savedProfile) {
      router.replace("/profil");
      return;
    }
    setProfile(savedProfile);
  }, [router]);

  const preview = useMemo(
    () => (profile ? calculateNutritionPreview(profile) : null),
    [profile]
  );

  const selectedGoal = GOAL_OPTIONS.find((item) => item.value === goal);
  const targetCalories = preview && selectedGoal
    ? Math.max(0, preview.tdee + selectedGoal.adjustment)
    : 0;

  function toggleValue(
    value: string,
    current: string[],
    update: (next: string[]) => void
  ) {
    update(current.includes(value)
      ? current.filter((item) => item !== value)
      : [...current, value]);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    savePreferences({
      goal,
      duration_days: duration,
      allergies,
      food_preferences: foodPreferences
    });
    router.push("/generating");
  }

  return (
    <main className="min-h-dvh bg-[#F7F9F8] pb-6">
      <AppHeader title="Preferensi & Target" step="Langkah 2/2" backHref="/profil" />

      <form onSubmit={handleSubmit} className="space-y-5 px-5 pb-6 pt-5">
        <section className="flex items-center justify-between rounded-2xl bg-[#244735] p-4 text-white shadow-sm">
          <div>
            <p className="text-[9px] font-semibold tracking-wide text-[#BFE4CD]">
              HASIL PERHITUNGAN IMT / BMI
            </p>
            <p className="mt-1 text-xl font-bold">
              {preview ? preview.bmi.toFixed(1) : "—"}
              <span className="ml-1 text-[10px] font-normal text-[#BFE4CD]">
                {preview?.bmiCategory ?? ""}
              </span>
            </p>
          </div>
          <div className="text-right">
            <p className="text-[9px] text-[#BFE4CD]">TDEE Estimasi</p>
            <p className="mt-1 text-sm font-bold text-[#FFD66B]">
              {preview ? `${preview.tdee.toLocaleString("id-ID")} kcal` : "—"}
            </p>
          </div>
        </section>

        <section>
          <div className="mb-3 flex items-center justify-between gap-2">
            <h2 className="text-xs font-bold text-gray-800">Tujuan Diet</h2>
            <span className="rounded-full bg-[#DDF4E5] px-2.5 py-1 text-[9px] font-medium text-dietmate-dark">
              Target simulasi
            </span>
          </div>

          <div className="space-y-2.5">
            {GOAL_OPTIONS.map((option) => {
              const selected = goal === option.value;
              const estimate = preview
                ? Math.max(0, preview.tdee + option.adjustment)
                : null;

              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setGoal(option.value)}
                  aria-pressed={selected}
                  className={`flex w-full items-center gap-3 rounded-2xl border p-3.5 text-left transition ${
                    selected
                      ? "border-[#72B58F] bg-[#EFFAF3]"
                      : "border-gray-200 bg-white"
                  }`}
                >
                  <span className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${
                    selected ? "bg-white text-dietmate-accent" : "bg-gray-100 text-gray-500"
                  }`}>
                    <Icon name={option.value === "weight_loss" ? "activity" : option.value === "maintenance" ? "heart" : "target"} size={18} />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-[11px] font-bold text-gray-800">{option.title}</span>
                    <span className="mt-1 block text-[9px] leading-4 text-gray-500">
                      {option.description}
                      {estimate !== null ? ` • ${estimate.toLocaleString("id-ID")} kcal/hari` : ""}
                    </span>
                  </span>
                  <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${
                    selected ? "border-dietmate-accent bg-dietmate-accent text-white" : "border-gray-300"
                  }`}>
                    {selected && <Icon name="check" size={13} />}
                  </span>
                </button>
              );
            })}
          </div>
          <p className="mt-2 text-[9px] leading-4 text-gray-400">
            Penyesuaian defisit 500 kkal dan surplus 300 kkal mengikuti aturan awal proposal untuk prototipe. Backend tetap perlu mengevaluasi keamanan dan kesesuaian target sebelum rekomendasi ditampilkan.
          </p>
        </section>

        <section>
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-xs font-bold text-gray-800">Durasi Rencana Resep</h2>
            <span className="rounded-full bg-[#DDF4E5] px-2.5 py-1 text-[9px] font-medium text-dietmate-dark">
              {duration} hari
            </span>
          </div>
          <p className="mb-3 text-[10px] text-gray-500">
            Pilih rentang hari meal plan yang ingin dibuat (1–7 hari).
          </p>
          <div className="grid grid-cols-7 gap-1.5">
            {[1, 2, 3, 4, 5, 6, 7].map((day) => (
              <button
                key={day}
                type="button"
                onClick={() => setDuration(day)}
                aria-pressed={duration === day}
                className={`rounded-xl border py-2.5 text-center transition ${
                  duration === day
                    ? "border-dietmate-dark bg-dietmate-dark text-white"
                    : "border-gray-200 bg-white text-gray-600"
                }`}
              >
                <span className="block text-xs font-bold">{day}</span>
                <span className="text-[9px]">Hr</span>
              </button>
            ))}
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-xs font-bold text-gray-800">Alergi & Pantangan</h2>
          <div className="flex flex-wrap gap-2">
            {ALLERGY_OPTIONS.map((option) => {
              const selected = allergies.includes(option.value);
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => toggleValue(option.value, allergies, setAllergies)}
                  aria-pressed={selected}
                  className={`rounded-full border px-3 py-2 text-[10px] font-medium transition ${
                    selected
                      ? "border-[#8BC6A2] bg-[#E2F6E9] text-dietmate-dark"
                      : "border-gray-200 bg-white text-gray-600"
                  }`}
                >
                  {option.label} {selected && "✓"}
                </button>
              );
            })}
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-xs font-bold text-gray-800">Preferensi Makanan</h2>
          <div className="flex flex-wrap gap-2">
            {FOOD_PREFERENCE_OPTIONS.map((option) => {
              const selected = foodPreferences.includes(option.value);
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => toggleValue(option.value, foodPreferences, setFoodPreferences)}
                  aria-pressed={selected}
                  className={`rounded-full border px-3 py-2 text-[10px] font-medium transition ${
                    selected
                      ? "border-[#8BC6A2] bg-[#E2F6E9] text-dietmate-dark"
                      : "border-gray-200 bg-white text-gray-600"
                  }`}
                >
                  {option.label} {selected && "✓"}
                </button>
              );
            })}
          </div>
        </section>

        <section className="rounded-xl bg-blue-50 p-3 text-[10px] leading-4 text-blue-800">
          <div className="flex gap-2">
            <Icon name="info" size={15} className="mt-0.5 shrink-0" />
            <p>
              Pada mode demo, hasil menu menggunakan data contoh. Setelah FastAPI dan RAG tersedia, pilihan ini akan dikirim ke backend untuk retrieval resep dan validasi nutrisi.
            </p>
          </div>
        </section>

        <div className="sticky bottom-0 -mx-5 border-t border-gray-100 bg-[#F7F9F8]/95 px-5 pb-2 pt-3 backdrop-blur">
          <PrimaryButton type="submit">
            Buat Meal Plan {duration} Hari <Icon name="sparkles" size={16} />
          </PrimaryButton>
        </div>
      </form>
    </main>
  );
}
