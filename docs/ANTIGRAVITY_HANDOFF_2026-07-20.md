# Antigravity Handoff (2026-07-20)

## 목적
이 문서는 현재 프로젝트를 Antigravity 환경에서 즉시 이어서 작업할 수 있도록, 기술 맥락/아키텍처/완료 내역/검증 상태/운영 절차/남은 리스크/다음 액션을 한 번에 전달하기 위한 인수인계 문서다.

---

## 1) 프로젝트 한 줄 요약
다이어그램(PPTX, draw.io)을 증거 기반으로 해석하여 Provider-neutral IR로 변환하고, 정책(allowlist) 통제를 거쳐 Bicep 초안을 생성하는 파이프라인이다.

핵심은 "무조건 많이 생성"이 아니라 "정책에 맞는 것만 안전하게 생성"이다.

---

## 2) 현재 상태 스냅샷

### 운영/정책 관점
- 정책 authoritative 경로: runner pre-filter (확정)
- 기본 동작: report-only (allowlist 비어 있으면 Azure 코드 생성 억제)
- 허용 카테고리 검증: CLI/API 모두 fail-fast
- 정책 적용 증명: run-manifest에 policy snapshot + runtime fingerprint 저장
- 운영 가시성: API/job payload/UI에서 enforcement 및 snapshot 확인 가능

### 최신 검증된 실행
- 정책 회귀 실행: `python scripts/run_policy_quality_gates.py`
  - 결과: `QUALITY_GATES=PASS`
  - 내역:
    - 회귀 3시나리오 통과
    - invalid category 입력 시 runner exit code 2 확인
- 릴리즈 증적 패키징:
  - 명령: `python scripts/package_release_evidence.py --run-id run-20260716-050127`
  - 생성: `runs/run-20260716-050127/release-evidence-run-20260716-050127.zip`
  - 포함 아티팩트 확인 완료

---

## 3) 아키텍처 개요

### 파이프라인 흐름
1. Input Adapter
- PPTX: `src/run_pptx_evidence.py` -> `adapters.pptx_adapter`
- draw.io: `src/run_drawio_evidence.py` -> `adapters.drawio_adapter`

2. Evidence Validation
- `validators.raw_evidence_validator.validate_records`
- 에러/통과 결과는 `validation-report.md`에 기록

3. Graph + IR
- Graph: `graph.reconstruction.build_graph`
- IR: `ir.compiler.compile_ir`
- Question Gate: `reports.questions.collect_questions`

4. Policy Injection + Enforcement
- IR에 `codegenPolicy.allowedCategories` 반영
- Runner에서 Azure resource pre-filter (authoritative)
- Emitter는 후속 처리 계층 (runner가 안전 게이트)

5. Emission + Reports
- Bicep: `emitters.bicep_emitter.emit_bicep`
- Traceability: `reports.traceability`
- Readiness: `reports.readiness`
- Questions report: unresolved-questions
- Manifest: run metadata + policy/runtime fingerprint

---

## 4) 디렉터리/주요 파일

### 핵심 엔트리
- `src/run_pptx_evidence.py`
- `src/run_drawio_evidence.py`
- `src/api_server.py`
- `src/static/index.html`

### 정책/검증
- `src/policy/codegen_policy.py`
- `tests/test_policy_regression.py`
- `scripts/run_policy_quality_gates.py`

### 운영 증적
- `scripts/package_release_evidence.py`
- `docs/POLICY_ENFORCEMENT_CHECKLIST.md`
- `docs/OPERATIONS_RELEASE_CHECKLIST.md`
- `docs/EMITTER_DRIFT_RCA.md`

---

## 5) 정책 모델 상세

### 허용 카테고리
`src/policy/codegen_policy.py`

- SAFE
  - azure.networkBundle
  - azure.virtualNetwork
  - azure.networkSecurityGroup
  - azure.routeTable
  - azure.logAnalyticsWorkspace

- RISKY/MANUAL
  - azure.firewall
  - azure.avdBundle
  - azure.avdWorkspace
  - azure.avdHostPool
  - azure.avdApplicationGroup

### 검증 함수
- `validate_allowed_categories(values)`
  - normalize + unknown 탐지
  - unknown 존재 시 ValueError

### 실패 동작
- CLI runner: invalid category -> stderr에 `policy_validation_error=...`, exit code 2
- API ingest: invalid category -> HTTP 400 + detail 메시지

---

## 6) API 계약 (현재)

### GET /health
응답 주요 필드:
- status
- codegenEnforcementMode
- codegenEnforcementLocation
- knownAllowedCategories (배열)

### POST /api/v1/ingest
폼 필드:
- file (multipart)
- allowedCategories (comma-separated string)

응답 주요 필드:
- jobId
- runId
- status
- allowedCategories
- effectiveAllowedCategories
- codegenEnforcementMode
- codegenEnforcementLocation

### GET /api/v1/jobs/{jobId}
응답 주요 필드:
- status, stdout, stderr, artifactNames
- codegenEnforcementMode, codegenEnforcementLocation
- codegenPolicySnapshot
- runtimeFingerprint

### GET /api/v1/runs/{runId}/artifacts
- 허용 아티팩트 목록 반환

### GET /api/v1/runs/{runId}/artifacts/{name}
- 개별 아티팩트 다운로드

---

## 7) UI 상태 (src/static/index.html)

현재 화면에서 확인 가능한 것:
- health/enforcement badge
- allowlist 선택 + 고급 입력(advanced)
- 업로드/잡 상태/로그/아티팩트
- timeline
- allowlist compliance summary
- policy snapshot 카드
  - requested/effective categories
  - runtime platform
  - runner/emitter/policy hash (축약)

추가된 안전 장치:
- 업로드 전 preflight category validation
  - /health에서 받은 knownAllowedCategories 기준으로 advanced 입력 검증
  - unknown category가 있으면 업로드 차단 + UI에 즉시 이유 표시

---

## 8) 산출물 규격 (run 폴더)

각 run 기본 산출물:
- raw-evidence.json
- architecture.graph.json
- architecture.ir.json
- main.bicep
- traceability-matrix.csv
- iac-readiness-report.md
- unresolved-questions.md
- validation-report.md
- run-manifest.json

manifest 핵심 필드:
- codegenPolicySnapshot
  - enforcementMode
  - enforcementLocation
  - requestedAllowedCategories
  - effectiveAllowedCategories
- runtimeFingerprint
  - pythonVersion
  - pythonExecutable
  - platform
  - moduleFiles (runner/emitter/policy path + sha256)

---

## 9) 자동화/테스트

### 정책 회귀 테스트
파일: `tests/test_policy_regression.py`

시나리오:
1. report-only
2. networkBundle only
3. composite allowlist

검증:
- main.bicep에 firewall/avd hostpool 토큰 미포함
- manifest snapshot/runtime 필드 존재
- effective allowlist 값 일치

실행:
- `python -m unittest discover -s tests -p "test_policy_regression.py"`

### 품질 게이트 스크립트
파일: `scripts/run_policy_quality_gates.py`

동작:
1. 정책 회귀 테스트 실행
2. invalid category gate(exit code 2) 검증
3. PASS/FAIL 한 줄 요약

실행:
- `python scripts/run_policy_quality_gates.py`

---

## 10) 릴리즈 증적 패키징

파일: `scripts/package_release_evidence.py`

실행:
- `python scripts/package_release_evidence.py --run-id <run-id>`

기본 포함 파일:
- run-manifest.json
- main.bicep
- validation-report.md
- iac-readiness-report.md
- traceability-matrix.csv
- unresolved-questions.md
- architecture.ir.json
- release-evidence-summary.md (자동 생성)

summary 포함 내용:
- firewallDeclared/avdHostPoolDeclared
- enforcementMode
- requested/effective allowlist
- runtimePlatform

---

## 11) 알려진 이슈/리스크

1. Emitter 드리프트 이력
- 과거 source/runtime 체감 불일치 이슈가 있었음
- 현재는 runner pre-filter가 authoritative이므로 안전성은 확보
- 관련 문서: `docs/EMITTER_DRIFT_RCA.md`

2. FastAPI TestClient 경고
- starlette/httpx 관련 deprecation warning 출력 가능
- 기능상 blocker는 아님

3. 저장소 상태
- 현재 작업 경로는 git repo로 인식되지 않음 (`git status` 실패)
- Antigravity에서 버전 관리 연동 시 초기 설정 확인 필요

---

## 12) Antigravity에서 바로 시작하는 절차

### A. 환경 준비
1. Python 3.11 사용
2. 의존성 설치
- `pip install -r requirements.txt`

### B. 품질 게이트 먼저 실행
- `python scripts/run_policy_quality_gates.py`
- 기대값: `QUALITY_GATES=PASS`

### C. API 서버 실행
- `uvicorn src.api_server:app --reload`
- 브라우저 확인:
  - `/` (업로드 UI)
  - `/health` (enforcement + known categories)

### D. 샘플 업로드 점검
- draw.io 또는 PPTX 업로드
- 잡 완료 후:
  - policy snapshot 카드 확인
  - 아티팩트 다운로드 확인

### E. 릴리즈 증적 묶기
- `python scripts/package_release_evidence.py --run-id <생성된 run-id>`

---

## 13) 권장 다음 작업 (우선순위)

P0
1. CI에 `run_policy_quality_gates.py` 연결 (PR/merge 게이트)
2. API 응답 스키마 문서화(OpenAPI 예시 + 운영자 문서)

P1
1. golden input 3종 이상으로 run snapshot diff 자동화
2. UI에서 knownAllowedCategories를 별도 도움말 패널로 표시

P2
1. emitter 로직 책임 분리(분류/억제/출력 단 분리)
2. drift 탐지 이벤트를 validation-report에 자동 경고로 반영

---

## 14) 실행 예시 커맨드 모음

정책 회귀:
- `python -m unittest discover -s tests -p "test_policy_regression.py"`

품질 게이트:
- `python scripts/run_policy_quality_gates.py`

PPTX 수동 실행:
- `python src/run_pptx_evidence.py --input "Architecture Diagram to IaC Compiler.pptx" --allow-category azure.networkBundle`

draw.io 수동 실행:
- `python src/run_drawio_evidence.py --input "samples/simple.drawio" --allow-category azure.networkBundle`

릴리즈 증적 패키징:
- `python scripts/package_release_evidence.py --run-id run-20260716-050127`

API 서버 실행:
- `uvicorn src.api_server:app --reload`

---

## 15) 결론
현재 프로젝트는 "정책 기반 안전 생성" 관점에서 실사용 가능한 운영 베이스라인에 도달했다.
Antigravity에서는 CI 게이트화와 운영 자동화(증적/드리프트 모니터링)를 우선 진행하면 된다.

핵심 원칙은 유지한다:
- runner pre-filter는 안전 게이트로 고정
- 정책/런타임 증적은 항상 manifest/API/UI에서 즉시 확인 가능해야 함
