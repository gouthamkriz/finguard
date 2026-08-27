# FinGuard

FinGuard is a graph-driven fraud investigation application that helps reviewers trace suspicious relationships across customers, accounts, devices, IP addresses, and merchants. The system surfaces shared infrastructure, circular transfer loops, shortest transfer paths, blast radius impact, and synthetic identity clusters in a single investigation workspace.

## Problem statement

Modern fraud teams often need to connect fragmented signals across accounts, devices, IP addresses, and transaction history. Manual review is slow and error-prone when the important signal is the relationship network rather than a single record. FinGuard keeps the investigation grounded in a graph database and presents that context in a readable web experience.

## What FinGuard does

FinGuard helps a reviewer:

- search entities by ID or name
- inspect shared device usage and shared IP activity
- detect circular transfers between accounts
- find shortest bounded payment paths
- calculate blast radius exposure for a compromised device
- detect synthetic identity patterns that combine device reuse, proxy IP usage, and high-risk merchant activity
- visualize a one-hop neighborhood graph around an entity for rapid investigation

## Architecture overview

The application follows a three-layer design:

Browser -> React + Vite frontend -> FastAPI REST API -> Cognodb via db.py and queries.py

Important constraints:

- the frontend never connects directly to the database
- graph data comes from the REST API only
- Cypher queries are parameterized and centralized in queries.py
- all investigation logic is exposed through the backend API

## Technology stack

- Python 3.11
- FastAPI
- Neo4j Python driver
- CognoDB / Neo4j-compatible graph database
- React 19
- TypeScript
- Vite
- Cytoscape
- Pytest

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── services.py
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env.example
├── db.py
├── queries.py
├── requirements.txt
├── seed.py
├── seed_data.py
├── test_api.py
├── test_connection.py
├── .env.example
├── .gitignore
├── README.md
└── docs/
    ├── investigation-guide.md
    ├── demo-guide.md
    └── screenshots/README.md
```

## Prerequisites

Before running the project, make sure the following are available:

- Python 3.11+
- Node.js 18+ and npm
- access to a working CognoDB / Neo4j-compatible database
- network access from the local machine to the database

## Environment setup

1. Create a Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install Python dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Install frontend dependencies:

```powershell
cd frontend
npm install
cd ..
```

4. Configure local environment variables in `.env`:

```env
COGNODB_URI=
COGNODB_USERNAME=
COGNODB_PASSWORD=
```

Do not commit `.env`.

## CognoDB configuration

The backend connects using the official Neo4j Python driver. Configuration is loaded from environment variables defined in `.env` by `db.py` and passed through the backend service layer.

Required environment variables:

```env
COGNODB_URI=
COGNODB_USERNAME=
COGNODB_PASSWORD=
```

Notes:

- keep `COGNODB_URI`, `COGNODB_USERNAME`, and `COGNODB_PASSWORD` server-side only
- never expose these in frontend code or Vite config
- do not copy real secret values into README or committed config files

## Database seeding instructions

The seeded graph is created and validated by `seed.py`:

```powershell
.\.venv\Scripts\python.exe seed.py
```

This script:

- verifies database connectivity
- creates graph constraints and indexes
- loads the canonical FinGuard dataset
- validates the expected counts and scenario mappings

## Backend startup

Run the FastAPI app from the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open:

- http://localhost:8000/health
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Frontend startup

Run the frontend development server:

```powershell
cd frontend
npm run dev
```

The Vite app serves on:

- http://localhost:5173

Production API routing uses:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The value is defined in `frontend/.env.example` and can be overridden in a local `.env` file for the frontend if needed.

## API documentation location

Interactive API documentation is available at:

- http://localhost:8000/docs

Current backend routes include:

- `GET /health`
- `GET /api/v1/search`
- `GET /api/v1/investigations/shared-device`
- `GET /api/v1/investigations/shared-ip`
- `GET /api/v1/investigations/circular-transfers`
- `GET /api/v1/investigations/shortest-path`
- `GET /api/v1/investigations/high-risk-merchants`
- `GET /api/v1/investigations/blast-radius`
- `GET /api/v1/investigations/synthetic-identity`
- `GET /api/v1/neighborhood`

## Demo

🎥 [Watch the FinGuard Demo](https://youtu.be/T2cnpgFpVm4)

## Investigation workflows

A typical workflow is:

1. Search for a customer, account, device, IP address, or merchant.
2. Select a result to open the investigation workspace.
3. Review the relationship summary and evidence cards.
4. Open the graph for the selected entity.
5. Inspect connected nodes and edges.
6. Run a targeted investigation such as shared device, shared IP, circular transfer, or blast radius.
7. Use the graph and evidence side panel to understand the relationship path before making a judgment.

## Canonical demonstration scenarios

These scenarios are part of the seeded dataset and are used as demonstration anchors.

### Scenario 1 — Shared Device

Input: `DEV-909`

Expected customers:

- `CUST-A`
- `CUST-B`
- `CUST-C`

### Scenario 2 — Shared IP

Input: `192.0.2.45`

Expected customers:

- `CUST-W`
- `CUST-X`
- `CUST-Y`
- `CUST-Z`

### Scenario 3 — Circular Transfer

Input: `ACC-101`

Expected cycle:

`ACC-101 -> ACC-202 -> ACC-303 -> ACC-101`

`cycleLength = 3`

### Scenario 4 — Device Blast Radius

Input: `DEV-101`

Expected impact:

- 1 hop = 4 entities
- 2 hops = 9 entities
- 3 hops = 10 entities

### Scenario 5 — Synthetic Identity

Inputs:

- `DEV-101`
- `192.0.2.45`

Expected:

- 4 customer cluster members
- `MERCH-99`
- `riskRating = HIGH`

## Testing instructions

Run the backend API test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest test_api.py -v
```

Expected result: `24 passed`.

Run the frontend production build:

```powershell
cd frontend
npm run build
```

Expected result: TypeScript passes and Vite completes a successful production build.

## Production build instructions

Frontend production build:

```powershell
cd frontend
npm run build
```

This command validates the app with TypeScript and generates a Vite production bundle.

## Security notes

- `.env` is required for local credentials and must not be committed
- `db.py` loads values from environment variables only
- frontend configuration uses safe public variables such as `VITE_API_BASE_URL`
- no database credentials are exposed in the frontend or docs
- query parameters are validated server-side
- errors remain sanitized and do not leak internal driver or database details

## Limits and scope

This project focuses on a specific fraud review workflow and seeded graph dataset. It is not a general-purpose graph platform and is intentionally scoped to a documentation-friendly investigation use case.

## Deployment notes

The intended production architecture remains:

Browser -> Frontend -> HTTP REST API -> FastAPI -> db.py -> CognoDB Cloud

A hosted deployment is acceptable only when:

- the backend remains the only component that connects to CognoDB
- the frontend uses a public API base URL such as `VITE_API_BASE_URL`
- secrets remain in the server environment only
- CORS is explicit and limited to trusted origins
- health checks remain safe and do not expose internal data

No automatic deployment was performed in this session.

## Investigation guide

See [docs/investigation-guide.md](docs/investigation-guide.md) for a non-technical workflow guide.

## Demo guide

See [docs/demo-guide.md](docs/demo-guide.md) for the canonical demo sequence and scenario walkthrough.

## Screenshot readiness

No browser-based screenshot capture was performed in this environment. Manual capture instructions are documented in [docs/screenshots/README.md](docs/screenshots/README.md).

## Security and repository audit

The repository is expected to keep `.env`, `.venv`, and Python cache files out of source control via `.gitignore`.

The frontend must never contain:

- `COGNODB_URI`
- `COGNODB_USERNAME`
- `COGNODB_PASSWORD`
- raw `bolt+s://` strings
- untrusted query concatenation in Cypher

## Final note

This repository is ready for review as a bounded, graph-backed fraud investigation demo. It uses real graph data, a documented backend API, a staged seeded dataset, and a frontend workflow designed for investigation rather than generic dashboard display.
