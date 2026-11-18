import Link from "next/link";
import { Icon } from "@/components/ui/icon";

const items = [
  { href: "/dashboard", label: "Home", icon: "home" as const, key: "home" },
  { href: "/plan", label: "Plan", icon: "calendar" as const, key: "plan" },
  { href: "/pengaturan", label: "Profile", icon: "user" as const, key: "profile" }
];

export function BottomNavigation({ active }: { active: "home" | "plan" | "profile" }) {
  return (
    <nav className="sticky bottom-0 z-20 grid grid-cols-3 border-t border-gray-100 bg-white/95 px-4 pb-[max(env(safe-area-inset-bottom),8px)] pt-2 backdrop-blur">
      {items.map((item) => {
        const selected = active === item.key;
        return (
          <Link
            key={item.key}
            href={item.href}
            aria-current={selected ? "page" : undefined}
            className={`flex flex-col items-center gap-1 py-1 text-[9px] font-medium transition ${selected ? "text-dietmate-dark" : "text-slate-400"}`}
          >
            <Icon name={item.icon} size={18} />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
