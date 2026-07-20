# Project Kickoff

## 1. 프로젝트 목적
"그림을 코드로"가 아니라 "아키텍처 의도를 검증 가능한 자동화 패키지로 컴파일"하는 플랫폼을 만든다.

핵심 파이프라인:
- Diagram Sources
- Understanding Engine
- Provider-neutral Architecture IR
- Automation Outputs

## 2. 문제 정의
- 다이어그램 소스가 PPTX/draw.io/PDF/이미지로 분산됨
- 연결선, 경계, 범례 의미가 누락되기 쉬움
- 추론과 원본 사실이 섞이면 배포 코드 오류 위험이 큼
- 온프렘/하이브리드 자산은 IaC 단독으로 완결되지 않음

## 3. 설계 원칙
- Deterministic evidence 우선
- VLM 결과는 candidate/hypothesis로만 저장
- 충돌은 confidence + provenance 기반 병합
- Blocker 질문 미해결 시 Production-ready 출력 금지
- 모든 산출물은 run manifest로 재현 가능해야 함

## 4. MVP 산출물 계약
필수 산출물:
- raw-evidence.json
- element-registry.json
- architecture.graph.json
- architecture.ir.json
- unresolved-questions.md
- traceability-matrix.csv
- iac-readiness-report.md
- main.bicep 또는 Terraform
- validation-report.md
- run-manifest.json

## 5. 성공 기준 (초기)
- editable source 기준 node recall >= 95%
- edge F1 >= 90%
- hallucinated edge rate <= 1%
- blocker silent-default count = 0
- traceability coverage = 100%

## 6. 운영 원칙
- 코드 생성과 배포 실행을 분리
- 미지원 항목 삭제 금지, Manual/Unsupported로 유지
- 모델/파서/프롬프트 버전 기록
- 민감정보는 IR에 저장 금지
