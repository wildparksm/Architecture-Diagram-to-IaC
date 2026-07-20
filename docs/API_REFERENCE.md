# API Reference

Architecture Diagram to IaC Compiler의 REST API 명세서입니다.  
FastAPI의 자동 생성 docs도 `/docs` (Swagger UI) 및 `/redoc` (ReDoc)에서 확인할 수 있습니다.

---

## 공통 사항

| 항목 | 값 |
|---|---|
| Base URL | `http://localhost:8000` (로컬 실행 기준) |
| 서버 실행 | `uvicorn src.api_server:app --reload` |
| Content-Type | 특별 명시 없으면 `application/json` |
| 최대 업로드 크기 | 100 MB |

---

## Endpoints

### `GET /health`

**설명**: 서버 상태 및 현재 정책 enforcement 정보 반환.

**응답 예시**:
```json
{
  "status": "ok",
  "codegenEnforcementMode": "runner-pre-filter",
  "codegenEnforcementLocation": "src/run_pptx_evidence.py, src/run_drawio_evidence.py",
  "knownAllowedCategories": [
    "azure.networkBundle",
    "azure.virtualNetwork",
    "azure.networkSecurityGroup",
    "azure.routeTable",
    "azure.logAnalyticsWorkspace",
    "azure.firewall",
    "azure.avdBundle",
    "azure.avdWorkspace",
    "azure.avdHostPool",
    "azure.avdApplicationGroup"
  ]
}
```

**필드 설명**:

| 필드 | 타입 | 설명 |
|---|---|---|
| `status` | string | `"ok"` 고정 |
| `codegenEnforcementMode` | string | 정책 적용 방식. 현재 `"runner-pre-filter"` |
| `codegenEnforcementLocation` | string | authoritative enforcement 위치 경로 |
| `knownAllowedCategories` | string[] | 허용 가능한 전체 카테고리 목록 |

---

### `POST /api/v1/ingest`

**설명**: 다이어그램 파일을 업로드하고 파이프라인 잡을 생성합니다.

**Content-Type**: `multipart/form-data`

**요청 필드**:

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `file` | file | ✅ | 업로드할 다이어그램 파일 (`.pptx`, `.drawio`, `.xml`) |
| `allowedCategories` | string | ❌ | 허용 카테고리 쉼표 구분 목록 (예: `"azure.networkBundle,azure.virtualNetwork"`) |

**성공 응답** (`202` 또는 `200`):
```json
{
  "jobId": "a3f1c8e2b04d4b9e9c1a2d3e4f5a6b7c",
  "runId": "run-20260720-104500-a3f1c8e2",
  "status": "queued",
  "allowedCategories": ["azure.networkBundle"],
  "effectiveAllowedCategories": ["azure.networkBundle"],
  "codegenEnforcementMode": "runner-pre-filter",
  "codegenEnforcementLocation": "src/run_pptx_evidence.py, src/run_drawio_evidence.py"
}
```

**오류 응답**:

| 코드 | 조건 | 예시 |
|---|---|---|
| `400` | 파일명 없음 | `{"detail": "Missing filename"}` |
| `400` | 지원하지 않는 파일 형식 | `{"detail": "Unsupported file type. Allowed: .drawio, .pptx, .xml"}` |
| `400` | 알 수 없는 allowedCategory | `{"detail": "Unsupported allow categories: azure.notReal. Allowed categories: ..."}` |
| `413` | 파일 크기 초과 (100MB) | `{"detail": "Uploaded file exceeds size limit"}` |

**필드 설명**:

| 필드 | 타입 | 설명 |
|---|---|---|
| `jobId` | string | 잡 식별자 (UUID hex) |
| `runId` | string | 산출물 저장 폴더명 (`runs/{runId}/`) |
| `status` | string | `"queued"` (백그라운드 실행 대기) |
| `allowedCategories` | string[] | 검증 후 정규화된 요청 카테고리 목록 |
| `effectiveAllowedCategories` | string[] | 실제 적용되는 카테고리 (현재는 `allowedCategories`와 동일) |
| `codegenEnforcementMode` | string | 정책 적용 방식 |
| `codegenEnforcementLocation` | string | authoritative enforcement 위치 경로 |

---

### `GET /api/v1/jobs/{jobId}`

**설명**: 잡 상태 및 결과를 조회합니다.

**경로 파라미터**: `jobId` — `/api/v1/ingest` 응답에서 받은 `jobId`.

**응답 예시 (완료)**:
```json
{
  "jobId": "a3f1c8e2b04d4b9e9c1a2d3e4f5a6b7c",
  "runId": "run-20260720-104500-a3f1c8e2",
  "status": "completed",
  "sourceType": "pptx",
  "filename": "Architecture Diagram to IaC Compiler.pptx",
  "createdAtUtc": "2026-07-20T01:45:00.000000+00:00",
  "updatedAtUtc": "2026-07-20T01:45:12.000000+00:00",
  "allowedCategories": ["azure.networkBundle"],
  "returnCode": 0,
  "message": "Pipeline completed",
  "outputDir": "/path/to/runs/run-20260720-104500-a3f1c8e2",
  "artifactNames": [
    "architecture.graph.json",
    "architecture.ir.json",
    "iac-readiness-report.md",
    "main.bicep",
    "raw-evidence.json",
    "run-manifest.json",
    "traceability-matrix.csv",
    "unresolved-questions.md",
    "validation-report.md"
  ],
  "stdout": "...",
  "stderr": "",
  "codegenEnforcementMode": "runner-pre-filter",
  "codegenEnforcementLocation": "src/run_pptx_evidence.py, src/run_drawio_evidence.py",
  "codegenPolicySnapshot": {
    "enforcementMode": "runner-pre-filter",
    "enforcementLocation": "src/run_pptx_evidence.py",
    "requestedAllowedCategories": ["azure.networkBundle"],
    "effectiveAllowedCategories": ["azure.networkBundle"]
  },
  "runtimeFingerprint": {
    "pythonVersion": "3.11.x",
    "pythonExecutable": "/usr/bin/python3.11",
    "platform": "linux",
    "moduleFiles": {
      "runner": {"path": "src/run_pptx_evidence.py", "sha256": "abcd1234..."},
      "emitter": {"path": "src/emitters/bicep_emitter.py", "sha256": "efgh5678..."},
      "policy": {"path": "src/policy/codegen_policy.py", "sha256": "ijkl9012..."}
    }
  }
}
```

**`status` 값**:

| 값 | 설명 |
|---|---|
| `queued` | 잡 생성됨, 아직 실행 전 |
| `running` | 파이프라인 실행 중 |
| `completed` | 정상 완료 (`returnCode: 0`) |
| `failed` | 실패 (`returnCode != 0`) |

**오류 응답**:

| 코드 | 조건 |
|---|---|
| `404` | jobId가 존재하지 않음 |

**`codegenPolicySnapshot` 필드 설명**:

| 필드 | 타입 | 설명 |
|---|---|---|
| `enforcementMode` | string | 적용 방식 |
| `enforcementLocation` | string | authoritative 실행 파일 경로 |
| `requestedAllowedCategories` | string[] | 요청에서 전달된 카테고리 |
| `effectiveAllowedCategories` | string[] | 실제 runner가 적용한 카테고리 |

**`runtimeFingerprint` 필드 설명**:

| 필드 | 타입 | 설명 |
|---|---|---|
| `pythonVersion` | string | 실행 시 Python 버전 |
| `pythonExecutable` | string | Python 바이너리 경로 |
| `platform` | string | OS 플랫폼 |
| `moduleFiles` | object | runner/emitter/policy 파일 경로 + SHA-256 해시 |

---

### `GET /api/v1/runs/{runId}/artifacts`

**설명**: run에서 다운로드 가능한 아티팩트 목록을 반환합니다.

**경로 파라미터**: `runId` — 잡 응답의 `runId` 또는 `runs/` 폴더명.

**응답 예시**:
```json
{
  "runId": "run-20260720-104500-a3f1c8e2",
  "artifacts": [
    "architecture.graph.json",
    "architecture.ir.json",
    "iac-readiness-report.md",
    "main.bicep",
    "raw-evidence.json",
    "run-manifest.json",
    "traceability-matrix.csv",
    "unresolved-questions.md",
    "validation-report.md"
  ]
}
```

**오류 응답**:

| 코드 | 조건 |
|---|---|
| `404` | runId 폴더가 존재하지 않음 |

---

### `GET /api/v1/runs/{runId}/artifacts/{name}`

**설명**: 아티팩트 파일을 다운로드합니다.

**경로 파라미터**:
- `runId`: run 식별자
- `name`: 아티팩트 파일명

**허용 아티팩트 목록** (다운로드 가능한 파일):

| 파일명 | 설명 |
|---|---|
| `raw-evidence.json` | 원시 증거 레코드 |
| `architecture.graph.json` | 재구성된 아키텍처 그래프 |
| `architecture.ir.json` | Provider-neutral IR |
| `main.bicep` | 생성된 Bicep 초안 |
| `traceability-matrix.csv` | 추적성 매트릭스 |
| `iac-readiness-report.md` | IaC 준비도 리포트 |
| `unresolved-questions.md` | 미해결 질문 목록 |
| `validation-report.md` | 검증 리포트 |
| `run-manifest.json` | 실행 메타데이터 (정책 스냅샷 + 런타임 핑거프린트 포함) |
| `deployable-resources.md` | 배포 가능 리소스 요약 |

**오류 응답**:

| 코드 | 조건 |
|---|---|
| `400` | 허용 목록에 없는 파일명 |
| `404` | 파일이 존재하지 않음 |

---

## 정책 카테고리 목록

### SAFE (기본 허용 권장)

| 카테고리 | 설명 |
|---|---|
| `azure.networkBundle` | VNet + NSG + RouteTable 묶음 |
| `azure.virtualNetwork` | Azure Virtual Network |
| `azure.networkSecurityGroup` | Azure NSG |
| `azure.routeTable` | Azure Route Table |
| `azure.logAnalyticsWorkspace` | Log Analytics Workspace |

### RISKY / MANUAL (명시적 허용 필요)

| 카테고리 | 설명 |
|---|---|
| `azure.firewall` | Azure Firewall (고위험 — 수동 검토 권장) |
| `azure.avdBundle` | AVD 전체 묶음 |
| `azure.avdWorkspace` | AVD Workspace |
| `azure.avdHostPool` | AVD Host Pool |
| `azure.avdApplicationGroup` | AVD Application Group |

> **주의**: `allowedCategories`를 빈 값으로 두면 `report-only` 모드가 활성화되어 Azure 리소스 코드가 생성되지 않습니다.

---

## 운영 참고

### 정책 enforcement 흐름

```
POST /api/v1/ingest
  → validate_allowed_categories()  ← 알 수 없는 카테고리 → 400 즉시 반환
  → Job queued
  → runner pre-filter              ← Azure 리소스 필터링 (authoritative)
  → emitter (후속 처리)
  → manifest 기록 (snapshot + fingerprint)
```

### 문제 진단 체크리스트

1. **잡이 `failed` 상태**: `stderr` 필드 확인 → `policy_validation_error` 또는 파이프라인 오류 메시지 확인
2. **예상과 다른 Bicep 생성**: `codegenPolicySnapshot.effectiveAllowedCategories` 필드 확인
3. **drift 의심**: `runtimeFingerprint.moduleFiles` SHA-256 비교 → `docs/EMITTER_DRIFT_RCA.md` 참조

---

*최종 업데이트: 2026-07-20*
