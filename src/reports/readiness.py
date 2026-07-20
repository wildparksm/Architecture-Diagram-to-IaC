from __future__ import annotations

from typing import Dict, List
from pathlib import Path


def write_iac_readiness_report(
    path: Path,
    records: List[Dict[str, object]],
    graph: Dict[str, object],
    architecture_ir: Dict[str, object],
) -> None:
    questions = architecture_ir.get("providerNeutralCore", {}).get("questions", [])
    blockers = [q for q in questions if isinstance(q, dict) and q.get("type") == "Blocker"]
    risks = [q for q in questions if isinstance(q, dict) and q.get("type") == "Risk"]
    readiness = architecture_ir.get("readiness", {}) if isinstance(architecture_ir.get("readiness"), dict) else {}
    gate_reasons = readiness.get("gateReasons", []) if isinstance(readiness.get("gateReasons"), list) else []

    lines = [
        "# IaC Readiness Report",
        "",
        "## Summary",
        f"- Raw evidence records: {len(records)}",
        f"- Graph nodes: {len(graph.get('nodes', []))}",
        f"- Graph edges: {len(graph.get('edges', []))}",
        f"- IR resources: {len(architecture_ir.get('providerNeutralCore', {}).get('resources', []))}",
        f"- Open blockers: {len(blockers)}",
        f"- Open risks: {len(risks)}",
        f"- Gate reasons: {', '.join(gate_reasons) if gate_reasons else 'none'}",
        "",
        "## Gate Decision",
    ]

    if isinstance(readiness, dict) and readiness.get("productionReady"):
        lines.append("- Production-ready: YES")
    else:
        lines.append("- Production-ready: NO")
        lines.append("- Reason: open blockers or unresolved assumptions")

    lines.append("")
    lines.append("## Notes")
    lines.append("- This report is draft quality and should be reviewed by an architect.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
