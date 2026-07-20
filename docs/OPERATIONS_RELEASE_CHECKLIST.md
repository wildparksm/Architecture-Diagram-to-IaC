# Operations Release Checklist

## Scope
- Internal beta operations for diagram-to-IaC pipeline.
- Enforces policy safety, runtime traceability, and operator observability.

## Pre-Release Gates
1. Policy regression
- Run `python scripts/run_policy_quality_gates.py`.
- All 3 scenarios must pass (report-only, networkBundle only, composite allowlist).

2. Schema and policy validation
- Invalid allow categories must fail fast in API and CLI.
- Error must include unsupported value and allowed category list.

3. Runtime traceability
- `run-manifest.json` contains:
  - `codegenPolicySnapshot`
  - `runtimeFingerprint`
- Job API payload includes both fields when run completes.

4. UI observability
- Upload page displays enforcement mode/location.
- Upload page shows policy requested/effective categories and runtime hashes.

## Regression Evidence Package (per release)
- Latest run ID with input file name.
- `main.bicep` suppression proof (no Firewall/AVD unless intentionally allowlisted and approved).
- `run-manifest.json` snapshot attached.
- Generate zip bundle: `python scripts/package_release_evidence.py --run-id <run-id>`

## Rollback Decision Rule
- If policy drift or runtime mismatch is detected:
  1. Stop release.
  2. Keep runner pre-filter as authoritative gate.
  3. Re-run policy regression before resuming release.

## Sign-off
- Engineering: policy and regression gates passed.
- Operator: UI/API observability checks passed.
- Release owner: rollback path verified.
