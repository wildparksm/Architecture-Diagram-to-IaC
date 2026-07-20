# Big Picture Transition Plan

## Why now
현재 MVP는 증거 추출, IR 컴파일, 리포트 생성, 업로드 UI/API, allowlist 기반 코드 생성 통제를 이미 갖추었다.
다음 단계는 기능 추가보다 운영 신뢰성과 정책 일관성을 높이는 전환이다.

## North Star (다음 4~6주)
- 정책 통제 일관성: report-only 기본 + allowlist 예외 규칙이 모든 경로에서 동일하게 보장
- 재현 가능성: 같은 입력에서 같은 IR/산출물이 나오고, drift 원인을 추적 가능
- 운영 가시성: UI/API에서 현재 enforcement 경로, 실패 원인, 산출물 품질을 즉시 확인
- 배포 준비도: 실제 배포 전 review gate와 수동 승인 절차를 표준화

## Workstream A: Policy and Governance
목표:
- 코드 생성 통제를 단일 소스로 정리하고, 예외 승인을 명시화

실행 항목:
1. enforcement source of truth 정의 (runner 또는 emitter 중 단일 authoritative 경로)
2. allowlist 정책 문서화 강화 (safe/risky/manual 분류 기준)
3. run-manifest에 policy snapshot 저장 (mode, location, allowlist, effective categories)
4. 승인 없는 고위험 카테고리 차단 규칙을 API 레벨에서 선제 적용

완료 기준:
- 정책 관련 회귀 테스트 100% 통과
- 운영자가 job 상세에서 effective policy를 즉시 확인 가능

## Workstream B: Determinism and Drift Control
목표:
- source/runtime 불일치와 캐시 드리프트를 재현 가능하게 감시

실행 항목:
1. 실행 시작 시 핵심 모듈 checksum 기록 (runner, emitter, policy)
2. run-manifest에 runtime fingerprint 기록 (python version, module file path)
3. drift 탐지 시 경고를 validation-report.md에 자동 출력
4. 최소 3개 golden input에 대해 결과 스냅샷 비교 자동화

완료 기준:
- drift 재현 로그 확보
- 동일 입력 반복 실행 시 핵심 산출물 diff 최소화

## Workstream C: UX and Operator Experience
목표:
- 업로드 페이지를 운영자 콘솔처럼 사용 가능하게 개선

실행 항목:
1. health/enforcement 배지 고도화 (상태 색상, stale 표시)
2. timeline 상태 뱃지화 (queued/running/completed/failed)
3. 완료 후 allowlist 준수 요약 표시 (generated vs suppressed counts)
4. 실패 시 복구 가이드 (예: 파일 형식, 정책 입력, 환경 의존성)

완료 기준:
- 운영자 관점에서 문제 원인 파악 시간을 단축
- 업로드 후 상태 확인/산출물 접근 경로가 단일 화면에서 완료

## Workstream D: Release Readiness
목표:
- "내부 운영 베타"를 위한 릴리즈 기준선 정의

실행 항목:
1. 품질 게이트: schema, policy, traceability, readiness 리포트 점검
2. 릴리즈 체크리스트: 의존성, 실행 커맨드, known issues, rollback 경로
3. 샘플 데이터셋 5종으로 E2E dry run 문서화
4. 주간 릴리즈 노트 템플릿 확정

완료 기준:
- 베타 운영 팀이 문서만으로 재실행 가능
- 변경사항이 릴리즈 노트에 일관되게 반영

## Suggested 2-Week Sprint Cut
Week 1:
1. Workstream A-1~A-3
2. Workstream B-1~B-2
3. Workstream C-1~C-2

Week 2:
1. Workstream B-3~B-4
2. Workstream C-3~C-4
3. Workstream D-1~D-2

## Metrics to Track
- Policy consistency: allowlist 회귀 실패 건수
- Drift frequency: 실행당 source/runtime mismatch 감지 건수
- Operator MTTR: 실패 원인 파악까지 걸린 평균 시간
- Release confidence: golden run 통과율

## Immediate Next Action
1. authoritative enforcement 경로 확정
2. run-manifest policy snapshot 필드 설계
3. UI에 allowlist 준수 요약 카드 추가
4. 운영 릴리즈 체크리스트와 drift RCA 문서를 정책 체크리스트에 연결
