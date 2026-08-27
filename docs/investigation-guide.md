# FinGuard investigation guide

This guide explains how a non-technical reviewer can use FinGuard to investigate suspicious financial activity.

## Search

Use the search page to look up an entity by ID or name. Valid entity types include:

- Customer
- Account
- Device
- IPAddress
- Merchant

A search can be broad or targeted. For example, searching for `DEV-909` or `192.0.2.45` narrows the review to a specific suspicious object.

## Selecting an entity

When a result appears, select it to move into the investigation workspace. The system brings the entity into context and loads the graph neighborhood around it.

## Opening the graph

The investigation workspace includes a graph panel. This graph shows the selected entity and the immediate surrounding nodes and relationships. This is useful for seeing how the entity fits into the broader network.

## Running investigations

The investigation panel includes focused checks such as:

- Shared Device
- Shared IP
- Circular Transfers
- Shortest Path
- High-Risk Merchants
- Blast Radius
- Synthetic Identity

Each check surfaces a distinct fraud pattern derived from the graph dataset.

## Understanding evidence

FinGuard writes the relevant evidence as structured results rather than raw technical output. Each investigation shows the objects involved and the relationship context behind the result.

## Selecting nodes

Click a node in the graph to inspect that entity in context. The detail panel shows the relevant metadata and highlights how it connects to the surrounding network.

## Selecting relationships

Click an edge to inspect the relationship type and the business meaning behind it. This helps explain whether the link is a payment, ownership, device use, or login pattern.

## Reading graph relationships

The graph emphasizes relationship direction and interaction patterns. A reviewer reads the visual edges to determine whether a suspicious pattern is emerging, such as a shared device among multiple customers or a circular account flow.

## Resetting or focusing the graph

Use the graph controls to refocus on a selected entity or refresh the neighborhood. This helps keep the review grounded in the specific investigation target instead of a broad graph view.

## Practical usage

A reviewer can start with one signal, such as a suspicious device or proxy IP, and then expand outward using the investigation tools until the graph explains the chain of potential fraud.
