import type { ReactNode } from "react";

export type IconName =
  | "leaf"
  | "heart"
  | "heart-pulse"
  | "sliders"
  | "calendar"
  | "user"
  | "arrow-right"
  | "arrow-left"
  | "chevron-right"
  | "check"
  | "activity"
  | "flame"
  | "utensils"
  | "clock"
  | "sparkles"
  | "alert"
  | "refresh"
  | "target"
  | "chef"
  | "plus"
  | "minus"
  | "info"
  | "x"
  | "home"
  | "log-out"
  | "edit"
  | "bell"
  | "scale";

const paths: Record<IconName, ReactNode> = {
  leaf: <><path d="M20 4c-8 0-14 4-14 11a5 5 0 0 0 5 5c7 0 11-6 9-16Z"/><path d="M4 20c3-5 7-8 13-11"/></>,
  heart: <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>,
  "heart-pulse": <><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6"/><path d="M3 12h4l2-3 3 6 2-3h5"/></>,
  sliders: <><path d="M4 21v-7"/><path d="M4 10V3"/><path d="M12 21v-9"/><path d="M12 8V3"/><path d="M20 21v-5"/><path d="M20 12V3"/><path d="M2 14h4"/><path d="M10 8h4"/><path d="M18 16h4"/></>,
  calendar: <><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></>,
  user: <><circle cx="12" cy="8" r="4"/><path d="M5 21v-2a7 7 0 0 1 14 0v2"/></>,
  "arrow-right": <><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></>,
  "arrow-left": <><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></>,
  "chevron-right": <path d="m9 18 6-6-6-6"/>,
  check: <path d="m5 12 4 4L19 6"/>,
  activity: <><path d="M22 12h-4l-3 8-6-16-3 8H2"/></>,
  flame: <path d="M12 22c4.4 0 7-3.1 7-7 0-3-1.5-5.2-4-7-.2 2-1.2 3-2 3-1-3-2.5-5-4-7-1 4-4 6.5-4 11 0 4 2.7 7 7 7Z"/>,
  utensils: <><path d="M7 3v7M4 3v4a3 3 0 0 0 6 0V3M7 10v11"/><path d="M17 3v18M17 3c3 2 3 7 0 9"/></>,
  clock: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
  sparkles: <><path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z"/><path d="m19 14 .9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9L19 14Z"/></>,
  alert: <><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></>,
  refresh: <><path d="M20 7v5h-5"/><path d="M4 17v-5h5"/><path d="M5.6 9a7 7 0 0 1 11.6-2L20 12M4 12l2.8 5a7 7 0 0 0 11.6-2"/></>,
  target: <><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></>,
  chef: <><path d="M6 13a4 4 0 1 1 1-7.9A5 5 0 0 1 17 7a3.5 3.5 0 0 1 1 6.9V20H6v-7Z"/><path d="M6 16h12"/></>,
  plus: <><path d="M12 5v14M5 12h14"/></>,
  minus: <path d="M5 12h14"/>,
  info: <><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></>,
  x: <><path d="m18 6-12 12M6 6l12 12"/></>,
  home: <><path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1V10Z"/></>,
  "log-out": <><path d="M10 17l5-5-5-5M15 12H3"/><path d="M12 3h6a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-6"/></>,
  edit: <><path d="m16 4 4 4M4 20l4-.8L19 8a2.8 2.8 0 0 0-4-4L4 15l0 5Z"/></>,
  bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4"/></>,
  scale: <><path d="M12 3v18M5 6h14M7 6l-3 6h6L7 6ZM17 6l-3 6h6l-3-6ZM5 21h14"/></>
};

export function Icon({
  name,
  size = 20,
  className = ""
}: {
  name: IconName;
  size?: number;
  className?: string;
}) {
  return (
    <svg
      aria-hidden="true"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {paths[name]}
    </svg>
  );
}
