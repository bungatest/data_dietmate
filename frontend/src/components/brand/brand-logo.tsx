import Image from "next/image";

export function BrandLogo({
  compact = false,
  light = false
}: {
  compact?: boolean;
  light?: boolean;
}) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white p-1 shadow-sm">
        <Image
          src="/images/dietmate-logo.png"
          alt="Logo DietMate"
          width={30}
          height={30}
          priority
        />
      </div>
      {!compact && (
        <span className={`text-lg font-bold tracking-tight ${light ? "text-white" : "text-dietmate-dark"}`}>
          DietMate
        </span>
      )}
    </div>
  );
}
