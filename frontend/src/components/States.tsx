import type { ReactNode } from "react";

export function LoadingState({ label = "Loading investigation data…" }: { label?: string }) {
  return <div className="state state-loading" role="status"><span className="spinner" aria-hidden="true" />{label}</div>;
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return <div className="state state-error" role="alert"><strong>Request unavailable</strong><span>{message}</span>{onRetry && <button type="button" className="button secondary" onClick={onRetry}>Try again</button>}</div>;
}

export function EmptyState({ children }: { children: ReactNode }) {
  return <div className="state state-empty">{children}</div>;
}
