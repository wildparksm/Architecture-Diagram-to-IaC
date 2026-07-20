# Policy Enforcement Checklist (Authoritative: Runner)

## Decision
- Authoritative enforcement path: runner pre-filter
- Target files:
  - `src/run_pptx_evidence.py`
  - `src/run_drawio_evidence.py`

## Checklist
1. Policy source
- `architecture.ir.json` MUST contain `codegenPolicy.allowedCategories`.
- Runners MUST normalize requested categories before emission.

2. Effective filtering
- Before calling emitter, runners MUST filter out Azure resources not in allowlist.
- Default (empty allowlist) MUST result in report-only behavior.

3. API/UI consistency
- `/health`, `/api/v1/ingest`, `/api/v1/jobs/{jobId}` MUST expose enforcement mode/location.
- Upload UI MUST display enforcement mode/location and compliance summary.

4. Manifest traceability
- `run-manifest.json` MUST include:
  - `codegenPolicySnapshot` (requested/effective categories, enforcement mode/location)
  - `runtimeFingerprint` (python/runtime and module file hashes)

5. Regression gate
- With `--allow-category azure.networkBundle`, generated `main.bicep` MUST NOT include Firewall/AVD declarations.
- For the same run, manifest policy snapshot MUST match the requested allowlist.

6. Operations integration
- `docs/OPERATIONS_RELEASE_CHECKLIST.md` MUST reference policy regression and runtime traceability gates.
- `docs/EMITTER_DRIFT_RCA.md` MUST be updated when drift symptom or root cause changes.

## Rollback rule
- If emitter/runtime drift is detected again, keep runner pre-filter as immutable gate and treat emitter filtering as best-effort only.
