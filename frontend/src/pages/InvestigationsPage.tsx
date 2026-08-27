import { useState } from "react";
import { api, ApiError } from "../services/api";
import { EmptyState, ErrorState, LoadingState } from "../components/States";
import { ResultViewer } from "../components/ResultViewer";

type InvestigationId = "sharedDevice" | "sharedIP" | "circularTransfers" | "shortestPath" | "highRiskMerchants" | "blastRadius" | "syntheticIdentity";
interface InvestigationDefinition { id: InvestigationId; title: string; description: string; fields: Array<{ name: string; label: string; placeholder?: string; type?: "text" | "number"; optional?: boolean; min?: number; max?: number }> }

const definitions: InvestigationDefinition[] = [
  { id: "sharedDevice", title: "Shared Device", description: "Find customer profiles connected to one device.", fields: [{ name: "deviceId", label: "Device ID", placeholder: "DEV-909" }] },
  { id: "sharedIP", title: "Shared IP", description: "Find customer profiles using one IPv4 address.", fields: [{ name: "ipAddress", label: "IPv4 address", placeholder: "192.0.2.45" }] },
  { id: "circularTransfers", title: "Circular Transfers", description: "Detect the approved three-account transfer cycle.", fields: [{ name: "accountNumber", label: "Account number", placeholder: "ACC-101" }] },
  { id: "shortestPath", title: "Shortest Path", description: "Find a bounded transfer path between accounts.", fields: [{ name: "sourceAccount", label: "Source account", placeholder: "ACC-101" }, { name: "targetAccount", label: "Target account", placeholder: "ACC-303" }, { name: "maxHops", label: "Maximum hops", type: "number", min: 1, max: 4 }] },
  { id: "highRiskMerchants", title: "High-Risk Merchant Exposure", description: "List exposure to HIGH-risk merchants; a merchant filter is optional.", fields: [{ name: "merchantId", label: "Merchant ID", placeholder: "MERCH-99", optional: true }] },
  { id: "blastRadius", title: "Blast Radius", description: "Measure bounded impact from a compromised device.", fields: [{ name: "deviceId", label: "Device ID", placeholder: "DEV-101" }, { name: "maxHops", label: "Maximum hops", type: "number", min: 1, max: 3 }] },
  { id: "syntheticIdentity", title: "Synthetic Identity", description: "Identify shared device and proxy infrastructure linked to HIGH-risk merchant payments.", fields: [{ name: "deviceId", label: "Device ID", placeholder: "DEV-101" }, { name: "ipAddress", label: "Proxy IPv4 address", placeholder: "192.0.2.45" }] },
];

function validIPv4(value: string): boolean { const segments = value.split("."); return segments.length === 4 && segments.every((segment) => /^\d+$/.test(segment) && Number(segment) >= 0 && Number(segment) <= 255); }

export function InvestigationsPage() {
  const [selected, setSelected] = useState<InvestigationId>("sharedDevice");
  const [values, setValues] = useState<Record<string, string>>({ deviceId: "DEV-909" });
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const current = definitions.find((definition) => definition.id === selected)!;

  function select(id: InvestigationId) { setSelected(id); setValues({}); setResult(null); setError(null); }
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
    } catch (requestError) { setError(requestError instanceof ApiError ? requestError.message : "Unable to complete the investigation."); } finally { setLoading(false); }
  }

  return <div className="investigation-layout"><aside className="investigation-list" aria-label="Investigation types">{definitions.map((definition) => <button key={definition.id} type="button" onClick={() => select(definition.id)} className={selected === definition.id ? "investigation-choice active" : "investigation-choice"}><strong>{definition.title}</strong><span>{definition.description}</span></button>)}</aside><div className="page-stack"><section className="panel"><h2>{current.title}</h2><p>{current.description}</p><form className="investigation-form" onSubmit={submit}>{current.fields.map((field) => <label key={field.name}>{field.label}{field.optional && <span className="optional">Optional</span>}<input type={field.type ?? "text"} value={values[field.name] ?? ""} placeholder={field.placeholder} min={field.min} max={field.max} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })} required={!field.optional} /></label>)}<button type="submit" className="button" disabled={loading}>{loading ? "Running…" : "Run investigation"}</button></form></section>{loading && <LoadingState label="Running investigation against the FinGuard API…" />}{error && <ErrorState message={error} />}{result !== null && !loading && (Array.isArray(result) && result.length === 0 ? <EmptyState>No matching investigation results found.</EmptyState> : <section className="panel result-panel"><h2>Investigation result</h2>{Array.isArray(result) ? <div className="result-grid">{result.map((item, index) => <article className="result-card" key={index}><ResultViewer data={item as Record<string, unknown>} /></article>)}</div> : <ResultViewer data={result as Record<string, unknown>} />}</section>)}{result === null && !loading && !error && <EmptyState>Provide investigation parameters to retrieve live results.</EmptyState>}</div></div>;
}
