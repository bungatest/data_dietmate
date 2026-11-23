"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/ui/app-header";
import { Icon } from "@/components/ui/icon";
import { getMealPlan } from "@/lib/storage/session";
import type { Recipe } from "@/types/dietmate";

export function RecipeDetailScreen({ recipeId }: { recipeId: string }) {
  const router = useRouter();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [nutrition, setNutrition] = useState<{
    calories_kcal: number;
    protein_g: number;
    carbs_g: number;
    fat_g: number;
  } | null>(null);

  useEffect(() => {
    const plan = getMealPlan();
    if (!plan) {
      router.replace("/dashboard");
      return;
    }
    for (const day of plan.days) {
      const found = day.meals.find((meal) => meal.recipe.id === recipeId);
      if (found) {
        setRecipe(found.recipe);
        setNutrition(found.nutrition);
        return;
      }
    }
  }, [recipeId, router]);

  if (!recipe) {
    return (
      <main className="min-h-dvh bg-white p-6">
        <p className="text-sm text-gray-500">Memuat detail resep...</p>
      </main>
    );
  }

  return (
    <main className="min-h-dvh bg-[#F7F9F8]">
      <AppHeader title="Detail Resep" backHref="/dashboard" />
      <div className="space-y-5 px-5 pb-8 pt-5">
        <div className="flex h-44 items-center justify-center rounded-[24px] bg-dietmate-light text-dietmate-dark">
          <Icon name="utensils" size={58} />
        </div>
        <section>
          <div className="mb-2 flex flex-wrap gap-2">
            {recipe.tags.map((tag) => (
              <span key={tag} className="rounded-full bg-[#DDF4E5] px-2.5 py-1 text-[9px] font-medium text-dietmate-dark">{tag}</span>
            ))}
          </div>
          <h1 className="text-xl font-bold text-dietmate-deep">{recipe.name}</h1>
          <p className="mt-2 text-xs leading-5 text-gray-500">{recipe.description}</p>
          <div className="mt-3 flex items-center gap-4 text-[10px] text-gray-500">
            <span className="flex items-center gap-1"><Icon name="clock" size={13} /> {recipe.prep_time_minutes} menit</span>
            <span className="flex items-center gap-1"><Icon name="utensils" size={13} /> {recipe.servings} porsi</span>
          </div>
        </section>

        {nutrition && (
          <section className="grid grid-cols-4 gap-2 rounded-2xl bg-white p-3 shadow-sm">
            <div><p className="text-[9px] text-gray-400">Kalori</p><p className="text-xs font-bold text-dietmate-dark">{nutrition.calories_kcal}</p><p className="text-[8px] text-gray-400">kcal</p></div>
            <div><p className="text-[9px] text-gray-400">Protein</p><p className="text-xs font-bold text-dietmate-dark">{nutrition.protein_g}</p><p className="text-[8px] text-gray-400">gram</p></div>
            <div><p className="text-[9px] text-gray-400">Karbo</p><p className="text-xs font-bold text-dietmate-dark">{nutrition.carbs_g}</p><p className="text-[8px] text-gray-400">gram</p></div>
            <div><p className="text-[9px] text-gray-400">Lemak</p><p className="text-xs font-bold text-dietmate-dark">{nutrition.fat_g}</p><p className="text-[8px] text-gray-400">gram</p></div>
          </section>
        )}

        <section className="rounded-2xl bg-white p-4 shadow-sm">
          <h2 className="mb-3 text-sm font-bold text-gray-800">Bahan-bahan</h2>
          <ul className="space-y-2">
            {recipe.ingredients.map((ingredient) => (
              <li key={ingredient} className="flex items-start gap-2 text-xs text-gray-600">
                <Icon name="check" size={14} className="mt-0.5 shrink-0 text-dietmate-accent" />
                {ingredient}
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-2xl bg-white p-4 shadow-sm">
          <h2 className="mb-3 text-sm font-bold text-gray-800">Cara Memasak</h2>
          <ol className="space-y-3">
            {recipe.instructions.map((instruction, index) => (
              <li key={instruction} className="flex gap-3 text-xs leading-5 text-gray-600">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-dietmate-light text-[10px] font-bold text-dietmate-dark">{index + 1}</span>
                {instruction}
              </li>
            ))}
          </ol>
        </section>

        <Link href="/dashboard" className="block rounded-2xl bg-dietmate-dark py-3 text-center text-xs font-semibold text-white">
          Kembali ke Meal Plan
        </Link>
      </div>
    </main>
  );
}
