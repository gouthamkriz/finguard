export type EntityType = "Customer" | "Account" | "Device" | "IPAddress" | "Merchant";

export interface ApiErrorPayload {
  error: {
    code: "VALIDATION_ERROR" | "NOT_FOUND" | "DATABASE_UNAVAILABLE" | "QUERY_FAILED" | string;
    message: string;
  };
}

export interface HealthResponse {
  status: "ok";
  database: "connected";
}

export interface EntitySearchResult {
  id: string;
  entityType: EntityType;
  name?: string;
  riskLevel?: string;
  createdDate?: string;
  accountType?: string;
  status?: string;
  balance?: number;
  deviceType?: string;
  os?: string;
  isProxy?: boolean;
  category?: string;
  riskRating?: string;
}

export interface SharedDeviceResponse {
  deviceId: string;
  deviceType: string;
  os: string;
  connectedCustomers: Array<{ customerId: string; name: string; riskLevel: string; lastUsed?: string; accountNumber?: string }>;
}

export interface SharedIPResponse {
  ipAddress: string;
  isProxy: boolean;
  connectedCustomers: Array<{ customerId: string; name: string; riskLevel: string; lastLogin?: string; loginCount?: number }>;
}

export interface TransactionItem { txId: string; amount: number; timestamp: string }

export interface CircularTransferResponse {
  sourceAccount: string;
  hop1Account: string;
  hop2Account: string;
  transactionChain: TransactionItem[];
  cycleLength: number;
}

export interface ShortestPathResponse { accountChain: string[]; transactionChain: TransactionItem[]; totalHops: number }

export interface HighRiskMerchantExposure {
  merchantId: string;
  merchantName: string;
  riskRating: string;
  accountNumber: string;
  customerId: string;
  customerName: string;
  paymentAmount: number;
  paymentTimestamp: string;
}

export interface BlastRadiusResponse {
  deviceId: string;
  connectedEntityTypes: string[];
  connectedEntityIds: string[];
  totalImpactedEntities: number;
  maxDepthReached: number;
}

export interface SyntheticIdentityResponse {
  sharedDevice: string;
  sharedIP: string;
  isProxy: boolean;
  merchantId: string;
  targetMerchant: string;
  riskRating: string;
  matchedCustomerCount: number;
  clusterMembers: Array<{ customerId: string; customerName: string; accountNumber: string; paymentAmount: number; paymentTimestamp: string }>;
}

export interface NeighborhoodEdge {
  sourceType: string;
  sourceId: string;
  relationshipType: string;
  relProps: Record<string, unknown>;
  targetType: string;
  targetId: string;
}
