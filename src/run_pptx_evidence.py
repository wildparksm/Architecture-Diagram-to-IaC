from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import platform
import sys

from adapters.pptx_adapter import PptxAdapter, dump_json
from emitters.bicep_emitter import emit_bicep
from graph.reconstruction import build_graph
from ir.compiler import compile_ir
from policy.codegen_policy import validate_allowed_categories
from reports.questions import collect_questions, write_question_report
from reports.readiness import write_iac_readiness_report
from reports.traceability import build_traceability_rows, write_traceability_csv
from validators.raw_evidence_validator import validate_records


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate raw evidence from PPTX source")
    parser.add_argument("--input", required=True, help="Path to PPTX file")
    parser.add_argument("--runs-dir", default="runs", help="Output runs directory")
    parser.add_argument("--run-id", default="", help="Optional run id")
    parser.add_argument("--allow-category", action="append", default=[], help="Allowed codegen category")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        normalized_allowed_categories = validate_allowed_categories(args.allow_category)
    except ValueError as exc:
        print(f"policy_validation_error={exc}", file=sys.stderr)
        return 2

    run_id = args.run_id or datetime.now(timezone.utc).strftime("run-%Y%m%d-%H%M%S")
    input_path = Path(args.input)
    runs_dir = Path(args.runs_dir)
    run_dir = runs_dir / run_id

    adapter = PptxAdapter(run_id=run_id)
    records = adapter.extract(input_path)

    errors = validate_records(records)

    raw_evidence_path = run_dir / "raw-evidence.json"
    graph_path = run_dir / "architecture.graph.json"
    ir_path = run_dir / "architecture.ir.json"
    manifest_path = run_dir / "run-manifest.json"
    bicep_path = run_dir / "main.bicep"
    traceability_path = run_dir / "traceability-matrix.csv"
    readiness_path = run_dir / "iac-readiness-report.md"
    questions_path = run_dir / "unresolved-questions.md"
    validation_path = run_dir / "validation-report.md"

    graph = build_graph(records)
    questions = collect_questions(records, graph)
    architecture_ir = compile_ir(graph, questions=questions)
    architecture_ir["codegenPolicy"] = {
        "allowedCategories": normalized_allowed_categories,
    }

    dump_json(raw_evidence_path, records)
    dump_json(graph_path, graph)
    dump_json(ir_path, architecture_ir)

    codegen_ir = deepcopy(architecture_ir)
    allowed_categories = set(architecture_ir.get("codegenPolicy", {}).get("allowedCategories", []))
    core = codegen_ir.get("providerNeutralCore", {}) if isinstance(codegen_ir.get("providerNeutralCore"), dict) else {}
    resources = core.get("resources", []) if isinstance(core.get("resources"), list) else []
    core["resources"] = [
        resource
        for resource in resources
        if not isinstance(resource, dict)
        or not str(resource.get("category", "")).startswith("azure.")
        or str(resource.get("category", "")) in allowed_categories
    ]
    emitted_code_locations = emit_bicep(codegen_ir, bicep_path)
    traceability_rows = build_traceability_rows(records, graph, architecture_ir, questions, emitted_code_locations)
    write_traceability_csv(traceability_path, traceability_rows)
    write_iac_readiness_report(readiness_path, records, graph, architecture_ir)

    write_question_report(questions_path, questions)

    dump_json(
        manifest_path,
        {
            "runId": run_id,
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "inputFile": str(input_path),
            "recordCount": len(records),
            "graphNodeCount": len(graph.get("nodes", [])),
            "graphEdgeCount": len(graph.get("edges", [])),
            "traceabilityRowCount": len(traceability_rows),
            "questionCount": len(questions),
            "emittedBicep": str(bicep_path.name),
            "validator": "raw-evidence-validator/0.1.0",
            "status": "failed" if errors else "passed",
            "codegenPolicySnapshot": {
                "enforcementMode": "runner-pre-filter",
                "enforcementLocation": [
                    "src/run_pptx_evidence.py",
                    "src/run_drawio_evidence.py",
                ],
                "requestedAllowedCategories": list(args.allow_category),
                "effectiveAllowedCategories": sorted(allowed_categories),
            },
            "runtimeFingerprint": {
                "pythonVersion": sys.version,
                "pythonExecutable": sys.executable,
                "platform": platform.platform(),
                "moduleFiles": {
                    "runner": {
                        "path": str(Path(__file__).resolve()),
                        "sha256": _file_sha256(Path(__file__).resolve()),
                    },
                    "emitter": {
                        "path": str((Path(__file__).resolve().parent / "emitters" / "bicep_emitter.py").resolve()),
                        "sha256": _file_sha256((Path(__file__).resolve().parent / "emitters" / "bicep_emitter.py").resolve()),
                    },
                    "policy": {
                        "path": str((Path(__file__).resolve().parent / "policy" / "codegen_policy.py").resolve()),
                        "sha256": _file_sha256((Path(__file__).resolve().parent / "policy" / "codegen_policy.py").resolve()),
                    },
                },
            },
        },
    )

    validation_lines = ["# Validation Report", ""]
    if errors:
        validation_lines.append("Status: FAILED")
        validation_lines.append("")
        for e in errors:
            validation_lines.append(f"- {e}")
    else:
        validation_lines.append("Status: PASSED")
        validation_lines.append("")
        validation_lines.append(f"- Records: {len(records)}")
        validation_lines.append(f"- Graph nodes: {len(graph.get('nodes', []))}")
        validation_lines.append(f"- Graph edges: {len(graph.get('edges', []))}")
        validation_lines.append(f"- IR resources: {len(architecture_ir.get('providerNeutralCore', {}).get('resources', []))}")
        validation_lines.append(f"- Questions: {len(questions)}")
        validation_lines.append("- Required fields: OK")
        validation_lines.append("- Confidence dimensions: OK")

    validation_path.write_text("\n".join(validation_lines) + "\n", encoding="utf-8")

    print(f"run_id={run_id}")
    print(f"records={len(records)}")
    print(f"output={run_dir}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
