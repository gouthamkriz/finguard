import { useCallback, useEffect, useState } from "react";
import { AppShell, type Page } from "./components/AppShell";
import { api } from "./services/api";
import type { HealthResponse } from "./types/api";
import { DashboardPage } from "./pages/DashboardPage";
import { SearchPage } from "./pages/SearchPage";
import { InvestigationsPage } from "./pages/InvestigationsPage";

export default function App() {
  const [page, setPage] = useState<Page>("dashboard");
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthState, setHealthState] = useState<"checking" | "connected" | "unavailable">("checking");
  const refreshHealth = useCallback(async () => { setHealthState("checking"); try { setHealth(await api.getHealth()); setHealthState("connected"); } catch { setHealth(null); setHealthState("unavailable"); } }, []);
  useEffect(() => { void refreshHealth(); }, [refreshHealth]);
  return <AppShell page={page} setPage={setPage} healthState={healthState} health={health} refreshHealth={() => void refreshHealth()}>{page === "dashboard" ? <DashboardPage /> : page === "search" ? <SearchPage /> : <InvestigationsPage />}</AppShell>;
}
