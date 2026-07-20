# Architecture Diagram to IaC Compiler

## 프로젝트 시작점
이 프로젝트는 다이어그램의 픽셀을 바로 코드로 변환하지 않고, 증거 기반으로 아키텍처 의도를 복원한 뒤 Provider-neutral IR을 통해 자동화 산출물을 생성하는 것을 목표로 한다.

현재 기준 자료:
- `Architecture Diagram to IaC Compiler.pptx` (17장)
- `POWERPOINT_COPILOT_AUGMENTATION_PROMPT.md` (보강 요구사항 및 확장 방향)

## 핵심 원칙
- Metadata-first, VLM-second
- Multi-extractor + Evidence Registry + Reconciliation
- Provider-neutral Core IR
- Question/Approval Gate 기반 무음 기본값 금지
- Traceability: Source -> Evidence -> IR -> Code -> Validation

## 초기 MVP 범위
입력:
- PPTX
- draw.io XML
- PNG/JPG (보조)

현재 입력 방식:
- CLI 기반 파일 경로 입력(로컬/워크스페이스 파일)
- 프론트 업로드 페이지 연동은 진행 중이며, 백엔드 업로드 API MVP를 먼저 구현함 (`src/api_server.py`)

이해 대상:
- Node/Edge/Container/Text/Legend
- Azure 주요 리소스 + Generic On-prem 요소

출력:
- `raw-evidence.json`
- `element-registry.json`
- `architecture.graph.json`
- `architecture.ir.json`
- `unresolved-questions.md`
- `traceability-matrix.csv`
- `main.bicep` 또는 Terraform
- `validation-report.md`

## 문서 인덱스
- `docs/ANTIGRAVITY_HANDOFF_2026-07-20.md` ← 최신 인수인계 문서
- `docs/API_REFERENCE.md` ← API 운영자 레퍼런스
- `docs/BIG_PICTURE_TRANSITION_PLAN.md`
- `docs/EMITTER_DRIFT_RCA.md`
- `docs/OPERATIONS_RELEASE_CHECKLIST.md`
- `docs/POLICY_ENFORCEMENT_CHECKLIST.md`
- `docs/PROJECT_KICKOFF.md`
- `docs/MVP_BACKLOG.md`
- `docs/SLIDE_TO_WORKSTREAM_MAPPING.md`

## 현재 상태 (2026-07-20 기준)
운영 베이스라인 달성. 정책 기반 안전 생성 파이프라인 동작 중.
- QUALITY_GATES=PASS 확인
- Runner pre-filter authoritative 확정
- API + UI 정책 가시성 구현 완료

## 다음 우선 작업
- **P0**: `.github/workflows/policy-quality-gates.yml` CI 게이트 활성화 (GitHub 연동 필요)
- **P1**: golden input 3종으로 run snapshot diff 자동화
- **P1**: UI knownAllowedCategories 도움말 패널 추가
- **P2**: emitter 로직 책임 분리 + drift 탐지 자동 경고

자세한 내용은 `docs/ANTIGRAVITY_HANDOFF_2026-07-20.md` 참조.

## 운영 스크립트
- 품질 게이트 실행: `python scripts/run_policy_quality_gates.py`
- 릴리즈 증적 패키징: `python scripts/package_release_evidence.py --run-id <run-id>`
- API 서버 실행: `uvicorn src.api_server:app --reload`

## CI
- `.github/workflows/policy-quality-gates.yml` — PR 및 main 브랜치 push 시 품질 게이트 자동 실행
