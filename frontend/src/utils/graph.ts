export type CanonicalEntityType = "Customer" | "Account" | "Device" | "IPAddress" | "Merchant";

export interface NeighborhoodRelationship {
  sourceType: string;
  sourceId: string;
  relationshipType: string;
  relProps: Record<string, unknown>;
  targetType: string;
  targetId: string;
}

export interface GraphNodeData {
  id: string;
  label: string;
  entityType: CanonicalEntityType;
  metadata?: Record<string, unknown>;
}

export interface GraphEdgeData {
  id: string;
  source: string;
  target: string;
  relationshipType: string;
  metadata: Record<string, unknown>;
}

export interface GraphData {
  nodes: GraphNodeData[];
  edges: GraphEdgeData[];
}

const ENTITY_TYPE_LABELS: Record<string, CanonicalEntityType> = {
  customer: "Customer",
  account: "Account",
  device: "Device",
  ipaddress: "IPAddress",
  ip: "IPAddress",
  merchant: "Merchant",
};

export function canonicalizeEntityType(value: string): CanonicalEntityType {
  const normalized = String(value ?? "").trim().toLowerCase();
  return ENTITY_TYPE_LABELS[normalized] ?? "Customer";
}

export function normalizeNeighborhoodGraph(relationships: NeighborhoodRelationship[]): GraphData {
  const nodesById = new Map<string, GraphNodeData>();
  const edges: GraphEdgeData[] = [];

  relationships.forEach((relationship) => {
    const sourceType = canonicalizeEntityType(relationship.sourceType);
    const targetType = canonicalizeEntityType(relationship.targetType);
    const sourceNode: GraphNodeData = {
      id: relationship.sourceId,
      label: relationship.sourceId,
      entityType: sourceType,
      metadata: { sourceType },
    };
    const targetNode: GraphNodeData = {
      id: relationship.targetId,
      label: relationship.targetId,
      entityType: targetType,
      metadata: { sourceType: targetType },
    };

    nodesById.set(sourceNode.id, sourceNode);
    nodesById.set(targetNode.id, targetNode);

    const metadata = Object.fromEntries(
      Object.entries(relationship.relProps ?? {}).filter(([, value]) => value !== null && value !== undefined)
    );

    edges.push({
      id: `${relationship.sourceId}:${relationship.relationshipType}:${relationship.targetId}`,
      source: relationship.sourceId,
      target: relationship.targetId,
      relationshipType: relationship.relationshipType,
      metadata,
    });
  });

  return {
    nodes: Array.from(nodesById.values()),
    edges,
  };
}
