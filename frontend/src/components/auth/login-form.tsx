"use client";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { Icon } from "@/components/ui/icon";
import { PrimaryButton } from "@/components/ui/primary-button";
import { getRouteAfterLogin, isMockAuthMode, loginAccount } from "@/lib/api/auth";

export function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setNotice("");
    setBusy(true);

    try {
      const result = await loginAccount({ email: email.trim(), password });
      router.push(getRouteAfterLogin(result.progress));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Tidak dapat masuk. Periksa email dan kata sandi.");
      setBusy(false);
    }
  }

  const inputClass = "h-10 w-full rounded-xl border border-[#DCE4DF] bg-white px-3 text-[12px] text-[#263B30] outline-none transition placeholder:text-gray-400 focus:border-[#478461] focus:ring-2 focus:ring-[#478461]/10";

  return (
    <main className="flex min-h-dvh flex-col bg-white">
      <header className="relative flex min-h-[194px] shrink-0 flex-col rounded-b-[30px] bg-dietmate-dark px-6 pb-6 pt-8 text-white">
        <div className="flex items-center justify-between">
          <h1 className="text-[19px] font-bold">Masuk</h1>
          <button
            type="button"
            onClick={() => router.push("/home")}
            aria-label="Kembali ke beranda"
            className="rounded-full p-1 text-white/85 hover:bg-white/10"
          >
            <Icon name="arrow-left" size={20} />
          </button>
        </div>

        <div className="mt-3 flex flex-1 flex-col items-center justify-center">
          <div className="flex h-[76px] w-[96px] flex-col items-center justify-center rounded-2xl bg-white p-2">
            <Image
              src="/images/dietmate-logo.png"
              alt="DietMate"
              width={43}
              height={43}
              className="h-10 w-10 object-contain"
              priority
            />
            <span className="mt-0.5 text-[15px] font-extrabold tracking-tight text-dietmate-accent">DietMate</span>
          </div>
          <p className="mt-2 text-[9px] font-semibold tracking-[1.4px] text-[#D3E5D9]">
            SMART DIET PLANNER
          </p>
        </div>
      </header>

      <form onSubmit={handleSubmit} className="flex flex-1 flex-col px-6 pb-6 pt-5">
        <div className="space-y-4">
          <label className="block">
            <span className="mb-1.5 block text-[10px] font-medium text-[#34483C]">Email</span>
            <input
              type="email"
              autoComplete="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="nama@email.com"
              className={inputClass}
              required
            />
          </label>

          <label className="block">
            <span className="mb-1.5 block text-[10px] font-medium text-[#34483C]">Kata Sandi</span>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Masukkan kata sandi"
                className={`${inputClass} pr-14`}
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword((value) => !value)}
                className="absolute inset-y-0 right-3 text-[10px] font-medium text-dietmate-accent"
              >
                {showPassword ? "Sembunyi" : "Lihat"}
              </button>
            </div>
          </label>
        </div>

        <div className="mt-3 flex justify-end">
          <button
            type="button"
            onClick={() => setNotice("Fitur lupa kata sandi akan dihubungkan setelah endpoint pemulihan akun tersedia di FastAPI.")}
            className="text-[10px] font-medium text-gray-500 hover:text-dietmate-dark"
          >
            Lupa Kata Sandi?
          </button>
        </div>

        {notice && <p className="mt-3 rounded-xl bg-dietmate-light px-3 py-2 text-[10px] leading-4 text-dietmate-dark">{notice}</p>}
        {error && <p role="alert" className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-[10px] leading-4 text-red-700">{error}</p>}
        {isMockAuthMode() && (
          <p className="mt-3 text-[9px] leading-4 text-gray-400">
            Mode demo: email dan kata sandi belum diverifikasi server. Gunakan untuk mencoba alur navigasi saja.
          </p>
        )}

        <div className="mt-7">
          <PrimaryButton type="submit" busy={busy}>Masuk</PrimaryButton>
        </div>

        <div className="mt-auto pt-8 text-center text-[11px] text-gray-500">
          Belum punya akun?{" "}
          <Link href="/register" className="font-bold text-dietmate-dark">Daftar</Link>
        </div>
      </form>
    </main>
  );
}
