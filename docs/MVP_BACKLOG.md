# MVP Backlog

## P0 (즉시 착수)
1. Repository Skeleton 생성
- `src/adapters`, `src/extractors`, `src/graph`, `src/ir`, `src/emitters`, `src/validators`, `src/reports`
- `tests`, `schemas`, `samples`, `runs`

2. Evidence Schema v0.1 정의
- Raw Evidence 필드 표준화
- provenance, geometry, confidence dimensions 포함

3. PPTX Adapter 최소 기능
- shape text 추출
- object ID + slide/page 추출
- connector endpoint 후보 추출

4. Evidence Registry 구현
- stable ID 부여 규칙
- 중복 병합 규칙 초안

5. Question Service v0
- Blocker/Risk/Optional/Manual/Conflict/Unsupported 분류
- unresolved-questions.md 생성

## P1 (MVP 코어)
1. Graph Reconstruction v0
- explicit connector binding
- endpoint proximity + direction
- ambiguity penalty 적용

2. Provider-neutral IR Compiler v0
- resources, relationships, zones, securityControls, questions

3. Azure Bicep Emitter v0
- Resource Group, VNet, Subnet, NSG 중심

4. Validation Runner v0
- Schema validation
- Graph invariant validation
- Bicep lint/build

## P2 (MVP 확장)
1. Terraform AzureRM Emitter v0
2. draw.io XML Adapter v0
3. Traceability Matrix 자동 생성
4. iac-readiness-report.md 자동 생성

## P3 (품질 및 운영)
1. Golden Dataset 9종 구축
2. 메트릭 리포트 자동화 (precision/recall/F1 등)
3. run-manifest 재현성 검사
4. CI 파이프라인 기본형

## P4 (운영 전환 큰그림)
1. 정책 단일화: codegen enforcement authoritative 경로 확정 (runner vs emitter)
2. Drift 제어: 모듈 checksum/runtime fingerprint를 run-manifest에 기록
3. 운영 UX: health/enforcement/timeline + allowlist 준수 요약 카드 고도화
4. 릴리즈 준비: 베타 체크리스트 및 주간 릴리즈 노트 템플릿 정착

## 제외 범위 (현재)
- 자동 배포 실행
- 온프렘 전체 완전 자동화 표현
- 멀티클라우드 코드 생성 정식 지원
