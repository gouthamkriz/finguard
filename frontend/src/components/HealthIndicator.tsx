import type { HealthResponse } from "../types/api";

type HealthState = "checking" | "connected" | "unavailable";

export function HealthIndicator({ state, health, onRefresh }: { state: HealthState; health: HealthResponse | null; onRefresh: () => void }) {
  const label = state === "checking" ? "Checking systems" : state === "connected" && health ? "API & database connected" : "API unavailable";
  return <button type="button" className={`health health-${state}`} onClick={onRefresh} aria-label={`${label}. Refresh health status.`}><span aria-hidden="true" className="health-dot" />{label}</button>;
}
