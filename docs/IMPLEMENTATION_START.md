# Implementation Start

## 오늘 시작할 작업
1. PPTX Adapter 최소 구현
- 대상: 텍스트/도형/커넥터 단서 추출
- 출력: `runs/<run-id>/raw-evidence.json`

2. Evidence Validation
- `schemas/raw-evidence.schema.json`으로 검증
- 실패 건은 `runs/<run-id>/validation-report.md`에 기록

3. Question Gate 생성
- confidence 하한 미달 항목을 `unresolved-questions.md`에 기록
- Blocker가 존재하면 `production-ready=false`로 명시

## 첫 실행 기준
- 입력 파일: `Architecture Diagram to IaC Compiler.pptx`
- 목표 슬라이드: 1~17
- 성공 조건:
  - slide/object/source provenance가 모두 채워짐
  - confidence 6차원 값이 누락 없이 기록됨
  - schema validation 100% 통과

## 산출물 경로 규칙
- `runs/<run-id>/raw-evidence.json`
- `runs/<run-id>/unresolved-questions.md`
- `runs/<run-id>/validation-report.md`
- `runs/<run-id>/run-manifest.json`

## 진행 상태 (2026-07-15)
- 상태: P1 확장 완료 (PPTX + draw.io 파이프라인, 질문 게이트, 추적성/준비도 리포트)
- 실행 입력 1: `Architecture Diagram to IaC Compiler.pptx`
- 최근 실행 ID 1: `run-20260715-073322`
- 생성 레코드 수 1: 542
- 그래프 노드/엣지 1: 511 / 31
- 질문 수 1: 238 (Risk 33 / Optional 205)
- IR 리소스 수 1: 119
- unknown 노이즈 감소 1: 505 -> 113
- 실행 입력 2: `samples/simple.drawio`
- 최근 실행 ID 2: `run-20260715-041428`
- 생성 레코드 수 2: 5
- 그래프 노드/엣지 2: 2 / 1
- 질문 수 2: 1
- 검증 결과: PASSED
- 게이트 정책: `blocker > 0` 또는 `risk > 200`이면 production-ready = NO
- 코드 산출물: 각 run에 `main.bicep` 초안 자동 생성 및 traceability 라인 매핑 완료
- 최신 PPTX gate 결과: production-ready = YES
- 최신 PPTX Bicep 구성: 실제 Azure resource 선언 + contextualAzureResources + deferredAzureResources + inferredResources
- 최신 PPTX deferred scaffold: Azure Firewall용 주석 기반 Bicep 힌트 자동 생성
- 최신 PPTX bundle scaffold: `VNet / Subnet / NSG / Route Table`, `AVD Workspace / Host Pool / App Group` 실제 scaffold 선언으로 승격
- 최신 PPTX 분류 개선: 슬라이드 제목/서술 문장/메타 라벨을 unknown 리소스 후보에서 제외하는 필터 적용
- 프론트 업로드 연동 상태: 1차 API 구현 완료 (`src/api_server.py`, `/api/v1/ingest`, `/api/v1/jobs/{jobId}`, `/api/v1/runs/{runId}/artifacts`)
- 프론트 업로드 연동 상태: 업로드 UI 1차 구현 완료 (`src/static/index.html`, `GET /`)
- 최신 PPTX dedupe 개선: `azure.avdBundle` 우선 규칙 적용으로 standalone `azure.avdHostPool`은 `deduplicatedAzureResources`에 기록
- 최신 PPTX firewall 개선: `azure.firewall`을 deferred에서 실제 scaffold resource(공인 IP/정책/VNet+AzureFirewallSubnet/Azure Firewall)로 승격
- 코드 생성 정책: 기본 report-only, allowlist가 전달된 경우에만 Bicep emission

생성 산출물 (PPTX run):
- `runs/run-20260715-073322/raw-evidence.json`
- `runs/run-20260715-073322/architecture.graph.json`
- `runs/run-20260715-073322/architecture.ir.json`
- `runs/run-20260715-073322/main.bicep`
- `runs/run-20260715-073322/deployable-resources.md`
- `runs/run-20260715-073322/traceability-matrix.csv`
- `runs/run-20260715-073322/iac-readiness-report.md`
- `runs/run-20260715-073322/unresolved-questions.md`
- `runs/run-20260715-073322/validation-report.md`
- `runs/run-20260715-073322/run-manifest.json`

생성 산출물 (draw.io run):
- `runs/run-20260715-041428/raw-evidence.json`
- `runs/run-20260715-041428/architecture.graph.json`
- `runs/run-20260715-041428/architecture.ir.json`
- `runs/run-20260715-041428/main.bicep`
- `runs/run-20260715-041428/traceability-matrix.csv`
- `runs/run-20260715-041428/iac-readiness-report.md`
- `runs/run-20260715-041428/unresolved-questions.md`
- `runs/run-20260715-041428/validation-report.md`
- `runs/run-20260715-041428/run-manifest.json`

백엔드 API 산출물:
- `src/api_server.py`
- `requirements.txt`

프론트 업로드 산출물:
- `src/static/index.html`
