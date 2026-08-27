import type { ReactNode } from "react";

function renderValue(value: unknown): ReactNode {
  if (Array.isArray(value)) {
    return <ul>{value.map((item, index) => <li key={index}>{typeof item === "object" && item !== null ? <ResultViewer data={item as Record<string, unknown>} compact /> : String(item)}</li>)}</ul>;
  }
  if (value !== null && typeof value === "object") {
    return <ResultViewer data={value as Record<string, unknown>} compact />;
  }
  return String(value);
}

export function ResultViewer({ data, compact = false }: { data: Record<string, unknown>; compact?: boolean }) {
  return <dl className={compact ? "result-detail compact" : "result-detail"}>{Object.entries(data).filter(([, value]) => value !== null && value !== undefined).map(([key, value]) => <div key={key}><dt>{key}</dt><dd>{renderValue(value)}</dd></div>)}</dl>;
}
