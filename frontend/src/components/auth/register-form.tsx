"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { registerAccount, isMockAuthMode } from "@/lib/api/auth";
import { Icon } from "@/components/ui/icon";
import { PrimaryButton } from "@/components/ui/primary-button";

export function RegisterForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (name.trim().length < 2) {
      setError("Masukkan nama lengkap minimal 2 karakter.");
      return;
    }
    if (password.length < 8) {
      setError("Kata sandi minimal 8 karakter.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Konfirmasi kata sandi belum sama.");
      return;
    }
    if (!acceptedTerms) {
      setError("Kamu perlu menyetujui Syarat & Ketentuan terlebih dahulu.");
      return;
    }

    setBusy(true);
    try {
      await registerAccount({ name: name.trim(), email: email.trim(), password });
      // Password hanya dikirim ke API dan tidak disimpan di browser storage.
      router.push("/profil");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Pendaftaran belum berhasil. Coba lagi.");
      setBusy(false);
    }
  }

  const inputClass = "h-10 w-full rounded-xl border border-[#DCE4DF] bg-white px-3 text-[12px] text-[#263B30] outline-none transition placeholder:text-gray-400 focus:border-[#478461] focus:ring-2 focus:ring-[#478461]/10";
  const labelClass = "mb-1.5 block text-[10px] font-medium text-[#34483C]";

  return (
    <main className="flex min-h-dvh flex-col bg-white">
      <header className="flex h-[98px] shrink-0 items-start justify-between rounded-b-[28px] bg-dietmate-dark px-6 pb-5 pt-8 text-white">
        <h1 className="text-[18px] font-bold">Daftar Akun Baru</h1>
        <button
          type="button"
          onClick={() => router.push("/home")}
          aria-label="Tutup halaman daftar"
          className="-mr-1 rounded-full p-1 text-white/80 transition hover:bg-white/10 hover:text-white"
        >
          <Icon name="x" size={18} />
        </button>
      </header>

      <form onSubmit={handleSubmit} className="flex flex-1 flex-col px-6 pb-5 pt-5">
        <div className="space-y-3">
          <label className="block">
            <span className={labelClass}>Nama Lengkap</span>
            <input
              autoComplete="name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="Nama lengkap"
              className={inputClass}
              required
            />
          </label>

          <label className="block">
            <span className={labelClass}>Email</span>
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
            <span className={labelClass}>Kata Sandi</span>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                autoComplete="new-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Minimal 8 karakter"
                className={`${inputClass} pr-12`}
                minLength={8}
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword((value) => !value)}
                className="absolute inset-y-0 right-3 text-[10px] font-medium text-dietmate-accent"
              >
                {showPassword ? "Sembunyikan" : "Lihat"}
              </button>
            </div>
          </label>

          <label className="block">
            <span className={labelClass}>Konfirmasi Kata Sandi</span>
            <input
              type={showPassword ? "text" : "password"}
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              placeholder="Ulangi kata sandi"
              className={inputClass}
              required
            />
          </label>
        </div>

        <label className="mt-4 flex items-start gap-2 text-[10px] leading-4 text-gray-500">
          <input
            type="checkbox"
            checked={acceptedTerms}
            onChange={(event) => setAcceptedTerms(event.target.checked)}
            className="mt-0.5 h-3.5 w-3.5 accent-[#28543C]"
          />
          <span>Saya menyetujui <span className="font-semibold text-dietmate-dark">Syarat & Ketentuan</span> DietMate.</span>
        </label>

        {error && (
          <p role="alert" className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-[10px] leading-4 text-red-700">
            {error}
          </p>
        )}

        {isMockAuthMode() && (
          <p className="mt-3 text-[9px] leading-4 text-gray-400">
            Mode demo: pendaftaran belum membuat akun permanen. Autentikasi sebenarnya akan menggunakan FastAPI.
          </p>
        )}

        <div className="mt-4">
          <PrimaryButton type="submit" busy={busy}>
            Daftar
          </PrimaryButton>
        </div>

        <div className="mt-auto pt-8 text-center text-[11px] text-gray-500">
          Sudah punya akun?{" "}
          <Link href="/login" className="font-bold text-dietmate-dark">
            Masuk
          </Link>
        </div>
      </form>
    </main>
  );
}
