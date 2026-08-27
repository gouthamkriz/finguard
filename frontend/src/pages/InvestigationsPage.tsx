import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api, ApiError } from "../services/api";
import { EmptyState, ErrorState, LoadingState } from "../components/States";
import { ResultViewer } from "../components/ResultViewer";
import { GraphCanvas } from "../components/GraphCanvas";

type InvestigationId = "sharedDevice" | "sharedIP" | "circularTransfers" | "shortestPath" | "highRiskMerchants" | "blastRadius" | "syntheticIdentity";
interface InvestigationDefinition { id: InvestigationId; title: string; description: string; fields: Array<{ name: string; label: string; placeholder?: string; type?: "text" | "number"; optional?: boolean; min?: number; max?: number }> }

const definitions: InvestigationDefinition[] = [
  { id: "sharedDevice", title: "Shared Device", description: "Find customer profiles connected to one device.", fields: [{ name: "deviceId", label: "Device ID", placeholder: "Example: DEV-909" }] },
  { id: "sharedIP", title: "Shared IP Address", description: "Find customer profiles using one IPv4 address.", fields: [{ name: "ipAddress", label: "IPv4 address", placeholder: "Example: 192.0.2.45" }] },
  { id: "circularTransfers", title: "Circular Transfer", description: "Detect the approved three-account transfer cycle.", fields: [{ name: "accountNumber", label: "Account number", placeholder: "Example: ACC-101" }] },
  { id: "shortestPath", title: "Shortest Path", description: "Find a bounded transfer path between accounts.", fields: [{ name: "sourceAccount", label: "Source account", placeholder: "Example: ACC-101" }, { name: "targetAccount", label: "Target account", placeholder: "Example: ACC-303" }, { name: "maxHops", label: "Maximum hops", type: "number", min: 1, max: 4 }] },
  { id: "highRiskMerchants", title: "High-Risk Merchant Exposure", description: "List exposure to HIGH-risk merchants; a merchant filter is optional.", fields: [{ name: "merchantId", label: "Merchant ID", placeholder: "Example: MERCH-99", optional: true }] },
  { id: "blastRadius", title: "Device Blast Radius", description: "Measure bounded impact from a compromised device.", fields: [{ name: "deviceId", label: "Device ID", placeholder: "Example: DEV-101" }, { name: "maxHops", label: "Maximum hops", type: "number", min: 1, max: 3 }] },
  { id: "syntheticIdentity", title: "Synthetic Identity", description: "Identify shared device and proxy infrastructure linked to HIGH-risk merchant payments.", fields: [{ name: "deviceId", label: "Device ID", placeholder: "Example: DEV-101" }, { name: "ipAddress", label: "Proxy IPv4 address", placeholder: "Example: 192.0.2.45" }] },
];

const validServiceValues = new Set(definitions.map((definition) => definition.id));
const serviceValueMap: Record<string, InvestigationId> = {
  "shared-device": "sharedDevice",
  "shared-ip": "sharedIP",
  "circular-transfers": "circularTransfers",
  "shortest-path": "shortestPath",
  "high-risk-merchants": "highRiskMerchants",
  "blast-radius": "blastRadius",
  "synthetic-identity": "syntheticIdentity",
};

function serviceIdToParam(value: InvestigationId): string {
  return {
    sharedDevice: "shared-device",
    sharedIP: "shared-ip",
    circularTransfers: "circular-transfers",
    shortestPath: "shortest-path",
    highRiskMerchants: "high-risk-merchants",
    blastRadius: "blast-radius",
    syntheticIdentity: "synthetic-identity",
  }[value];
}

function resolveServiceFromParam(service: string | null): InvestigationId {
  if (!service) return "sharedDevice";
  const normalized = service.trim().toLowerCase();
  return serviceValueMap[normalized] ?? "sharedDevice";
}

function validIPv4(value: string): boolean { const segments = value.split("."); return segments.length === 4 && segments.every((segment) => /^\d+$/.test(segment) && Number(segment) >= 0 && Number(segment) <= 255); }

function summarizeInvestigation(result: unknown): Array<{ label: string; value: string }> {
  if (!result || typeof result !== "object") return [];
  const obj = result as Record<string, unknown>;

  if ("deviceId" in obj && "connectedCustomers" in obj) {
    const customers = Array.isArray(obj.connectedCustomers) ? obj.connectedCustomers as Array<Record<string, unknown>> : [];
    return [
      { label: "Entity", value: String(obj.deviceId) },
      { label: "Customers linked", value: `${customers.length}` },
      { label: "Device type", value: obj.deviceType ? String(obj.deviceType) : "Unavailable" },
    ];
  }

  if ("ipAddress" in obj && "connectedCustomers" in obj) {
    const customers = Array.isArray(obj.connectedCustomers) ? obj.connectedCustomers as Array<Record<string, unknown>> : [];
    return [
      { label: "IP address", value: String(obj.ipAddress) },
      { label: "Customers linked", value: `${customers.length}` },
      { label: "Proxy status", value: obj.isProxy !== undefined ? String(obj.isProxy) : "Unavailable" },
    ];
  }

  if ("cycleLength" in obj && "transactionChain" in obj) {
    const chain = Array.isArray(obj.transactionChain) ? obj.transactionChain as Array<Record<string, unknown>> : [];
    const source = obj.sourceAccount ? String(obj.sourceAccount) : "Unknown";
    return [
      { label: "Cycle", value: `${obj.cycleLength ?? "n/a"}-account transfer loop` },
      { label: "Origin", value: source },
      { label: "Transactions", value: `${chain.length}` },
    ];
  }

  if ("accountChain" in obj && "totalHops" in obj) {
    const chain = Array.isArray(obj.accountChain) ? obj.accountChain : [];
    return [
      { label: "Path", value: chain.length ? chain.join(" → ") : "No path available" },
      { label: "Hop count", value: String(obj.totalHops ?? 0) },
    ];
  }

  if (Array.isArray(obj)) {
    return [{ label: "Results", value: `${obj.length} matching records` }];
  }

  if ("matchedCustomerCount" in obj && "riskRating" in obj) {
    return [
      { label: "Matched customers", value: String(obj.matchedCustomerCount ?? 0) },
      { label: "Merchant", value: obj.merchantId ? String(obj.merchantId) : "Unavailable" },
      { label: "Risk rating", value: obj.riskRating ? String(obj.riskRating) : "Unavailable" },
    ];
  }

  if ("deviceId" in obj && "totalImpactedEntities" in obj) {
    return [
      { label: "Device", value: String(obj.deviceId) },
      { label: "Impacted entities", value: String(obj.totalImpactedEntities ?? 0) },
      { label: "Max depth", value: String(obj.maxDepthReached ?? 0) },
    ];
  }

  return Object.entries(obj).slice(0, 3).map(([key, value]) => ({ label: key, value: typeof value === "string" ? value : Array.isArray(value) ? `${value.length} items` : String(value) }));
}

export function InvestigationsPage({ initialEntityId = "ACC-101", onEntityIdChange }: { initialEntityId?: string; onEntityIdChange?: (entityId: string) => void }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [selected, setSelected] = useState<InvestigationId>(() => resolveServiceFromParam(searchParams.get("service")));
  const [values, setValues] = useState<Record<string, string>>({ deviceId: "DEV-909" });
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const current = definitions.find((definition) => definition.id === selected)!;

  useEffect(() => {
    const requestedService = resolveServiceFromParam(searchParams.get("service"));
    if (!validServiceValues.has(requestedService)) {
      setSearchParams({ service: serviceIdToParam("sharedDevice") }, { replace: true });
      return;
    }
    setSelected(requestedService);
  }, [searchParams, setSearchParams]);

  useEffect(() => {
    if (initialEntityId && initialEntityId.trim()) {
      const entityId = initialEntityId.trim();
      setValues((prev) => ({ ...prev, deviceId: entityId.startsWith("DEV") ? entityId : prev.deviceId, accountNumber: entityId.startsWith("ACC") ? entityId : prev.accountNumber, ipAddress: entityId.includes(".") ? entityId : prev.ipAddress, merchantId: entityId.startsWith("MERCH") ? entityId : prev.merchantId }));
    }
  }, [initialEntityId]);

  const summary = useMemo(() => summarizeInvestigation(result), [result]);

  function select(id: InvestigationId) {
    setSelected(id);
    setSearchParams({ service: serviceIdToParam(id) }, { replace: false });
    setValues({});
    setResult(null);
    setError(null);
  }
  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const required = current.fields.filter((field) => !field.optional);
    if (required.some((field) => !values[field.name]?.trim())) { setError("Complete all required fields before running this investigation."); return; }
    if (values.ipAddress && !validIPv4(values.ipAddress.trim())) { setError("Enter a valid IPv4 address."); return; }
    const hops = Number(values.maxHops);
    const hopField = current.fields.find((field) => field.name === "maxHops");
    if (hopField && (!Number.isInteger(hops) || hops < (hopField.min ?? 1) || hops > (hopField.max ?? 4))) { setError(`Maximum hops must be between ${hopField.min} and ${hopField.max}.`); return; }
    setLoading(true); setError(null); setResult(null);
    try {
      const value = values;
      const response = selected === "sharedDevice" ? await api.sharedDevice(value.deviceId.trim()) : selected === "sharedIP" ? await api.sharedIP(value.ipAddress.trim()) : selected === "circularTransfers" ? await api.circularTransfers(value.accountNumber.trim()) : selected === "shortestPath" ? await api.shortestPath(value.sourceAccount.trim(), value.targetAccount.trim(), hops) : selected === "highRiskMerchants" ? await api.highRiskMerchants(value.merchantId?.trim()) : selected === "blastRadius" ? await api.blastRadius(value.deviceId.trim(), hops) : await api.syntheticIdentity(value.deviceId.trim(), value.ipAddress.trim());
      setResult(response);
      if (selected === "sharedDevice" && typeof value.deviceId === "string") { onEntityIdChange?.(value.deviceId.trim()); }
      if (selected === "sharedIP" && typeof value.ipAddress === "string") { onEntityIdChange?.(value.ipAddress.trim()); }
      if (selected === "circularTransfers" && typeof value.accountNumber === "string") { onEntityIdChange?.(value.accountNumber.trim()); }
      if (selected === "blastRadius" && typeof value.deviceId === "string") { onEntityIdChange?.(value.deviceId.trim()); }
      if (selected === "syntheticIdentity" && typeof value.deviceId === "string") { onEntityIdChange?.(value.deviceId.trim()); }
    } catch (requestError) { setError(requestError instanceof ApiError ? requestError.message : "Unable to complete the investigation."); } finally { setLoading(false); }
  }

  return <div className="investigation-layout"><aside className="investigation-list" aria-label="Investigation types">{definitions.map((definition) => <button key={definition.id} type="button" onClick={() => select(definition.id)} className={selected === definition.id ? "investigation-choice active" : "investigation-choice"}><strong>{definition.title}</strong><span>{definition.description}</span></button>)}</aside><div className="page-stack"><section className="panel"><h2>{current.title}</h2><p>{current.description}</p><form className="investigation-form" onSubmit={submit}>{current.fields.map((field) => <label key={field.name}>{field.label}{field.optional && <span className="optional">Optional</span>}<input type={field.type ?? "text"} value={values[field.name] ?? ""} placeholder={field.placeholder} min={field.min} max={field.max} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })} required={!field.optional} /></label>)}<button type="submit" className="button" disabled={loading}>{loading ? "Running…" : "Run investigation"}</button></form></section>{loading && <LoadingState label="Running investigation against the FinGuard API…" />}{error && <ErrorState message={error} />}{result !== null && !loading && (Array.isArray(result) && result.length === 0 ? <EmptyState>No matching investigation evidence was found.</EmptyState> : <section className="panel result-panel"><h2>Investigation evidence</h2>{summary.length > 0 && <div className="evidence-summary" aria-live="polite">{summary.map((item) => <div key={`${item.label}-${item.value}`} className="summary-pill"><span>{item.label}</span><strong>{item.value}</strong></div>)}</div>}{Array.isArray(result) ? <div className="result-grid">{result.map((item, index) => <article className="result-card" key={index}><ResultViewer data={item as Record<string, unknown>} /></article>)}</div> : <ResultViewer data={result as Record<string, unknown>} />}</section>)}{result === null && !loading && !error && <EmptyState>Provide investigation parameters to retrieve live results.</EmptyState>}<section className="panel"><h2>Interactive graph</h2><p>Use the approved neighborhood API to inspect the one-hop graph around a selected entity.</p><GraphCanvas initialEntityId={initialEntityId} /></section></div></div>;
}
