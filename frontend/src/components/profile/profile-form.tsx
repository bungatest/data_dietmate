"use client";

import { useEffect, useMemo, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/ui/app-header";
import { Icon } from "@/components/ui/icon";
import { PrimaryButton } from "@/components/ui/primary-button";
import { ACTIVITY_OPTIONS } from "@/lib/constants";
import { calculateNutritionPreview } from "@/lib/nutrition/preview";
import { getCurrentUser, getProfile, saveProfile } from "@/lib/storage/session";
import type { ActivityLevel, Gender, UserProfile } from "@/types/dietmate";

export function ProfileForm() {
  const router = useRouter();
  const [age, setAge] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [gender, setGender] = useState<Gender>("female");
  const [activity, setActivity] = useState<ActivityLevel>("moderate");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!getCurrentUser()) {
      router.replace("/register");
      return;
    }
    const saved = getProfile();
    if (!saved) return;
    setAge(String(saved.age));
    setHeight(String(saved.height_cm));
    setWeight(String(saved.weight_kg));
    setGender(saved.gender);
    setActivity(saved.activity_level);
  }, [router]);

  const profile = useMemo<UserProfile | null>(() => {
    const ageValue = Number(age);
    const heightValue = Number(height);
    const weightValue = Number(weight);
    const selectedActivity = ACTIVITY_OPTIONS.find((item) => item.value === activity);

    if (
      !age ||
      !height ||
      !weight ||
      !Number.isFinite(ageValue) ||
      !Number.isFinite(heightValue) ||
      !Number.isFinite(weightValue) ||
      !selectedActivity
    ) return null;

    return {
      age: ageValue,
      gender,
      height_cm: heightValue,
      weight_kg: weightValue,
      activity_level: activity,
      pal: selectedActivity.pal
    };
  }, [age, height, weight, gender, activity]);

  const preview = useMemo(
    () => (profile && profile.age >= 18 && profile.height_cm > 0 && profile.weight_kg > 0
      ? calculateNutritionPreview(profile)
      : null),
    [profile]
  );

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (!profile) {
      setError("Lengkapi usia, tinggi badan, dan berat badan terlebih dahulu.");
      return;
    }
    if (profile.age < 18) {
      setError("Prototype DietMate ini difokuskan untuk pengguna dewasa (minimal 18 tahun).");
      return;
    }
    if (profile.height_cm < 100 || profile.height_cm > 250) {
      setError("Masukkan tinggi badan antara 100–250 cm.");
      return;
    }
    if (profile.weight_kg < 30 || profile.weight_kg > 300) {
      setError("Masukkan berat badan antara 30–300 kg.");
      return;
    }

    saveProfile(profile);
    router.push("/preferensi");
  }

  return (
    <main className="min-h-dvh bg-[#F7F9F8]">
      <AppHeader title="Register & Profil Fisik" step="Langkah 1/2" backHref="/home" />

      <form onSubmit={handleSubmit} className="space-y-5 px-5 pb-8 pt-5">
        <section className="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="grid grid-cols-3 gap-2">
            <label className="min-w-0 text-center">
              <span className="mb-2 block text-[10px] font-medium text-gray-600">Tinggi (cm)</span>
              <input
                type="number"
                inputMode="decimal"
                min="100"
                max="250"
                value={height}
                onChange={(event) => setHeight(event.target.value)}
                placeholder="165"
                className="h-10 w-full rounded-xl border border-gray-200 bg-white px-1 text-center text-sm font-semibold text-gray-800 outline-none focus:border-dietmate-accent"
              />
            </label>
            <label className="min-w-0 text-center">
              <span className="mb-2 block text-[10px] font-medium text-gray-600">Berat (kg)</span>
              <input
                type="number"
                inputMode="decimal"
                min="30"
                max="300"
                value={weight}
                onChange={(event) => setWeight(event.target.value)}
                placeholder="60"
                className="h-10 w-full rounded-xl border border-gray-200 bg-white px-1 text-center text-sm font-semibold text-gray-800 outline-none focus:border-dietmate-accent"
              />
            </label>
            <label className="min-w-0 text-center">
              <span className="mb-2 block text-[10px] font-medium text-gray-600">Usia (tahun)</span>
              <input
                type="number"
                inputMode="numeric"
                min="18"
                max="100"
                value={age}
                onChange={(event) => setAge(event.target.value)}
                placeholder="25"
                className="h-10 w-full rounded-xl border border-gray-200 bg-white px-1 text-center text-sm font-semibold text-gray-800 outline-none focus:border-dietmate-accent"
              />
            </label>
          </div>

          <div className="mt-5 flex items-center gap-3">
            <span className="text-xs font-medium text-gray-600">Gender:</span>
            <div className="flex flex-1 gap-2">
              <button
                type="button"
                onClick={() => setGender("female")}
                className={`flex-1 rounded-full border px-2 py-2 text-[11px] font-medium transition ${
                  gender === "female"
                    ? "border-[#75B28F] bg-[#EFFAF3] text-dietmate-dark"
                    : "border-gray-200 bg-white text-gray-500"
                }`}
              >
                Perempuan ♀
              </button>
              <button
                type="button"
                onClick={() => setGender("male")}
                className={`flex-1 rounded-full border px-2 py-2 text-[11px] font-medium transition ${
                  gender === "male"
                    ? "border-[#75B28F] bg-[#EFFAF3] text-dietmate-dark"
                    : "border-gray-200 bg-white text-gray-500"
                }`}
              >
                Laki-laki ♂
              </button>
            </div>
          </div>
        </section>

        <section>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-xs font-bold text-gray-800">Berapa tingkat aktivitas fisikmu?</h2>
            <span className="rounded-full bg-[#DDF4E5] px-2.5 py-1 text-[10px] font-medium text-dietmate-dark">
              5 Level
            </span>
          </div>

          <div className="-mx-5 flex snap-x gap-2.5 overflow-x-auto px-5 pb-3">
            {ACTIVITY_OPTIONS.map((option, index) => {
              const selected = activity === option.value;
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setActivity(option.value)}
                  aria-pressed={selected}
                  className={`relative flex min-h-[122px] w-[116px] shrink-0 snap-start flex-col items-center justify-center rounded-2xl border p-3 text-center transition ${
                    selected
                      ? "border-dietmate-dark bg-dietmate-dark text-white shadow-md"
                      : "border-gray-200 bg-white text-gray-700"
                  }`}
                >
                  {selected && (
                    <span className="absolute right-2 top-2 rounded-full bg-white/15 p-1">
                      <Icon name="check" size={11} />
                    </span>
                  )}
                  <span className={`mb-2 flex h-8 w-8 items-center justify-center rounded-full ${
                    selected ? "bg-white/15 text-white" : "bg-gray-100 text-gray-500"
                  }`}>
                    <Icon name={index === 0 ? "user" : index === 1 ? "activity" : "flame"} size={16} />
                  </span>
                  <span className="text-[10px] font-semibold leading-4">{option.title}</span>
                  <span className={`mt-1 text-[9px] ${selected ? "text-white/75" : "text-gray-400"}`}>
                    PAL: {option.pal}
                  </span>
                </button>
              );
            })}
          </div>
        </section>

        <section className="rounded-[22px] bg-[#244735] p-4 text-white shadow-soft">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-[11px] font-medium text-[#BFE4CD]">Estimasi otomatis (preview)</p>
            <span className="h-2 w-2 rounded-full bg-[#62D59A]" />
          </div>

          {preview ? (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div className="border-r border-white/15 pr-3">
                  <p className="text-[10px] text-[#BFE4CD]">BMI / IMT</p>
                  <p className="mt-1 text-2xl font-bold">
                    {preview.bmi.toFixed(1)}
                    <span className="ml-1 text-[10px] font-medium text-[#BFE4CD]">
                      ({preview.bmiCategory})
                    </span>
                  </p>
                  <p className="mt-3 text-[10px] text-[#BFE4CD]">TDEE</p>
                  <p className="text-lg font-bold text-[#FFD66B]">
                    {preview.tdee.toLocaleString("id-ID")} kcal
                  </p>
                </div>
                <div className="space-y-3 pl-1">
                  <div>
                    <p className="text-[10px] text-[#BFE4CD]">BMR</p>
                    <p className="text-sm font-bold">{preview.bmr.toLocaleString("id-ID")} kcal</p>
                  </div>
                  <div>
                    <p className="text-[10px] text-[#BFE4CD]">Faktor PAL</p>
                    <p className="text-sm font-bold">{profile?.pal.toFixed(3)}</p>
                  </div>
                  <p className="text-[9px] leading-4 text-[#BFE4CD]">
                    Target kalori dipilih pada langkah berikutnya.
                  </p>
                </div>
              </div>
            </>
          ) : (
            <div className="rounded-xl bg-white/5 px-3 py-4 text-center text-xs text-white/70">
              Isi tinggi, berat, dan usia untuk melihat estimasi BMI, BMR, dan TDEE.
            </div>
          )}
          <p className="mt-3 border-t border-white/15 pt-3 text-[9px] leading-4 text-white/60">
            Nilai ini hanya preview di browser. Perhitungan dan validasi final dilakukan backend FastAPI.
          </p>
        </section>

        {error && (
          <p role="alert" className="rounded-xl bg-red-50 px-3 py-2 text-xs text-red-700">
            {error}
          </p>
        )}

        <PrimaryButton type="submit">
          Lanjutkan <Icon name="arrow-right" size={17} />
        </PrimaryButton>
      </form>
    </main>
  );
}
