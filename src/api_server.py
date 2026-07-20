from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, List, Optional
import shutil
import subprocess
import sys
import uuid

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

try:
    from policy.codegen_policy import get_known_allowed_categories, validate_allowed_categories
except ModuleNotFoundError:
    from src.policy.codegen_policy import get_known_allowed_categories, validate_allowed_categories

ROOT_DIR = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT_DIR / "runs"
UPLOADS_DIR = ROOT_DIR / "uploads"
STATIC_DIR = ROOT_DIR / "src" / "static"
MAX_UPLOAD_BYTES = 100 * 1024 * 1024
CODEGEN_ENFORCEMENT_MODE = "runner-pre-filter"
CODEGEN_ENFORCEMENT_LOCATION = "src/run_pptx_evidence.py, src/run_drawio_evidence.py"

ALLOWED_EXTENSIONS = {
    ".pptx": "pptx",
    ".drawio": "drawio",
    ".xml": "drawio",
}

ALLOWED_ARTIFACTS = {
    "raw-evidence.json",
    "architecture.graph.json",
    "architecture.ir.json",
    "main.bicep",
    "traceability-matrix.csv",
    "iac-readiness-report.md",
    "unresolved-questions.md",
    "validation-report.md",
    "run-manifest.json",
    "deployable-resources.md",
}


@dataclass
class JobState:
    job_id: str
    run_id: str
    status: str
    source_type: str
    filename: str
    created_at_utc: str
    updated_at_utc: str
    input_path: str
    allowed_categories: List[str] = field(default_factory=list)
    return_code: Optional[int] = None
    message: str = ""
    output_dir: str = ""
    stdout: str = ""
    stderr: str = ""
    artifact_names: List[str] = field(default_factory=list)
    codegen_policy_snapshot: Dict[str, object] = field(default_factory=dict)
    runtime_fingerprint: Dict[str, object] = field(default_factory=dict)


JOBS: Dict[str, JobState] = {}

app = FastAPI(title="Architecture Diagram to IaC API", version="0.1.0")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _update_job(job_id: str, **changes: object) -> None:
    job = JOBS[job_id]
    for key, value in changes.items():
        setattr(job, key, value)
    job.updated_at_utc = _now_iso()


def _build_command(source_type: str, input_path: Path, run_id: str, allowed_categories: List[str]) -> List[str]:
    if source_type == "pptx":
        runner = ROOT_DIR / "src" / "run_pptx_evidence.py"
    else:
        runner = ROOT_DIR / "src" / "run_drawio_evidence.py"

    return [
        sys.executable,
        str(runner),
        "--input",
        str(input_path),
        "--run-id",
        run_id,
        "--runs-dir",
        str(RUNS_DIR),
    ] + [item for category in allowed_categories for item in ("--allow-category", category)]


def _collect_artifacts(run_dir: Path) -> List[str]:
    if not run_dir.exists():
        return []
    return sorted([path.name for path in run_dir.iterdir() if path.is_file()])


def _load_manifest_fields(run_dir: Path) -> Dict[str, Dict[str, object]]:
    manifest_path = run_dir / "run-manifest.json"
    if not manifest_path.exists() or not manifest_path.is_file():
        return {
            "codegenPolicySnapshot": {},
            "runtimeFingerprint": {},
        }
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {
            "codegenPolicySnapshot": {},
            "runtimeFingerprint": {},
        }

    snapshot = payload.get("codegenPolicySnapshot", {})
    runtime = payload.get("runtimeFingerprint", {})
    return {
        "codegenPolicySnapshot": snapshot if isinstance(snapshot, dict) else {},
        "runtimeFingerprint": runtime if isinstance(runtime, dict) else {},
    }


def _run_pipeline_job(job_id: str) -> None:
    job = JOBS[job_id]
    _update_job(job_id, status="running", message="Pipeline started")

    cmd = _build_command(job.source_type, Path(job.input_path), job.run_id, job.allowed_categories)
    result = subprocess.run(
        cmd,
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    run_dir = RUNS_DIR / job.run_id
    artifact_names = _collect_artifacts(run_dir)
    manifest_fields = _load_manifest_fields(run_dir)

    if result.returncode == 0:
        _update_job(
            job_id,
            status="completed",
            return_code=result.returncode,
            message="Pipeline completed",
            output_dir=str(run_dir),
            artifact_names=artifact_names,
            stdout=result.stdout,
            stderr=result.stderr,
            codegen_policy_snapshot=manifest_fields["codegenPolicySnapshot"],
            runtime_fingerprint=manifest_fields["runtimeFingerprint"],
        )
        return

    _update_job(
        job_id,
        status="failed",
        return_code=result.returncode,
        message="Pipeline failed",
        output_dir=str(run_dir),
        artifact_names=artifact_names,
        stdout=result.stdout,
        stderr=result.stderr,
        codegen_policy_snapshot=manifest_fields["codegenPolicySnapshot"],
        runtime_fingerprint=manifest_fields["runtimeFingerprint"],
    )


@app.get("/health")
def health() -> Dict[str, object]:
    return {
        "status": "ok",
        "codegenEnforcementMode": CODEGEN_ENFORCEMENT_MODE,
        "codegenEnforcementLocation": CODEGEN_ENFORCEMENT_LOCATION,
        "knownAllowedCategories": get_known_allowed_categories(),
    }


@app.get("/", response_class=HTMLResponse)
def home():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(path=str(index_file), filename="index.html")
    return HTMLResponse(content="<h1>Upload UI not found</h1>", status_code=404)


@app.post("/api/v1/ingest")
async def ingest(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    allowedCategories: str = Form(""),
) -> Dict[str, object]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    suffix = Path(file.filename).suffix.lower()
    source_type = ALLOWED_EXTENSIONS.get(suffix)
    if not source_type:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS.keys()))
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {allowed}")

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    job_id = uuid.uuid4().hex
    run_id = datetime.now(timezone.utc).strftime("run-%Y%m%d-%H%M%S") + f"-{job_id[:8]}"
    job_dir = UPLOADS_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(file.filename).name
    input_path = job_dir / safe_name
    raw_allowed_categories = [item.strip() for item in allowedCategories.split(",") if item.strip()]
    try:
        allowed_categories = validate_allowed_categories(raw_allowed_categories)
    except ValueError as exc:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise HTTPException(status_code=400, detail=str(exc))

    size = 0
    with input_path.open("wb") as target:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                target.close()
                input_path.unlink(missing_ok=True)
                shutil.rmtree(job_dir, ignore_errors=True)
                raise HTTPException(status_code=413, detail="Uploaded file exceeds size limit")
            target.write(chunk)

    created_at = _now_iso()
    JOBS[job_id] = JobState(
        job_id=job_id,
        run_id=run_id,
        status="queued",
        source_type=source_type,
        filename=safe_name,
        created_at_utc=created_at,
        updated_at_utc=created_at,
        input_path=str(input_path),
        allowed_categories=allowed_categories,
    )

    background_tasks.add_task(_run_pipeline_job, job_id)

    return {
        "jobId": job_id,
        "runId": run_id,
        "status": "queued",
        "allowedCategories": allowed_categories,
        "effectiveAllowedCategories": allowed_categories,
        "codegenEnforcementMode": CODEGEN_ENFORCEMENT_MODE,
        "codegenEnforcementLocation": CODEGEN_ENFORCEMENT_LOCATION,
    }


@app.get("/api/v1/jobs/{job_id}")
def get_job(job_id: str) -> Dict[str, object]:
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "jobId": job.job_id,
        "runId": job.run_id,
        "status": job.status,
        "sourceType": job.source_type,
        "filename": job.filename,
        "createdAtUtc": job.created_at_utc,
        "updatedAtUtc": job.updated_at_utc,
        "allowedCategories": job.allowed_categories,
        "returnCode": job.return_code,
        "message": job.message,
        "outputDir": job.output_dir,
        "artifactNames": job.artifact_names,
        "stdout": job.stdout,
        "stderr": job.stderr,
        "codegenEnforcementMode": CODEGEN_ENFORCEMENT_MODE,
        "codegenEnforcementLocation": CODEGEN_ENFORCEMENT_LOCATION,
        "codegenPolicySnapshot": job.codegen_policy_snapshot,
        "runtimeFingerprint": job.runtime_fingerprint,
    }


@app.get("/api/v1/runs/{run_id}/artifacts")
def list_artifacts(run_id: str) -> Dict[str, object]:
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists() or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail="Run not found")

    artifacts = [name for name in _collect_artifacts(run_dir) if name in ALLOWED_ARTIFACTS]
    return {
        "runId": run_id,
        "artifacts": artifacts,
    }


@app.get("/api/v1/runs/{run_id}/artifacts/{name}")
def download_artifact(run_id: str, name: str) -> FileResponse:
    if name not in ALLOWED_ARTIFACTS:
        raise HTTPException(status_code=400, detail="Artifact is not downloadable")

    target = RUNS_DIR / run_id / name
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")

    return FileResponse(path=str(target), filename=name)
