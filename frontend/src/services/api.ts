import type {
  ApiErrorPayload,
  BlastRadiusResponse,
  CircularTransferResponse,
  EntitySearchResult,
  EntityType,
  HealthResponse,
  HighRiskMerchantExposure,
  NeighborhoodEdge,
  SharedDeviceResponse,
  SharedIPResponse,
  ShortestPathResponse,
  SyntheticIdentityResponse,
} from "../types/api";

const API_BASE_URL = (import.meta.env.VITE_API_URL ?? import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

export class ApiError extends Error {
  constructor(public readonly status: number, public readonly code: string, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

function queryString(params: Record<string, string | number | undefined>): string {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") query.set(key, String(value));
  });
  const serialized = query.toString();
  return serialized ? `?${serialized}` : "";
}

async function get<T>(path: string, params: Record<string, string | number | undefined> = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}${queryString(params)}`, { headers: { Accept: "application/json" } });
  } catch {
    throw new ApiError(0, "NETWORK_ERROR", "Unable to reach the FinGuard API. Check that the backend is running.");
  }

  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const error = payload as ApiErrorPayload | null;
    throw new ApiError(response.status, error?.error?.code ?? "HTTP_ERROR", error?.error?.message ?? "The investigation service returned an unexpected response.");
  }
  return payload as T;
}

export const api = {
  getHealth: () => get<HealthResponse>("/health"),
  search: (q: string, type?: EntityType) => get<EntitySearchResult[]>("/api/v1/search", { q, type }),
  sharedDevice: (deviceId: string) => get<SharedDeviceResponse>("/api/v1/investigations/shared-device", { deviceId }),
  sharedIP: (ipAddress: string) => get<SharedIPResponse>("/api/v1/investigations/shared-ip", { ipAddress }),
  circularTransfers: (accountNumber: string) => get<CircularTransferResponse>("/api/v1/investigations/circular-transfers", { accountNumber }),
  shortestPath: (sourceAccount: string, targetAccount: string, maxHops: number) => get<ShortestPathResponse>("/api/v1/investigations/shortest-path", { sourceAccount, targetAccount, maxHops }),
  highRiskMerchants: (merchantId?: string) => get<HighRiskMerchantExposure[]>("/api/v1/investigations/high-risk-merchants", { merchantId }),
  blastRadius: (deviceId: string, maxHops: number) => get<BlastRadiusResponse>("/api/v1/investigations/blast-radius", { deviceId, maxHops }),
  syntheticIdentity: (deviceId: string, ipAddress: string) => get<SyntheticIdentityResponse>("/api/v1/investigations/synthetic-identity", { deviceId, ipAddress }),
  neighborhood: (entityId: string) => get<NeighborhoodEdge[]>("/api/v1/neighborhood", { entityId }),
};
