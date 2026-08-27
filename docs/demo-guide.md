# FinGuard canonical demonstration guide

This guide documents the seeded scenarios that should be used in a live demo or submission walkthrough.

## Scenario 1 — Shared Device

Input:

- `DEV-909`

Expected results:

- `CUST-A`
- `CUST-B`
- `CUST-C`

This demonstrates a single device being used by multiple customers, which is a common shared-infrastructure fraud signal.

## Scenario 2 — Shared IP

Input:

- `192.0.2.45`

Expected results:

- `CUST-W`
- `CUST-X`
- `CUST-Y`
- `CUST-Z`

This demonstrates a shared proxy IP associated with multiple customers.

## Scenario 3 — Circular Transfer

Input:

- `ACC-101`

Expected cycle:

- `ACC-101 -> ACC-202 -> ACC-303 -> ACC-101`

Expected `cycleLength`:

- `3`

This demonstrates an account loop that indicates circular fund movement among three accounts.

## Scenario 4 — Device Blast Radius

Input:

- `DEV-101`

Expected result counts:

- 1 hop = 4 entities
- 2 hops = 9 entities
- 3 hops = 10 entities

This demonstrates a bounded network expansion from a compromised device across connection types.

## Scenario 5 — Synthetic Identity

Inputs:

- `DEV-101`
- `192.0.2.45`

Expected results:

- 4 customer cluster members
- `MERCH-99`
- `riskRating = HIGH`

This demonstrates a synthetic identity pattern that combines a shared device and shared proxy address with payment activity to a high-risk merchant.

## Submission note

These scenarios are part of the approved seeded dataset and should be documented as demonstration use cases rather than hard-coded application behavior.
