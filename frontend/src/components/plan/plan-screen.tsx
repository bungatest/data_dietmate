"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/ui/app-header";
import { Icon } from "@/components/ui/icon";
import { BottomNavigation } from "@/components/navigation/bottom-navigation";
import { getCurrentUser, getMealPlan, getProfile } from "@/lib/storage/session";
import type { MealPlanResponse, MealType } from "@/types/dietmate";

const MEAL_LABELS: Record<MealType, string> = {
  breakfast: "Sarapan",
  lunch: "Makan siang",
  dinner: "Makan malam"
};

const SOURCE_LABELS: Record<MealPlanResponse["source"], string> = {
  mock: "MODE DEMO",
  stub: "DATABASE",
  rag: "AI · RAG"
};

export function PlanScreen() {
  const router = useRouter();
  const [plan, setPlan] = useState<MealPlanResponse | null>(null);
  const [activeDay, setActiveDay] = useState(1);
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const currentUser = getCurrentUser();
    if (!currentUser) {
      router.replace("/login");
      return;
    }
    setUserName(currentUser.name);
    const saved = getMealPlan();
    if (!saved) {
      router.replace(getProfile() ? "/preferensi" : "/profil");
      return;
    }
    setPlan(saved);
  }, [router]);

  const day = useMemo(
    () => plan?.days.find((item) => item.day_number === activeDay),
    [plan, activeDay]
  );

  if (!plan) {
    return <main className="min-h-dvh bg-white" />;
  }

  const summary = plan.nutrition_summary;

  return (
    <main className="min-h-dvh bg-[#F7F9F8] pb-8">
      <AppHeader title="7-Day Meal Plan" backHref="/dashboard" />

      <div className="space-y-5 px-5 pb-8 pt-5">
        <div className="mb-1">
          <p className="text-[18px] font-bold text-dietmate-deep">Hi, {userName || "Teman DietMate"}!</p>
          <p className="mt-0.5 text-[10px] text-gray-500">Your personalized diet planner</p>
        </div>

        <section className="rounded-[22px] bg-[#244735] p-4 text-white shadow-soft">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[10px] text-[#BFE4CD]">TARGET KALORI HARIAN</p>
              <p className="mt-1 text-2xl font-bold text-[#FFD66B]">
                {summary.target_calories_kcal.toLocaleString("id-ID")} <span className="text-xs font-medium">kcal</span>
              </p>
            </div>
            <span className="rounded-full bg-white/10 px-3 py-1 text-[9px]">
              {SOURCE_LABELS[plan.source] ?? plan.source}
            </span>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-2 border-t border-white/15 pt-3">
            <div>
              <p className="text-[9px] text-[#BFE4CD]">BMI</p>
              <p className="text-sm font-bold">{summary.bmi.toFixed(1)}</p>
            </div>
            <div>
              <p className="text-[9px] text-[#BFE4CD]">BMR</p>
              <p className="text-sm font-bold">{summary.bmr_kcal.toLocaleString("id-ID")}</p>
            </div>
            <div>
              <p className="text-[9px] text-[#BFE4CD]">TDEE</p>
              <p className="text-sm font-bold">{summary.tdee_kcal.toLocaleString("id-ID")}</p>
            </div>
          </div>
        </section>

        {plan.source === "mock" && (
          <section className="rounded-xl border border-amber-200 bg-amber-50 p-3 text-[10px] leading-4 text-amber-800">
            <strong>Data simulasi.</strong> Menu dan nutrisi pada halaman ini hanya contoh untuk pengembangan UI. Belum diambil dari dataset maupun pipeline RAG.
          </section>
        )}

        {plan.validation.warnings.length > 0 && (
          <section className="rounded-xl border border-gray-200 bg-white p-3">
            <p className="mb-1 text-[10px] font-bold text-gray-700">Catatan validasi</p>
            {plan.validation.warnings.map((warning) => (
              <p key={warning} className="text-[10px] leading-4 text-gray-500">• {warning}</p>
            ))}
          </section>
        )}

        <section>
          <div className="mb-3 flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-gray-800">Rencana Makan</h2>
              <p className="mt-1 text-[10px] text-gray-500">{plan.days.length} hari meal plan</p>
            </div>
            <span className="text-[10px] font-medium text-dietmate-accent">Pilih hari</span>
          </div>
          <div className="-mx-5 flex gap-2 overflow-x-auto px-5 pb-2">
            {plan.days.map((item) => (
              <button
                key={item.day_number}
                type="button"
                onClick={() => setActiveDay(item.day_number)}
                aria-pressed={activeDay === item.day_number}
                className={`min-w-11 rounded-xl border px-3 py-2 text-center ${
                  activeDay === item.day_number
                    ? "border-dietmate-dark bg-dietmate-dark text-white"
                    : "border-gray-200 bg-white text-gray-600"
                }`}
              >
                <span className="block text-[9px]">Hari</span>
                <span className="text-sm font-bold">{item.day_number}</span>
              </button>
            ))}
          </div>
        </section>

        {day && (
          <>
            <section className="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[10px] text-gray-500">Total nutrisi hari {day.day_number}</p>
                  <p className="mt-1 text-lg font-bold text-dietmate-deep">
                    {Math.round(day.totals.calories_kcal).toLocaleString("id-ID")} kcal
                  </p>
                </div>
                <Icon name="calendar" size={22} className="text-dietmate-accent" />
              </div>
              <div className="mt-3 grid grid-cols-3 gap-2 border-t border-gray-100 pt-3">
                <div><p className="text-[9px] text-gray-400">Protein</p><p className="text-xs font-bold text-gray-700">{day.totals.protein_g} g</p></div>
                <div><p className="text-[9px] text-gray-400">Karbohidrat</p><p className="text-xs font-bold text-gray-700">{day.totals.carbs_g} g</p></div>
                <div><p className="text-[9px] text-gray-400">Lemak</p><p className="text-xs font-bold text-gray-700">{day.totals.fat_g} g</p></div>
              </div>
            </section>

            <section className="space-y-3">
              {day.meals.map((meal) => (
                <Link
                  key={`${day.day_number}-${meal.recipe.id}-${meal.meal_type}`}
                  href={`/resep/${meal.recipe.id}`}
                  className="flex gap-3 rounded-2xl border border-gray-100 bg-white p-3 shadow-sm transition hover:border-[#A8CBB6]"
                >
                  <div className="flex h-[76px] w-[76px] shrink-0 items-center justify-center rounded-xl bg-dietmate-light text-dietmate-dark">
                    <Icon name="utensils" size={27} />
                  </div>
                  <div className="min-w-0 flex-1 py-0.5">
                    <p className="text-[9px] font-semibold uppercase tracking-wide text-dietmate-accent">
                      {MEAL_LABELS[meal.meal_type]}
                    </p>
                    <h3 className="mt-1 text-xs font-bold text-gray-800">{meal.recipe.name}</h3>
                    <p className="mt-1 line-clamp-2 text-[10px] leading-4 text-gray-500">{meal.recipe.description}</p>
                    <div className="mt-2 flex items-center justify-between text-[9px] text-gray-500">
                      <span>{meal.nutrition.calories_kcal} kcal</span>
                      <span className="flex items-center gap-1 text-dietmate-dark">Detail resep <Icon name="chevron-right" size={12} /></span>
                    </div>
                  </div>
                </Link>
              ))}
            </section>
          </>
        )}

        <button
          type="button"
          onClick={() => router.push("/profil")}
          className="w-full rounded-xl border border-dietmate-dark py-3 text-xs font-semibold text-dietmate-dark"
        >
          Buat meal plan baru
        </button>
      </div>
      <BottomNavigation active="plan" />
    </main>
  );
}
