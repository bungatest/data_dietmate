import Link from "next/link";
import { BrandLogo } from "@/components/brand/brand-logo";
import { Icon } from "@/components/ui/icon";

export function AppHeader({
  title,
  step,
  backHref = "/home"
}: {
  title: string;
  step?: string;
  backHref?: string;
}) {
  return (
    <header className="flex min-h-[66px] items-center gap-3 rounded-b-[22px] bg-dietmate-dark px-5 py-3 text-white">
      <Link
        href={backHref}
        aria-label="Kembali"
        className="rounded-full p-1 text-white/90 transition hover:bg-white/10"
      >
        <Icon name="arrow-left" size={20} />
      </Link>
      <BrandLogo compact />
      <h1 className="min-w-0 flex-1 truncate text-sm font-semibold">{title}</h1>
      {step && (
        <span className="shrink-0 rounded-full bg-white/15 px-2.5 py-1 text-[10px] font-medium text-white">
          {step}
        </span>
      )}
    </header>
  );
}
