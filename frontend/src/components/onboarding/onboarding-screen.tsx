"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { BrandLogo } from "@/components/brand/brand-logo";
import { Icon } from "@/components/ui/icon";
import { PrimaryButton } from "@/components/ui/primary-button";

const slides = [
  {
    eyebrow: "KENALI KEBUTUHANMU",
    title: "Kenali Kebutuhan Tubuhmu",
    description:
      "Masukkan profil fisik dan aktivitasmu untuk membantu DietMate menghitung estimasi kebutuhan kalori harian.",
    image: "/images/onboarding/slide-1.png"
  },
  {
    eyebrow: "TENTUKAN TUJUANMU",
    title: "Atur Tujuan & Preferensimu",
    description:
      "Pilih tujuan diet, durasi meal plan, serta preferensi dan pantangan makanan agar rekomendasi lebih sesuai.",
    image: "/images/onboarding/slide-2.png"
  },
  {
    eyebrow: "MEAL PLAN PERSONAL",
    title: "Dapatkan Meal Plan Personal",
    description:
      "DietMate menyusun rekomendasi menu berdasarkan kebutuhan nutrisi dan resep yang tersedia dalam basis pengetahuan.",
    image: "/images/onboarding/slide-3.png"
  }
];

export function OnboardingScreen() {
  const [active, setActive] = useState(0);
  const [imageFailed, setImageFailed] = useState(false);
  const router = useRouter();
  const slide = slides[active];
  const lastSlide = active === slides.length - 1;

  useEffect(() => {
    setImageFailed(false);
  }, [active]);

  return (
    <main className="flex min-h-dvh items-center justify-center bg-dietmate-canvas px-3 py-3">
      <section className="relative mx-auto flex min-h-[calc(100dvh-24px)] w-full max-w-[430px] flex-col overflow-hidden rounded-[30px] bg-dietmate-dark px-6 pb-6 pt-6 text-white shadow-soft">
        <div aria-hidden="true" className="pointer-events-none absolute -right-16 top-16 h-48 w-48 rounded-full bg-white/[0.05] blur-2xl" />
        <div aria-hidden="true" className="pointer-events-none absolute -bottom-16 -left-16 h-52 w-52 rounded-full bg-white/[0.05] blur-2xl" />

        <header className="relative z-10 flex items-center justify-between">
          <BrandLogo light />
          <button
            type="button"
            onClick={() => router.push("/home")}
            className="text-xs font-medium text-white/75 transition hover:text-white"
          >
            Lewati
          </button>
        </header>

        <section className="relative z-10 flex flex-1 flex-col justify-center py-7">
          <div className="mb-7 flex justify-center">
            <div className="relative flex h-[250px] w-[250px] items-center justify-center overflow-hidden rounded-full border-[8px] border-dietmate-light bg-dietmate-light shadow-lg">
              {imageFailed ? (
                <div className="flex flex-col items-center gap-2 text-dietmate-dark">
                  <Icon name="utensils" size={48} />
                  <span className="text-[10px] font-semibold">Tambahkan foto slide</span>
                </div>
              ) : (
                <Image
                  key={slide.image}
                  src={slide.image}
                  alt={slide.title}
                  fill
                  priority={active === 0}
                  sizes="250px"
                  className="object-cover"
                  onError={() => setImageFailed(true)}
                />
              )}
            </div>
          </div>

          <div className="text-center">
            <p className="mb-3 text-[10px] font-bold tracking-[2px] text-[#BBD7C5]">
              {slide.eyebrow}
            </p>
            <h1 className="mx-auto max-w-[290px] text-[26px] font-bold leading-tight text-white">
              {slide.title}
            </h1>
            <p className="mx-auto mt-3 max-w-[300px] text-[13px] leading-6 text-[#E3ECE5]">
              {slide.description}
            </p>
          </div>
        </section>

        <footer className="relative z-10 space-y-6">
          <div className="flex justify-center gap-2">
            {slides.map((item, index) => (
              <button
                key={item.eyebrow}
                type="button"
                onClick={() => setActive(index)}
                aria-label={`Buka slide ${index + 1}`}
                aria-current={active === index ? "step" : undefined}
                className={`h-2 rounded-full transition-all duration-300 ${
                  active === index ? "w-7 bg-white" : "w-2 bg-white/40"
                }`}
              />
            ))}
          </div>

          <div className="flex gap-3">
            {active > 0 && (
              <button
                type="button"
                onClick={() => setActive((value) => value - 1)}
                aria-label="Slide sebelumnya"
                className="flex h-12 w-12 items-center justify-center rounded-xl border border-white/25 text-white"
              >
                <Icon name="arrow-left" />
              </button>
            )}
            <PrimaryButton
              onClick={() => (lastSlide ? router.push("/home") : setActive((value) => value + 1))}
              className="flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-white text-sm font-bold !text-dietmate-dark shadow-lg transition hover:bg-dietmate-light active:scale-[0.98]"
            >
              {lastSlide ? "Mulai Sekarang" : "Lanjutkan"}
              <Icon name="arrow-right" size={17} />
            </PrimaryButton>
          </div>

          <p className="text-center text-[10px] text-[#C5D9CB]">
            Personalized Diet Planner berbasis AI
          </p>
        </footer>
      </section>
    </main>
  );
}
