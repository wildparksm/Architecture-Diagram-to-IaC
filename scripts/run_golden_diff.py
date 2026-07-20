from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT_DIR / "tests"
SNAPSHOTS_DIR = TESTS_DIR / "golden_snapshots"

GOLDEN_INPUTS = {
    "pptx_main": {
        "file": "Architecture Diagram to IaC Compiler.pptx",
        "runner": "src/run_pptx_evidence.py",
        "allow_categories": ["azure.networkBundle", "azure.firewall"],
    },
    "drawio_simple": {
        "file": "samples/simple.drawio",
        "runner": "src/run_drawio_evidence.py",
        "allow_categories": ["azure.networkBundle"],
    },
    "drawio_network": {
        "file": "samples/network_only.drawio",
        "runner": "src/run_drawio_evidence.py",
        "allow_categories": ["azure.virtualNetwork"],
    },
}

FILES_TO_COMPARE = [
    "architecture.ir.json",
    "main.bicep",
]


def _run_pipeline(key: str, config: dict, runs_dir: Path) -> Path:
    run_id = f"golden-{key}"
    cmd = [
        sys.executable,
        config["runner"],
        "--input",
        config["file"],
        "--runs-dir",
        str(runs_dir),
        "--run-id",
        run_id,
    ]
    for category in config.get("allow_categories", []):
        cmd.extend(["--allow-category", category])

    print(f"Running pipeline for {key}...")
    result = subprocess.run(
        cmd,
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        print(f"Error running pipeline for {key}:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    return runs_dir / run_id


def _normalize_json(filepath: Path) -> str:
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
        return json.dumps(data, indent=2, sort_keys=True)
    except Exception:
        return filepath.read_text(encoding="utf-8")


def _get_normalized_content(filepath: Path) -> str:
    if filepath.suffix == ".json":
        return _normalize_json(filepath)
    return filepath.read_text(encoding="utf-8")


def update_snapshots() -> None:
    temp_dir = Path(tempfile.mkdtemp(prefix="golden-update-"))
    try:
        runs_dir = temp_dir / "runs"
        runs_dir.mkdir()

        for key, config in GOLDEN_INPUTS.items():
            run_dir = _run_pipeline(key, config, runs_dir)
            snap_dir = SNAPSHOTS_DIR / key
            snap_dir.mkdir(parents=True, exist_ok=True)

            for filename in FILES_TO_COMPARE:
                src = run_dir / filename
                dst = snap_dir / filename
                if src.exists():
                    shutil.copy2(src, dst)
                    print(f"Updated snapshot: {dst.relative_to(ROOT_DIR)}")
                else:
                    print(f"Warning: {filename} not found in {run_dir}", file=sys.stderr)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def verify_snapshots() -> int:
    temp_dir = Path(tempfile.mkdtemp(prefix="golden-verify-"))
    failures = 0
    try:
        runs_dir = temp_dir / "runs"
        runs_dir.mkdir()

        for key, config in GOLDEN_INPUTS.items():
            run_dir = _run_pipeline(key, config, runs_dir)
            snap_dir = SNAPSHOTS_DIR / key

            if not snap_dir.exists():
                print(f"Error: Snapshot directory for {key} does not exist. Run --update first.", file=sys.stderr)
                failures += 1
                continue

            for filename in FILES_TO_COMPARE:
                gen_file = run_dir / filename
                snap_file = snap_dir / filename

                if not gen_file.exists():
                    print(f"Error: Generated file {filename} missing for {key}", file=sys.stderr)
                    failures += 1
                    continue
                if not snap_file.exists():
                    print(f"Error: Snapshot file {filename} missing for {key}", file=sys.stderr)
                    failures += 1
                    continue

                gen_content = _get_normalized_content(gen_file)
                snap_content = _get_normalized_content(snap_file)

                if gen_content != snap_content:
                    print(f"\n[FAIL] Diff found in {key}/{filename}:")
                    diff = difflib.unified_diff(
                        snap_content.splitlines(),
                        gen_content.splitlines(),
                        fromfile=f"snapshot/{filename}",
                        tofile=f"generated/{filename}",
                        lineterm="",
                    )
                    for line in diff:
                        print(line)
                    failures += 1
                else:
                    print(f"[PASS] {key}/{filename} matches snapshot.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    if failures > 0:
        print(f"\nGOLDEN_DIFF=FAIL ({failures} differences found)", file=sys.stderr)
        return 1
    
    print("\nGOLDEN_DIFF=PASS")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Golden Input Snapshot Diff Tool")
    parser.add_argument("--update", action="store_true", help="Update golden snapshots")
    parser.add_argument("--verify", action="store_true", help="Verify against golden snapshots")
    args = parser.parse_args()

    if not args.update and not args.verify:
        parser.print_help()
        sys.exit(1)

    if args.update:
        update_snapshots()
    
    if args.verify:
        sys.exit(verify_snapshots())


if __name__ == "__main__":
    main()
