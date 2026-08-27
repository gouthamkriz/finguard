import { useEffect, useMemo, useRef, useState } from "react";
import cytoscape from "cytoscape";
import { api, ApiError } from "../services/api";
import { EmptyState, ErrorState, LoadingState } from "./States";
import type { EntitySearchResult, EntityType, NeighborhoodEdge } from "../types/api";
import { normalizeNeighborhoodGraph, type GraphData } from "../utils/graph";

function getNodeStyle(entityType: string) {
  switch (entityType) {
    case "Customer":
      return { shape: "round-rectangle", borderWidth: 3, backgroundColor: "#8ad7ff", borderColor: "#1d4ed8" } as any;
    case "Account":
      return { shape: "round-rectangle", borderWidth: 3, backgroundColor: "#c4b5fd", borderColor: "#7c3aed" } as any;
    case "Device":
      return { shape: "hexagon", borderWidth: 3, backgroundColor: "#86efac", borderColor: "#15803d" } as any;
    case "IPAddress":
      return { shape: "ellipse", borderWidth: 3, backgroundColor: "#f9c74f", borderColor: "#a16207" } as any;
    case "Merchant":
      return { shape: "diamond", borderWidth: 3, backgroundColor: "#fda4af", borderColor: "#be123c" } as any;
    default:
      return { shape: "round-rectangle", borderWidth: 2, backgroundColor: "#cbd5e1", borderColor: "#64748b" } as any;
  }
}

function relationshipLabel(type: string) {
  const labels: Record<string, string> = {
    OWNS_ACCOUNT: "Owns account",
    USED_DEVICE: "Used device",
    LOGGED_IN_FROM: "Logged in from",
    TRANSFERRED_FUNDS: "Transferred funds",
    PAYMENT_TO: "Paid merchant",
  };
  return labels[type] ?? type;
}

export function GraphCanvas({ initialEntityId = "ACC-101" }: { initialEntityId?: string }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const graphRef = useRef<cytoscape.Core | null>(null);
  const [entityId, setEntityId] = useState(initialEntityId);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState<string | null>(null);
  const [nodeDetail, setNodeDetail] = useState<EntitySearchResult | null>(null);

  const selectedNode = useMemo(() => graphData?.nodes.find((node) => node.id === selectedNodeId) ?? null, [graphData, selectedNodeId]);
  const selectedEdge = useMemo(() => graphData?.edges.find((edge) => edge.id === selectedEdgeId) ?? null, [graphData, selectedEdgeId]);

  async function loadNeighborhood(nextEntityId: string) {
    const cleanValue = nextEntityId.trim();
    if (!cleanValue) {
      setError("Enter an entity identifier to load a graph neighborhood.");
      setGraphData(null);
      return;
    }

    setLoading(true);
    setError(null);
    setSelectedNodeId(null);
    setSelectedEdgeId(null);
    setNodeDetail(null);

    try {
      const response = await api.neighborhood(cleanValue);
      const normalized = normalizeNeighborhoodGraph(response);
      setGraphData(normalized);
      if (normalized.nodes.length === 0) {
        setError("No relationships found for this investigation.");
      }
    } catch (requestError) {
      setGraphData(null);
      setError(requestError instanceof ApiError ? requestError.message : "The graph could not be loaded from the API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setEntityId(initialEntityId);
    void loadNeighborhood(initialEntityId);
  }, [initialEntityId]);

  useEffect(() => {
    if (!graphData || !containerRef.current) {
      return;
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements: {
        nodes: graphData.nodes.map((node) => ({
          data: {
            id: node.id,
            label: node.label,
            entityType: node.entityType,
            ...node.metadata,
          },
        })),
        edges: graphData.edges.map((edge) => ({
          data: {
            id: edge.id,
            source: edge.source,
            target: edge.target,
            relationshipType: edge.relationshipType,
            ...edge.metadata,
          },
        })),
      },
      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            color: "#eaf2ff",
            "font-size": "11px",
            "font-weight": "700" as any,
            "text-wrap": "wrap",
            "text-max-width": "100px",
            "background-color": "#93c5fd",
            "border-width": 2,
            "border-color": "#1d4ed8",
            "width": 36,
            "height": 36,
            "overlay-padding": 8,
            "text-outline-color": "#08111f",
            "text-outline-width": 1,
            "padding": 8 as any,
          } as any,
        },
        {
          selector: "node[entityType = 'Customer']",
          style: getNodeStyle("Customer"),
        },
        {
          selector: "node[entityType = 'Account']",
          style: getNodeStyle("Account"),
        },
        {
          selector: "node[entityType = 'Device']",
          style: getNodeStyle("Device"),
        },
        {
          selector: "node[entityType = 'IPAddress']",
          style: getNodeStyle("IPAddress"),
        },
        {
          selector: "node[entityType = 'Merchant']",
          style: getNodeStyle("Merchant"),
        },
        {
          selector: "edge",
          style: {
            label: "data(relationshipType)",
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#94a3b8",
            "line-color": "#94a3b8",
            "line-style": "solid",
            "width": 2,
            "font-size": "10px",
            "color": "#dbeafe",
            "text-rotation": "autorotate",
            "text-margin-y": -8,
            "target-endpoint": "outside-to-node-or-label",
          },
        },
        {
          selector: "edge[relationshipType = 'OWNS_ACCOUNT']",
          style: { "line-color": "#8b5cf6", "target-arrow-color": "#8b5cf6" },
        },
        {
          selector: "edge[relationshipType = 'USED_DEVICE']",
          style: { "line-color": "#34d399", "target-arrow-color": "#34d399" },
        },
        {
          selector: "edge[relationshipType = 'LOGGED_IN_FROM']",
          style: { "line-color": "#60a5fa", "target-arrow-color": "#60a5fa" },
        },
        {
          selector: "edge[relationshipType = 'TRANSFERRED_FUNDS']",
          style: { "line-color": "#f59e0b", "target-arrow-color": "#f59e0b" },
        },
        {
          selector: "edge[relationshipType = 'PAYMENT_TO']",
          style: { "line-color": "#f87171", "target-arrow-color": "#f87171" },
        },
        {
          selector: "node:selected",
          style: {
            "border-width": 4,
            "overlay-opacity": 0.2,
          },
        },
      ],
      layout: {
        name: "cose",
        animate: true,
        fit: true,
        padding: 28,
        idealEdgeLength: 120,
        nodeRepulsion: 5000,
        gravity: 0.2,
      },
      zoom: 1,
      minZoom: 0.2,
      maxZoom: 2.2,
      wheelSensitivity: 0.18,
    });

    graphRef.current = cy;

    cy.on("tap", "node", (event) => {
      const nodeId = event.target.id();
      setSelectedNodeId(nodeId);
      setSelectedEdgeId(null);
    });

    cy.on("tap", "edge", (event) => {
      const edgeId = event.target.id();
      setSelectedEdgeId(edgeId);
      setSelectedNodeId(null);
    });

    cy.on("tap", (event) => {
      if (event.target === cy) {
        setSelectedNodeId(null);
        setSelectedEdgeId(null);
      }
    });

    cy.fit();
    return () => {
      cy.destroy();
      graphRef.current = null;
    };
  }, [graphData]);

  useEffect(() => {
    if (!selectedNode) {
      setNodeDetail(null);
      return;
    }

    const node = selectedNode;
    let ignore = false;
    async function hydrateNodeDetail() {
      try {
        const results = await api.search(node.id, node.entityType);
        if (!ignore && results.length > 0) {
          setNodeDetail(results[0]);
        } else if (!ignore) {
          setNodeDetail({
            id: node.id,
            entityType: node.entityType,
          } as EntitySearchResult);
        }
      } catch {
        if (!ignore) {
          setNodeDetail({
            id: node.id,
            entityType: node.entityType,
          } as EntitySearchResult);
        }
      }
    }

    void hydrateNodeDetail();
    return () => {
      ignore = true;
    };
  }, [selectedNode]);

  const handleResetLayout = () => {
    graphRef.current?.layout({ name: "cose", animate: true, fit: true, padding: 28, idealEdgeLength: 120 }).run();
  };

  const handleFocus = () => {
    const selected = graphRef.current?.$id(entityId);
    if (selected && selected.length > 0) {
      selected.select();
      graphRef.current?.animate({ center: { eles: selected }, duration: 300 });
      graphRef.current?.fit(selected, 40);
      setSelectedNodeId(entityId);
      setSelectedEdgeId(null);
      return;
    }
    void loadNeighborhood(entityId);
  };

  const selectedNeighborSummary = useMemo(() => {
    if (!graphData) {
      return [] as Array<{ label: string; target: string; type: string }>;
    }
    const neighbors = graphData.edges.filter((edge) => edge.source === selectedNodeId || edge.target === selectedNodeId).map((edge) => ({
      label: edge.source === selectedNodeId ? edge.target : edge.source,
      target: edge.source === selectedNodeId ? edge.target : edge.source,
      type: edge.relationshipType,
    }));
    return neighbors;
  }, [graphData, selectedNodeId]);

  return (
    <div className="graph-shell">
      <div className="graph-toolbar" aria-label="Graph controls">
        <div className="graph-toolbar-group">
          <button type="button" className="button secondary" onClick={() => graphRef.current?.fit()}>Fit graph</button>
          <button type="button" className="button secondary" onClick={handleResetLayout}>Reset layout</button>
          <button type="button" className="button secondary" onClick={() => graphRef.current?.zoom(graphRef.current.zoom() + 0.15)}>Zoom in</button>
          <button type="button" className="button secondary" onClick={() => graphRef.current?.zoom(graphRef.current.zoom() - 0.15)}>Zoom out</button>
        </div>
        <div className="focus-form">
          <label>
            Focus entity
            <input value={entityId} onChange={(event) => setEntityId(event.target.value)} placeholder="CUST-W / ACC-101 / DEV-909" aria-label="Entity identifier to graph" />
          </label>
          <button type="button" className="button" onClick={handleFocus}>Load neighborhood</button>
          <button type="button" className="button secondary" onClick={() => { setSelectedNodeId(null); setSelectedEdgeId(null); graphRef.current?.elements().unselect(); }}>Clear selection</button>
        </div>
      </div>

      {loading && <LoadingState label="Loading graph neighborhood from the API…" />}
      {error && <ErrorState message={error} />}
      {!loading && !error && graphData && graphData.nodes.length === 0 && <EmptyState>No relationships found for this investigation.</EmptyState>}

      {graphData && graphData.nodes.length > 0 && (
        <div className="graph-layout">
          <div className="graph-canvas" ref={containerRef} aria-label="Interactive graph visualization" role="img" />

          <aside className="graph-detail-panel" aria-live="polite">
            {selectedNode ? (
              <>
                <h3>Selected entity</h3>
                <p className="detail-title">{selectedNode.entityType}: {selectedNode.id}</p>
                <dl className="result-detail compact">
                  {nodeDetail && Object.entries(nodeDetail).filter(([, value]) => value !== null && value !== undefined).map(([key, value]) => (
                    <div key={key}><dt>{key}</dt><dd>{Array.isArray(value) ? value.join(", ") : String(value)}</dd></div>
                  ))}
                </dl>
                {selectedNeighborSummary.length > 0 && (
                  <div className="summary-block">
                    <h4>Connected entities</h4>
                    <ul>
                      {selectedNeighborSummary.map((neighbor) => (
                        <li key={`${neighbor.target}-${neighbor.type}`}><strong>{relationshipLabel(neighbor.type)}</strong> · {neighbor.target}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            ) : selectedEdge ? (
              <>
                <h3>Selected relationship</h3>
                <p className="detail-title">{selectedEdge.relationshipType}</p>
                <dl className="result-detail compact">
                  <div><dt>Source</dt><dd>{selectedEdge.source}</dd></div>
                  <div><dt>Target</dt><dd>{selectedEdge.target}</dd></div>
                  {Object.entries(selectedEdge.metadata ?? {}).filter(([, value]) => value !== null && value !== undefined).map(([key, value]) => (
                    <div key={key}><dt>{key}</dt><dd>{Array.isArray(value) ? value.join(", ") : typeof value === "object" ? JSON.stringify(value) : String(value)}</dd></div>
                  ))}
                </dl>
              </>
            ) : (
              <>
                <h3>Investigation context</h3>
                <p className="detail-title">{entityId}</p>
                <p className="muted">Select a node or edge to inspect the approved graph relationship data returned by the API.</p>
              </>
            )}
          </aside>
        </div>
      )}
    </div>
  );
}
