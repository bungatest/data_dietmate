import type { ButtonHTMLAttributes, ReactNode } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  busy?: boolean;
};

export function PrimaryButton({
  children,
  busy = false,
  disabled,
  className = "",
  ...props
}: Props) {
  return (
    <button
      {...props}
      disabled={disabled || busy}
      className={`flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl bg-dietmate-dark px-5 py-3 text-sm font-semibold text-white shadow-soft transition hover:bg-[#1f432f] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
    >
      {busy ? "Memproses..." : children}
    </button>
  );
}
