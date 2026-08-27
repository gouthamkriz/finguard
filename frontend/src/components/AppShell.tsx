import type { ReactNode } from "react";
import { HealthIndicator } from "./HealthIndicator";
import type { HealthResponse } from "../types/api";

export type Page = "dashboard" | "search" | "investigations";

const navigation: Array<{ id: Page; label: string; detail: string }> = [
  { id: "dashboard", label: "Dashboard", detail: "System readiness" },
  { id: "search", label: "Search", detail: "Entity lookup" },
  { id: "investigations", label: "Investigations", detail: "Relationship analysis" },
];

export function AppShell({ page, setPage, children, healthState, health, refreshHealth }: { page: Page; setPage: (page: Page) => void; children: ReactNode; healthState: "checking" | "connected" | "unavailable"; health: HealthResponse | null; refreshHealth: () => void }) {
  return <div className="app-shell"><aside className="sidebar"><div className="brand"><span className="brand-mark">F</span><div><strong>FinGuard</strong><small>Investigation Console</small></div></div><nav aria-label="Primary navigation">{navigation.map((item) => <button type="button" key={item.id} className={page === item.id ? "nav-item active" : "nav-item"} onClick={() => setPage(item.id)}><strong>{item.label}</strong><small>{item.detail}</small></button>)}</nav><p className="sidebar-note">Connected through the FinGuard REST API. Graph visualization arrives in Stage 10.</p></aside><main><header className="topbar"><div><p className="eyebrow">FINANCIAL CRIME INTELLIGENCE</p><h1>{navigation.find((item) => item.id === page)?.label}</h1></div><HealthIndicator state={healthState} health={health} onRefresh={refreshHealth} /></header><section className="page-content">{children}</section></main></div>;
}
