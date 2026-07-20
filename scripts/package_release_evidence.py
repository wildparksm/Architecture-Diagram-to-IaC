from __future__ import annotations

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import zipfile


DEFAULT_ARTIFACTS = [
    "run-manifest.json",
    "main.bicep",
    "validation-report.md",
    "iac-readiness-report.md",
    "traceability-matrix.csv",
    "unresolved-questions.md",
    "architecture.ir.json",
]

FIREWALL_TOKEN = "Microsoft.Network/azureFirewalls@2023-11-01"
AVD_HOSTPOOL_TOKEN = "Microsoft.DesktopVirtualization/hostPools@2024-04-03"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create release evidence zip for a run")
    parser.add_argument("--run-id", required=True, help="Run id under runs/")
    parser.add_argument("--runs-dir", default="runs", help="Runs directory")
    parser.add_argument("--output", default="", help="Optional output zip path")
    return parser.parse_args()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_summary(run_dir: Path, run_id: str) -> str:
    manifest_path = run_dir / "run-manifest.json"
    bicep_path = run_dir / "main.bicep"

    manifest = _read_json(manifest_path) if manifest_path.exists() else {}
    policy = manifest.get("codegenPolicySnapshot", {}) if isinstance(manifest.get("codegenPolicySnapshot"), dict) else {}
    runtime = manifest.get("runtimeFingerprint", {}) if isinstance(manifest.get("runtimeFingerprint"), dict) else {}

    bicep = bicep_path.read_text(encoding="utf-8") if bicep_path.exists() else ""

    lines = [
        "# Release Evidence Summary",
        "",
        f"- runId: {run_id}",
        f"- generatedAtUtc: {datetime.now(timezone.utc).isoformat()}",
        f"- firewallDeclared: {FIREWALL_TOKEN in bicep}",
        f"- avdHostPoolDeclared: {AVD_HOSTPOOL_TOKEN in bicep}",
        f"- enforcementMode: {policy.get('enforcementMode', '-')}",
        f"- requestedAllowedCategories: {policy.get('requestedAllowedCategories', [])}",
        f"- effectiveAllowedCategories: {policy.get('effectiveAllowedCategories', [])}",
        f"- runtimePlatform: {runtime.get('platform', '-')}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    run_dir = Path(args.runs_dir) / args.run_id
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"Run directory not found: {run_dir}")
        return 1

    output_path = Path(args.output) if args.output else run_dir / f"release-evidence-{args.run_id}.zip"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary_text = _build_summary(run_dir, args.run_id)

    with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for artifact_name in DEFAULT_ARTIFACTS:
            artifact_path = run_dir / artifact_name
            if artifact_path.exists() and artifact_path.is_file():
                zf.write(artifact_path, arcname=artifact_name)
        zf.writestr("release-evidence-summary.md", summary_text)

    print(f"run_id={args.run_id}")
    print(f"package={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
