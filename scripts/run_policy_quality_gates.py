from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]


def _run(cmd: list[str], title: str) -> int:
    print(f"\n== {title} ==")
    print("$", " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    print(f"exit={result.returncode}")
    return result.returncode


def main() -> int:
    failures = 0

    failures += _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_policy_regression.py",
        ],
        "Policy Regression Suite",
    )

    invalid_policy_cmd = [
        sys.executable,
        "src/run_pptx_evidence.py",
        "--input",
        "Architecture Diagram to IaC Compiler.pptx",
        "--allow-category",
        "azure.notRealCategory",
    ]
    print("\n== Policy Invalid Input Gate ==")
    print("$", " ".join(invalid_policy_cmd))
    invalid_result = subprocess.run(
        invalid_policy_cmd,
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if invalid_result.stdout:
        print(invalid_result.stdout.rstrip())
    if invalid_result.stderr:
        print(invalid_result.stderr.rstrip(), file=sys.stderr)
    print(f"exit={invalid_result.returncode}")

    if invalid_result.returncode != 2:
        print("Expected invalid category gate to exit with code 2.", file=sys.stderr)
        failures += 1

    if failures == 0:
        print("\n== Golden Snapshot Diff Gate ==")
        diff_result = subprocess.run(
            [sys.executable, "scripts/run_golden_diff.py", "--verify"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if diff_result.stdout:
            print(diff_result.stdout.rstrip())
        if diff_result.stderr:
            print(diff_result.stderr.rstrip(), file=sys.stderr)
        print(f"exit={diff_result.returncode}")
        
        if diff_result.returncode != 0:
            failures += 1

    if failures == 0:
        print("\nQUALITY_GATES=PASS")
        return 0

    print(f"\nQUALITY_GATES=FAIL ({failures})", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
