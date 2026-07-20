# Source Code Layout

- adapters: source-specific parsers (PPTX, draw.io, etc.)
- extractors: OCR/CV/VLM and metadata extractors
- graph: graph reconstruction logic
- ir: provider-neutral IR compiler
- emitters: target output generators (Bicep, Terraform, docs)
- validators: schema/semantic/target validators
- reports: traceability and report builders

## First runnable command

python src/run_pptx_evidence.py --input "Architecture Diagram to IaC Compiler.pptx"

python src/run_drawio_evidence.py --input "samples/simple.drawio"

## Upload API server (MVP)

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn src.api_server:app --host 0.0.0.0 --port 8000 --reload

Open UI:

http://localhost:8000/

Endpoints:

- POST /api/v1/ingest (multipart file upload)
- GET /api/v1/jobs/{jobId}
- GET /api/v1/runs/{runId}/artifacts
- GET /api/v1/runs/{runId}/artifacts/{name}

Quick flow:

1. Open `/`
2. Upload `.pptx` or `.drawio/.xml`
3. Select one or more codegen categories, or leave everything unselected for report-only mode
4. Wait until status becomes `completed`
5. Download generated artifacts from the links
6. Check enforcement metadata shown in UI (mode and location) to verify active policy path
7. Use the Job Timeline panel to track upload, queue, run, and completion events
8. Review the Allowlist Compliance card for IR-based eligible/suppressed resource counts

Default policy:

- No Bicep is emitted unless the upload request includes an allowlist
- Firewall and AVD stay report-only unless explicitly allowlisted
- Current enforcement path: runner pre-filter in `src/run_pptx_evidence.py` and `src/run_drawio_evidence.py`
