# Emitter Drift RCA (2026-07-20)

## Summary
- Symptom: allowlist policy edits looked correct in source, but runtime behavior intermittently appeared inconsistent.
- Current safety baseline: runner pre-filter (`src/run_pptx_evidence.py`, `src/run_drawio_evidence.py`) is authoritative.
- Impact scope: Bicep emission path only. IR/report generation remained stable.

## Confirmed Findings
1. Duplicate logic in emitter entry point
- `emit_bicep` had duplicated `codegenPolicy` initialization and repeated suppression blocks.
- This made code review and runtime reasoning harder and increased risk of accidental divergence.

2. Source/runtime ambiguity during iterations
- During rapid edits, runtime behavior did not always match what was expected from spot-checking source.
- Root technical risk: execution path ambiguity rather than a single deterministic policy gate.

3. Lack of direct runtime evidence in job-level API
- Before this change, policy/runtime fingerprint data existed only in run artifacts.
- Operator had to manually open artifact files to verify enforcement details.

## Corrective Actions Applied
1. Authoritative enforcement locked at runner level
- Runner pre-filter is the required gate before emitter call.

2. Runtime evidence expanded
- `run-manifest.json` now includes `codegenPolicySnapshot` and `runtimeFingerprint`.
- API job response surfaces these fields for immediate UI visibility.

3. Emitter duplicate logic removed
- Removed duplicated policy initialization and repeated suppression checks in `src/emitters/bicep_emitter.py`.

## Why this is safe now
- Even if emitter behavior regresses, non-allowlisted Azure resources are filtered out in runner before emitter execution.
- Each run now carries module hashes (runner/emitter/policy) for reproducibility and auditability.

## Remaining Risks
- Emitter still has broad responsibilities (resource inference + suppression + dedupe), so future edits can reintroduce complexity.
- No CI gate yet validating all policy scenarios on each change.

## Next Guardrails
1. Keep runner pre-filter immutable until at least 3 consecutive release cycles pass with green regression.
2. Run policy regression suite on every PR and release candidate.
3. If emitter-only policy handling is proposed, require dual-run diff proof against runner-enforced output.
