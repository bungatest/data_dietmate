"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/ui/app-header";
import { Icon } from "@/components/ui/icon";
import { BottomNavigation } from "@/components/navigation/bottom-navigation";
import { logoutAccount } from "@/lib/api/auth";
import { getCurrentUser, getProfile, getPreferences } from "@/lib/storage/session";
import type { DietMateUser } from "@/types/auth";
import type { UserProfile } from "@/types/dietmate";

export function SettingsScreen() {
  const router = useRouter();
  const [user, setUser] = useState<DietMateUser | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [targetLabel, setTargetLabel] = useState("Belum ditentukan");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const current = getCurrentUser();
    if (!current) {
      router.replace("/login");
      return;
    }
    setUser(current);
    setProfile(getProfile());
    const preferences = getPreferences();
    if (preferences) {
      const labels = {
        weight_loss: "Menurunkan Berat Badan",
        maintenance: "Menjaga Berat Badan",
        muscle_gain: "Menambah Massa Otot"
      };
      setTargetLabel(labels[preferences.goal]);
    }
  }, [router]);

  async function handleLogout() {
    setBusy(true);
    try {
      await logoutAccount();
      router.replace("/home");
    } catch (error) {
      setBusy(false);
      window.alert(error instanceof Error ? error.message : "Gagal keluar dari akun.");
    }
  }

  if (!user) return <main className="min-h-dvh bg-white" />;

  return (
    <main className="flex min-h-dvh flex-col bg-white">
      <AppHeader title="Profil & Pengaturan" backHref="/dashboard" />

      <section className="flex-1 px-5 pb-5 pt-5">
        <div className="flex flex-col items-center text-center">
          <div className="-mt-1 flex h-[68px] w-[68px] items-center justify-center rounded-full border-4 border-white bg-dietmate-light text-dietmate-dark shadow-sm">
            <Icon name="user" size={30} />
          </div>
          <h1 className="mt-2 text-sm font-bold text-dietmate-deep">{user.name}</h1>
          <p className="mt-0.5 text-[10px] text-gray-500">{user.email}</p>
          <p className="mt-1 text-[10px] text-gray-500">Target: {targetLabel}</p>
          <Link href="/profil" className="mt-3 inline-flex items-center gap-1.5 rounded-full border border-[#CBE6D5] bg-[#F0FAF3] px-3 py-1.5 text-[10px] font-semibold text-dietmate-dark">
            <Icon name="edit" size={12} /> Update Profil
          </Link>
        </div>

        <section className="mt-5 rounded-2xl border border-[#DCEFE3] bg-[#F1F8F3] p-3">
          <div className="flex items-center justify-between">
            <h2 className="text-[11px] font-bold text-dietmate-deep">Profil Fisik</h2>
            <Link href="/profil" className="text-[9px] font-semibold text-dietmate-dark">Edit</Link>
          </div>
          {profile ? (
            <div className="mt-2 space-y-1 text-[10px] text-gray-600">
              <p>Tinggi: {profile.height_cm} cm</p>
              <p>Berat: {profile.weight_kg} kg</p>
              <p>Usia: {profile.age} tahun</p>
            </div>
          ) : (
            <p className="mt-2 text-[10px] text-gray-500">Profil fisik belum dilengkapi.</p>
          )}
        </section>

        <div className="mt-4 divide-y divide-gray-100">
          <Link href="/profil" className="flex items-center gap-3 py-3">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-dietmate-light text-dietmate-dark"><Icon name="user" size={16} /></span>
            <span className="min-w-0 flex-1"><strong className="block text-[10px] font-semibold text-gray-800">Update Profil Akun</strong><small className="mt-0.5 block text-[9px] text-gray-400">Ubah informasi profil fisik</small></span>
            <Icon name="chevron-right" size={16} className="text-gray-400" />
          </Link>
          <Link href="/profil" className="flex items-center gap-3 py-3">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-600"><Icon name="scale" size={16} /></span>
            <span className="min-w-0 flex-1"><strong className="block text-[10px] font-semibold text-gray-800">Kalkulator Fisik (TB, BB, Usia)</strong><small className="mt-0.5 block text-[9px] text-gray-400">Kalkulasi ulang BMI, BMR, dan TDEE</small></span>
            <Icon name="chevron-right" size={16} className="text-gray-400" />
          </Link>
          <Link href="/preferensi" className="flex items-center gap-3 py-3">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-600"><Icon name="sliders" size={16} /></span>
            <span className="min-w-0 flex-1"><strong className="block text-[10px] font-semibold text-gray-800">Preferensi Makanan & Alergi</strong><small className="mt-0.5 block text-[9px] text-gray-400">Atur pantangan dan durasi resep</small></span>
            <Icon name="chevron-right" size={16} className="text-gray-400" />
          </Link>
          <div className="flex items-center gap-3 py-3 opacity-70">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-600"><Icon name="bell" size={16} /></span>
            <span className="min-w-0 flex-1"><strong className="block text-[10px] font-semibold text-gray-800">Pengaturan Notifikasi</strong><small className="mt-0.5 block text-[9px] text-gray-400">Fitur notifikasi akan tersedia berikutnya</small></span>
            <Icon name="chevron-right" size={16} className="text-gray-400" />
          </div>
        </div>

        <button
          type="button"
          onClick={handleLogout}
          disabled={busy}
          className="mt-5 flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-[#D33C35] text-[11px] font-bold text-white transition hover:bg-[#BD302A] disabled:opacity-60"
        >
          <Icon name="log-out" size={15} /> {busy ? "Keluar..." : "Keluar"}
        </button>
      </section>

      <BottomNavigation active="profile" />
    </main>
  );
}
