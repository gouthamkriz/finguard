import { useCallback, useEffect, useMemo, useState } from "react";
import { Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AppShell, type Page } from "./components/AppShell";
import { api } from "./services/api";
import type { HealthResponse } from "./types/api";
import { DashboardPage } from "./pages/DashboardPage";
import { SearchPage } from "./pages/SearchPage";
import { InvestigationsPage } from "./pages/InvestigationsPage";

const pageFromPath = (pathname: string): Page => {
  if (pathname === "/search") return "search";
  if (pathname === "/investigations") return "investigations";
  return "dashboard";
};

export default function App() {
  const location = useLocation();
  const navigate = useNavigate();
  const currentPage = useMemo(() => pageFromPath(location.pathname), [location.pathname]);
  const [investigationEntityId, setInvestigationEntityId] = useState("ACC-101");
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthState, setHealthState] = useState<"checking" | "connected" | "unavailable">("checking");

  const refreshHealth = useCallback(async () => { setHealthState("checking"); try { setHealth(await api.getHealth()); setHealthState("connected"); } catch { setHealth(null); setHealthState("unavailable"); } }, []);
  useEffect(() => { void refreshHealth(); }, [refreshHealth]);

  useEffect(() => {
    const handleNavigation = (event: Event) => {
      const message = event as CustomEvent<{ page: Page }>;
      if (message.detail?.page) {
        const nextPath = message.detail.page === "dashboard" ? "/" : `/${message.detail.page}`;
        navigate(nextPath, { replace: false });
      }
    };
    window.addEventListener("finGuardNavigate", handleNavigation);
    return () => window.removeEventListener("finGuardNavigate", handleNavigation);
  }, [navigate]);

  useEffect(() => {
    const expectedPath = currentPage === "dashboard" ? "/" : `/${currentPage}`;
    if (location.pathname !== expectedPath) {
      navigate(expectedPath, { replace: true });
    }
  }, [currentPage, location.pathname, navigate]);

  const openInvestigation = useCallback((entityId: string) => {
    const cleanValue = entityId.trim();
    if (!cleanValue) { return; }
    setInvestigationEntityId(cleanValue);
    navigate("/investigations", { replace: false });
  }, [navigate]);

  const handleSetPage = useCallback((page: Page) => {
    const nextPath = page === "dashboard" ? "/" : `/${page}`;
    navigate(nextPath, { replace: false });
  }, [navigate]);

  return <AppShell page={currentPage} setPage={handleSetPage} healthState={healthState} health={health} refreshHealth={() => void refreshHealth()}>{<Routes>
    <Route path="/" element={<DashboardPage />} />
    <Route path="/search" element={<SearchPage onOpenInvestigation={openInvestigation} />} />
    <Route path="/investigations" element={<InvestigationsPage initialEntityId={investigationEntityId} onEntityIdChange={setInvestigationEntityId} />} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>}</AppShell>;
}
