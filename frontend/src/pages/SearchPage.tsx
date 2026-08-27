import { useState } from "react";
import { api, ApiError } from "../services/api";
import type { EntitySearchResult, EntityType } from "../types/api";
import { EmptyState, ErrorState, LoadingState } from "../components/States";
import { ResultViewer } from "../components/ResultViewer";

const entityTypes: EntityType[] = ["Customer", "Account", "Device", "IPAddress", "Merchant"];

export function SearchPage({ onOpenInvestigation }: { onOpenInvestigation?: (entityId: string) => void }) {
  const [term, setTerm] = useState("");
  const [entityType, setEntityType] = useState<EntityType | "">("");
  const [results, setResults] = useState<EntitySearchResult[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const query = term.trim();
    if (!query) { setError("Enter a search term before starting an investigation."); return; }
    setLoading(true); setError(null); setResults(null);
    try { setResults(await api.search(query, entityType || undefined)); } catch (requestError) { setError(requestError instanceof ApiError ? requestError.message : "Unable to complete the search."); } finally { setLoading(false); }
  }

  return <div className="page-stack"><section className="panel"><div className="panel-heading"><div><h2>Entity search</h2><p>Search by customer ID, account number, device ID, IP address, or merchant name. Results are returned directly from the live FinGuard API.</p></div></div><form className="search-form" onSubmit={submit}><label>Search term<input value={term} onChange={(event) => setTerm(event.target.value)} maxLength={256} placeholder="e.g. Alice, ACC-101, DEV-909, 192.0.2.45" /></label><label>Entity type<select value={entityType} onChange={(event) => setEntityType(event.target.value as EntityType | "")}><option value="">All supported entities</option>{entityTypes.map((type) => <option key={type} value={type}>{type}</option>)}</select></label><button className="button" type="submit" disabled={loading}>{loading ? "Searching…" : "Search entities"}</button></form></section>{loading && <LoadingState label="Searching the FinGuard graph…" />}{error && <ErrorState message={error} />}{results && !loading && results.length === 0 && <EmptyState>No matching entities found. Try another identifier or search term.</EmptyState>}{results && results.length > 0 && <section className="result-grid" aria-label="Search results">{results.map((result) => <article className="result-card" key={`${result.entityType}-${result.id}`}><header><span className="tag">{result.entityType}</span><h3>{result.id}</h3></header><ResultViewer data={result as unknown as Record<string, unknown>} /><div className="card-actions"><button type="button" className="button secondary" onClick={() => onOpenInvestigation?.(result.id)}>Open in graph</button></div></article>)}</section>}</div>;
}
