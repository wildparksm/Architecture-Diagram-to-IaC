# Frontend Upload Integration Plan

## Why This Exists

Current MVP runs from local CLI input files, not from a web upload UI. This document defines how to integrate a future frontend upload page without changing core extraction/IR/emitter behavior.

## Current Diagram Origin (As-Is)

1. User/runner provides a local file path to CLI.
2. Runner loads file and executes parser pipeline.
3. Outputs are written to `runs/<run-id>/...`.

Current entrypoints:
- `python src/run_pptx_evidence.py --input "Architecture Diagram to IaC Compiler.pptx"`
- `python src/run_drawio_evidence.py --input "samples/simple.drawio"`

## Not Yet Implemented

- Backend upload API endpoint
- Async job status API for frontend polling
- User/session scoped storage for uploaded files

Implemented now:

- Web frontend upload page (`src/static/index.html`)
- Backend upload API endpoint (`POST /api/v1/ingest`)
- Async job status API (`GET /api/v1/jobs/{jobId}`)

## Target Integration Shape (Frontend + Backend)

### Frontend (planned)

1. Upload file (`.pptx`, `.drawio`, `.xml`)
2. Select target output (`bicep`, later `terraform`)
3. Submit and receive `jobId`
4. Poll status endpoint
5. Download artifacts (`main.bicep`, `traceability-matrix.csv`, reports)

Codegen policy:

- Default mode is report-only
- Uploaded files only emit Bicep when the request includes an explicit allowlist of categories
- Firewall and AVD are treated as manual/advanced categories

### Backend (planned)

Recommended endpoints:

1. `POST /api/v1/ingest`
- multipart file upload
- validates extension and max size
- stores file under temp workspace
- creates run id and starts pipeline
- returns `{ jobId, runId }`

2. `GET /api/v1/jobs/{jobId}`
- returns run status: `queued|running|failed|completed`
- returns summary metrics when complete

3. `GET /api/v1/runs/{runId}/artifacts`
- returns artifact list and download links

4. `GET /api/v1/runs/{runId}/artifacts/{name}`
- streams artifact file

## Backend Security/Validation Requirements

- Allowlist file types: `.pptx`, `.drawio`, `.xml`
- Block path traversal and zip bomb patterns
- Enforce upload size limit
- Per-job isolated working directory
- Optional malware scan hook before parsing

## Pipeline Contract To Preserve

Regardless of upload/CLI source, keep these artifacts and semantics unchanged:

- `raw-evidence.json`
- `architecture.graph.json`
- `architecture.ir.json`
- `main.bicep`
- `traceability-matrix.csv`
- `iac-readiness-report.md`
- `validation-report.md`
- `run-manifest.json`

## Immediate Next Step

Implement a thin backend adapter that accepts uploaded files and invokes existing runner logic, then expose artifact download endpoints for frontend consumption.
