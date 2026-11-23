import Link from "next/link";
import { BrandLogo } from "@/components/brand/brand-logo";
import { Icon } from "@/components/ui/icon";

const steps = [
  { number: "1", title: "Isi Profil & Fisik", icon: "user" as const },
  { number: "2", title: "Pilih Target & Preferensi", icon: "sliders" as const },
  { number: "3", title: "Dapatkan Meal Plan", icon: "calendar" as const }
];

export default function HomePage() {
  return (
    <main className="flex min-h-dvh flex-col bg-white">
      <header className="flex h-[98px] shrink-0 items-center rounded-b-[28px] bg-dietmate-dark px-6">
        <BrandLogo light />
      </header>

      <section className="flex flex-1 flex-col px-6 pb-7 pt-6">
        <div>
          <h1 className="text-[20px] font-bold leading-tight text-[#172B22]">
            Mulai Pola Hidup Sehat
          </h1>
          <p className="mt-1 text-[12px] text-gray-500">
            Rencana diet personal bertenaga AI
          </p>
        </div>

        <div className="relative mt-7 flex flex-col gap-5">
          <span
            aria-hidden="true"
            className="pointer-events-none absolute bottom-5 left-5 top-5 border-l border-dashed border-[#76A58A]"
          />
          {steps.map((step) => (
            <div
              key={step.number}
              className="relative z-10 flex min-h-10 items-center gap-3"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[14px] bg-dietmate-light text-dietmate-dark">
                <Icon name={step.icon} size={20} />
              </div>
              <div className="flex items-center gap-2">
                <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-dietmate-dark text-[10px] font-bold text-white">
                  {step.number}
                </span>
                <p className="text-[12px] font-semibold text-[#263B30]">
                  {step.title}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-auto pt-12">
          <Link
            href="/register"
            className="flex h-12 w-full items-center justify-center rounded-full bg-dietmate-dark text-[12px] font-bold text-white shadow-soft transition hover:bg-[#1f432f] active:scale-[0.99]"
          >
            Mulai Sekarang
          </Link>
          <p className="mt-4 text-center text-[11px] text-gray-500">
            Sudah punya akun?{" "}
            <Link href="/login" className="font-bold text-dietmate-dark">
              Masuk
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}
