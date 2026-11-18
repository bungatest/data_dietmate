"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { BrandLogo } from "@/components/brand/brand-logo";
import { Icon } from "@/components/ui/icon";
import { BottomNavigation } from "@/components/navigation/bottom-navigation";
import { getCurrentUser, getMealPlan, getProfile } from "@/lib/storage/session";
import type { MealPlanResponse } from "@/types/dietmate";

const MEAL_LABELS = {
  breakfast: "BREAKFAST",
  lunch: "LUNCH",
  dinner: "DINNER"
};

export function DashboardScreen() {
  const router = useRouter();
  const [plan, setPlan] = useState<MealPlanResponse | null>(null);
  const [userName, setUserName] = useState("Teman DietMate");

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

  const firstDay = useMemo(() => plan?.days[0], [plan]);

  if (!plan || !firstDay) {
    return <main className="min-h-dvh bg-white" />;
  }

  const summary = plan.nutrition_summary;
  const macroEnergy = summary.carbs_g * 4 + summary.protein_g * 4 + summary.fat_g * 9;
  const macroPercent = {
    carbs: macroEnergy ? Math.round((summary.carbs_g * 4 / macroEnergy) * 100) : 0,
    protein: macroEnergy ? Math.round((summary.protein_g * 4 / macroEnergy) * 100) : 0,
    fat: macroEnergy ? Math.round((summary.fat_g * 9 / macroEnergy) * 100) : 0
  };
  const initials = userName.trim().split(/\s+/).slice(0, 2).map((part) => part[0]).join("").toUpperCase();

  return (
    <main className="flex min-h-dvh flex-col bg-white">
      <header className="rounded-b-[34px] bg-dietmate-dark px-5 pb-6 pt-6 text-white">
        <div className="flex items-center justify-between">
          <BrandLogo light />
          <Link href="/pengaturan" aria-label="Buka profil" className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-white/40 bg-dietmate-light text-xs font-bold text-dietmate-dark">
            {initials || <Icon name="user" size={17} />}
          </Link>
        </div>

        <div className="mt-5">
          <h1 className="text-[20px] font-bold">Hi, {userName.split(" ")[0]}!</h1>
          <p className="mt-0.5 text-[10px] text-[#C5D9CB]">Your personalized diet planner</p>
        </div>

        <section className="mt-4 rounded-[22px] border border-white/10 bg-[#1D422F] p-3.5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-[9px] font-semibold tracking-wide text-[#BBD7C5]">YOUR METRICS</p>
              <p className="mt-1 text-[10px] font-semibold">BMI: {summary.bmi.toFixed(1)} <span className="ml-1 rounded-full bg-[#315E45] px-2 py-0.5 text-[8px] font-medium text-[#CFE5D6]">{summary.bmi_category}</span></p>
            </div>
            <div className="text-right text-[9px] leading-4 text-[#C5D9CB]">
              <p>BMR: <strong className="text-white">{summary.bmr_kcal.toLocaleString("id-ID")} KCAL</strong></p>
              <p>TDEE: <strong className="text-white">{summary.tdee_kcal.toLocaleString("id-ID")} KCAL</strong></p>
            </div>
          </div>

          <div className="mt-3 grid grid-cols-[86px_1fr] items-center gap-3 border-t border-white/10 pt-3">
            <div className="flex justify-center">
              <div
                className="flex h-[76px] w-[76px] items-center justify-center rounded-full p-[6px]"
                style={{ background: "conic-gradient(#E6B66B 0deg 275deg, rgba(255,255,255,0.14) 275deg 360deg)" }}
              >
                <div className="flex h-full w-full flex-col items-center justify-center rounded-full bg-[#1D422F] text-center">
                  <span className="text-[8px] text-[#BBD7C5]">TARGET</span>
                  <strong className="text-[14px] leading-4">{summary.target_calories_kcal.toLocaleString("id-ID")}</strong>
                  <span className="text-[8px] text-[#BBD7C5]">kcal</span>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <MacroBar label="Carbs" grams={summary.carbs_g} percent={macroPercent.carbs} color="bg-[#E6B66B]" />
              <MacroBar label="Protein" grams={summary.protein_g} percent={macroPercent.protein} color="bg-[#65C5A0]" />
              <MacroBar label="Fat" grams={summary.fat_g} percent={macroPercent.fat} color="bg-[#C8E8D4]" />
            </div>
          </div>
        </section>
      </header>

      <section className="flex-1 px-5 pb-5 pt-5">
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-dietmate-deep">Today&apos;s Meal Plan</h2>
            <p className="mt-0.5 text-[9px] text-gray-400">Hari {firstDay.day_number} dari {plan.days.length}</p>
          </div>
          <Link href="/plan" className="text-[10px] font-semibold text-dietmate-dark">View All</Link>
        </div>

        {plan.source === "mock" && (
          <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-[9px] leading-4 text-amber-800">
            Mode demo: menu ini masih data simulasi, belum diambil dari pipeline RAG.
          </div>
        )}

        <div className="space-y-2.5">
          {firstDay.meals.map((meal) => (
            <Link
              key={`${firstDay.day_number}-${meal.recipe.id}-${meal.meal_type}`}
              href={`/resep/${meal.recipe.id}`}
              className="flex items-center gap-3 rounded-2xl border border-gray-100 bg-white p-3 transition hover:border-[#B8D7C3]"
            >
              <div className="flex h-[62px] w-[62px] shrink-0 items-center justify-center rounded-xl bg-dietmate-light text-dietmate-dark">
                <Icon name="utensils" size={25} />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-[8px] font-semibold tracking-wide text-dietmate-accent">{MEAL_LABELS[meal.meal_type]}</p>
                <h3 className="mt-1 truncate text-[11px] font-bold text-gray-800">{meal.recipe.name}</h3>
                <p className="mt-1 text-[10px] font-semibold text-dietmate-dark">{meal.nutrition.calories_kcal} kcal</p>
              </div>
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#EFF8F2] text-dietmate-accent">
                <Icon name="chevron-right" size={15} />
              </span>
            </Link>
          ))}
        </div>

        <button
          type="button"
          onClick={() => router.push("/profil")}
          className="mt-5 w-full rounded-xl border border-dietmate-dark py-3 text-[11px] font-semibold text-dietmate-dark transition hover:bg-dietmate-light"
        >
          Buat Meal Plan Baru
        </button>
      </section>

      <BottomNavigation active="home" />
    </main>
  );
}

function MacroBar({
  label,
  grams,
  percent,
  color
}: {
  label: string;
  grams: number;
  percent: number;
  color: string;
}) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between text-[8px]">
        <span className="text-[#E4EFE7]">{label}: {grams}g</span>
        <span className="text-[#C5D9CB]">{percent}%</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, percent)}%` }} />
      </div>
    </div>
  );
}
