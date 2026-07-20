# Architecture Diagram to IaC Compiler
## PowerPoint Copilot 보강 프롬프트

- 대상 파일: `Architecture Diagram to IaC Compiler.pptx`
- 기준 슬라이드: 기존 17장
- 목적: 기존 기획의 핵심 메시지를 유지하면서 구현 가능성, 확장성, 검증 가능성, 하네스 엔지니어링 체계를 보강
- 사용 도구: Microsoft PowerPoint Copilot
- 권장 작업 방식: 원본을 복사한 뒤 복사본에서 수행
- 목표 분량: 약 27~30장
- 문서 성격: 경영진·아키텍트·개발팀이 함께 검토할 수 있는 기술 기획서

---

# 1. Copilot에 먼저 제공할 작업 원칙

아래 프롬프트를 PowerPoint Copilot에 입력하기 전에 현재 PPTX를 열고, 가능하면 원본 파일이 아닌 복사본에서 작업한다.

Copilot이 전체 요청을 한 번에 반영하지 못하면 이 문서의 **3. 단계별 분할 프롬프트**를 순서대로 실행한다.

---

# 2. 통합 실행 프롬프트

아래 내용을 그대로 PowerPoint Copilot에 입력한다.

---

현재 열려 있는 `Architecture Diagram to IaC Compiler` 프레젠테이션을 새로 작성하지 말고, 기존 17개 슬라이드의 메시지와 디자인 언어를 유지하면서 기술적으로 보강해 주세요.

## 작업 목표

이 프레젠테이션을 단순한 Azure 이미지-to-IaC 아이디어 문서가 아니라, 다음을 지원하는 **Provider-neutral Architecture Understanding & Compilation Platform** 기획서로 발전시켜 주세요.

- Azure 단독 구성도
- 온프렘 + Azure 하이브리드 구성도
- 온프렘 + AWS/GCP 등 퍼블릭 클라우드 구성도
- 멀티클라우드 구성도
- 순수 온프렘 구성도
- Kubernetes 및 SaaS가 혼합된 구성도
- PowerPoint, draw.io, PDF, SVG, PNG/JPG 등 다양한 입력 형식
- Bicep, Terraform, Ansible, PowerShell/DSC, Kubernetes YAML, 수동 작업 명세 등 다양한 출력 대상

단, 초기 MVP의 실제 코드 생성 지원 범위는 Azure Bicep과 AzureRM Terraform을 중심으로 유지하되, Core Architecture IR은 처음부터 특정 클라우드에 종속되지 않도록 설계해 주세요.

## 반드시 유지할 기존 핵심 메시지

1. 그림에서 곧바로 코드를 생성하지 않는다.
2. 먼저 Architecture Understanding Engine으로 구성도 의도를 이해한다.
3. PPTX/draw.io 같은 편집 가능한 원본의 Shape/XML Metadata를 우선 사용한다.
4. VLM은 단독 판정자가 아니라 여러 Extractor 결과를 조정하는 Reconciliation Engine이다.
5. 모든 결과는 Architecture IR을 거쳐 IaC 또는 다른 자동화 산출물로 생성한다.
6. 누락 정보는 임의 추론하지 않고 질문, 경고, 수동 제어 항목으로 관리한다.
7. 목표는 그림을 코드로 바꾸는 것이 아니라 아키텍처 의도를 코드화하는 것이다.

## 연구 근거 보강

2025년 논문  
`Overcoming Vision Language Model Challenges in Diagram Understanding: A Proof-of-Concept with XML-Driven Large Language Models Solutions`  
(arXiv:2502.04389)의 핵심 원칙을 연구 근거 슬라이드에 명시해 주세요.

다음 내용을 논문 기반 설계 원칙으로 표현하세요.

- VLM의 이미지 인식만으로 Diagram Structure와 Relationship을 안정적으로 복원하기 어렵다.
- PPTX, DOCX, XLSX 등 편집 가능한 문서 내부의 XML/Shape/Connector 정보를 추출해 텍스트 기반으로 해석하는 접근이 유효하다.
- 명시적 연결 정보가 부족할 때는 Connector endpoint, 좌표, 방향, 근접도 등을 사용해 연결 관계를 복원한다.
- 이 논문은 Proof-of-Concept이므로 아이콘·그룹·대규모 일반화 문제는 별도의 엔진 설계와 평가가 필요하다.
- 따라서 본 제품은 Metadata-first, Multi-extractor, Multi-pass, Evidence-driven 구조를 채택한다.

## 기존 슬라이드 보강 지시

### 기존 1번 표지
부제의 Azure 종속 표현을 줄이고 다음 방향으로 수정하세요.

- 기존 의미 유지
- `슬라이드·구성도 분석 기반 Architecture IR 및 IaC 자동 생성 플랫폼`
- Azure는 초기 Provider/Emitter 중 하나로 표현
- 하단 파이프라인은 `Diagram Sources → Understanding Engine → Provider-neutral IR → Automation Outputs`로 변경

### 기존 2번 문제 정의
Azure에 국한되지 않도록 문제 범위를 확장하세요.

추가 문제:
- 동일 자산이 여러 슬라이드와 파일에서 다른 이름으로 표현됨
- 온프렘 장비와 수동 운영 항목은 일반적인 클라우드 IaC로 직접 변환할 수 없음
- 연결선, 보안 경계, 범례, 색상 의미가 이미지 모델에서 자주 누락됨
- 추론과 원본 사실이 혼합되면 잘못된 배포 코드가 생성됨
- 검증 기준과 추적성이 없으면 생성 결과를 신뢰할 수 없음

### 기존 3번 핵심 결론
기존 6개 Signal을 다음 8개 Signal 구조로 확장하세요.

1. Shape/XML Metadata
2. Visual Layout
3. OCR/Text
4. Provider/Vendor Icon Matching
5. Connector Geometry
6. Container/Boundary Detection
7. LLM/VLM Semantic Reasoning
8. Self-Ensemble & Confidence Merge

최종 결과는 `Evidence-backed Architecture Understanding Engine`으로 표현하세요.

### 기존 4번 Workflow
다음 10단계로 확장하세요.

1. Project & Input Files
2. Source Classification
3. Multi-Extractor
4. Evidence Registry
5. Graph Reconstruction
6. Semantic Reconciliation
7. Provider-neutral Architecture IR
8. Question & Approval Gate
9. Multi-target Emitters
10. Validation & Deployment Package

각 단계가 생성하는 대표 Artifact를 하단에 작은 라벨로 표시하세요.

### 기존 5번 VLM 전략
VLM이 임의로 원본 사실을 덮어쓰지 못하도록 다음 원칙을 추가하세요.

- Deterministic evidence가 VLM 추론보다 우선
- VLM 결과는 Candidate 또는 Hypothesis로 저장
- 충돌 시 Evidence와 Confidence를 비교
- 낮은 신뢰도는 질문으로 전환
- 동일 입력과 모델/프롬프트 버전으로 재현 가능해야 함

### 기존 6번 연구 기반 원칙
논문 한계와 본 프로젝트의 보완책을 2열 비교표로 추가하세요.

예:
- 논문: 제한된 도형/연결선 중심 → 제품: 아이콘, 그룹, 컨테이너, 범례 지원
- 논문: 단일 문서/예제 중심 → 제품: 멀티파일·멀티슬라이드 Entity Resolution
- 논문: 텍스트 기반 Proof-of-Concept → 제품: Parser + CV + OCR + VLM Ensemble
- 논문: 구조 이해 검증 → 제품: IaC lint/build/plan/what-if까지 폐루프 검증

### 기존 7번 Extractor Layer
`Azure Icon Classifier`를 `Provider/Vendor Icon Classifier`로 변경하세요.

다음 Extractor를 추가하세요.

- SVG/Visio Adapter
- Embedded Image Extractor
- Group/Z-order Resolver
- Legend & Style Interpreter
- Multi-page Entity Resolver
- Existing Resource Detector

Extractor는 직접 IaC를 생성하지 않고 `Canonical Evidence Registry`에만 기록한다고 강조하세요.

### 기존 8번 Normalization
Element Registry를 단일 JSON 객체 수준이 아니라 다음 3단계로 보강하세요.

- Raw Evidence
- Canonical Element
- Semantic Candidate

반드시 포함할 필드:
- stable ID
- source document/page/object ID
- bbox/geometry/rotation/z-order
- text/style/group/container
- source evidence/provenance
- classification candidates
- confidence dimensions
- deployability classification
- unresolved questions
- model/parser version

Confidence는 단일 숫자가 아니라 다음 차원으로 표현하세요.

- existence
- text
- classification
- containment
- connectivity
- deployability

### 기존 9번 Graph
연결 복원 규칙을 추가하세요.

- explicit connector binding
- endpoint proximity
- arrowhead direction
- line intersection and branching
- label-to-edge association
- container crossing
- semantic compatibility
- ambiguity penalty

Node/Edge/Container 외에 다음을 표현하세요.

- Zone/Boundary
- External Actor
- Data Flow
- Management Flow
- Trust Relationship
- Dependency
- Existing/Manual Object

### 기존 10번 IR
Architecture IR을 Provider-neutral Core와 Provider Extension으로 분리하세요.

Core 예:
- compute
- network
- identity
- security
- data
- integration
- observability
- platform
- external
- physical
- logical

Provider Extension 예:
- Azure
- AWS
- GCP
- VMware
- Hyper-V
- Kubernetes
- Network Vendor
- Custom/Unknown

Architecture IR 내부에 다음 계층을 명시하세요.

- resources
- relationships
- containers/zones
- securityControls
- existingResources
- manualControls
- assumptions
- questions
- warnings
- evidenceLinks
- confidence
- targetCapabilities

### 기존 11번 질문 모델
질문을 단순 목록이 아니라 Lifecycle로 표현하세요.

`Detected → Classified → Asked → Answered → Validated → Applied → Closed`

질문 유형:
- Blocker
- Risk
- Optional
- Manual Control
- Conflict
- Unsupported

정책:
- Blocker가 남아 있으면 Production-ready 출력은 금지
- Draft code와 질문 보고서는 생성 가능
- 기본값 사용 시 출처와 영향 범위를 기록
- 답변 변경 시 관련 IR과 코드만 증분 재생성

### 기존 12번 코드 생성
Bicep/Terraform만 나열하지 말고 `Multi-target Emitter Framework`로 확장하세요.

초기 지원:
- Azure Raw Bicep
- Azure Verified Modules 기반 Bicep 확장
- AzureRM Terraform

확장 후보:
- AWS/GCP Terraform
- VMware Terraform/PowerCLI
- Ansible
- PowerShell DSC
- Kubernetes YAML/Helm
- Vendor Network Config
- Manual Runbook/Bill of Materials

다음 원칙을 강조하세요.
- Emitter는 IR을 읽기만 한다.
- Emitter가 원본 구성도를 다시 해석하지 않는다.
- 지원하지 않는 항목은 삭제하지 않고 Manual/Unsupported Artifact로 남긴다.
- 서로 다른 IaC 언어끼리 직접 변환하지 않는다.

### 기존 13번 상세 정의서
Traceability를 강화하세요.

각 명세 항목은 다음과 연결되어야 합니다.

`원본 Object → Evidence ID → IR Object → Question/Decision → 생성 코드 위치 → Validation 결과`

산출물에 다음을 추가하세요.

- architecture-spec.md/docx/pdf
- traceability-matrix.csv
- decision-log.md
- assumptions.md
- manual-controls.md
- bill-of-materials.csv
- change-impact-report.md

### 기존 14번 Validation
구문 검증 외에 다음 4단계 검증으로 확장하세요.

1. Schema Validation
2. Graph/Semantic Validation
3. Target IaC Validation
4. Cross-domain Architecture Validation

추가 검증:
- JSON Schema
- graph invariants
- duplicate CIDR/name detection
- unsupported target detection
- policy/security rule checks
- source-to-code traceability coverage
- hallucinated resource/edge detection
- deterministic regression comparison

### 기존 15번 MVP
MVP의 Core는 Provider-neutral로 수정하되 구현 범위는 현실적으로 유지하세요.

MVP 입력:
- PPTX
- draw.io XML
- PNG/JPG 보조
- Vector PDF 실험 지원

MVP 이해 대상:
- Node/Edge/Container/Text/Legend
- Azure 주요 리소스
- Generic On-prem compute/network/security/storage
- Existing/Manual/Unknown 분류

MVP 코드 출력:
- Azure Raw Bicep
- AzureRM Terraform 선택 지원
- 순수 온프렘은 코드 생성보다 Architecture Spec, BOM, Manual Runbook 생성

MVP 필수 산출물:
- raw-evidence.json
- element-registry.json
- architecture.graph.json
- architecture.ir.json
- detected-elements.csv
- iac-readiness-report.md
- unresolved-questions.md
- traceability-matrix.csv
- main.bicep 또는 Terraform
- validation-report.md
- run-manifest.json

### 기존 16번 Roadmap
로드맵을 다음 8단계로 재구성하세요.

0. Harness & Golden Dataset
1. Source Adapters / Evidence Registry
2. Graph Reconstruction
3. Semantic Reconciliation / Provider-neutral IR
4. Azure Bicep Emitter
5. Validation & What-if
6. Terraform / Hybrid Deployment Package
7. On-prem & Multi-cloud Plugins
8. CI/CD, PR Automation, Policy/Graph/Intune/PIM 확장

각 Phase에 Exit Criteria를 한 줄씩 표시하세요.

### 기존 17번 Vision
마지막 메시지를 다음 구조로 보강하세요.

`Evidence → Understanding → Intent → IR → Automation → Validation`

최종 문구:
“우리는 다이어그램 픽셀을 코드로 번역하지 않는다.  
증거를 기반으로 아키텍처 의도를 복원하고, 검증 가능한 자동화 패키지로 컴파일한다.”

## 반드시 추가할 신규 슬라이드

기존 흐름을 깨지 않도록 적절한 위치에 아래 신규 슬라이드를 삽입하세요.

### 신규 A. Scope Matrix
Azure, Hybrid, Multi-cloud, Pure On-prem을 행으로 두고 다음 열을 비교하세요.

- Source Understanding
- Semantic Mapping
- Code Generation
- Manual Artifact
- Validation
- MVP Support Level

### 신규 B. Three Truth Layers
다음 3계층을 하나의 계단형 또는 파이프라인 다이어그램으로 표현하세요.

1. Evidence Truth: 원본에서 관찰한 사실
2. Semantic Truth: 의미 해석과 후보
3. Deployment Truth: 배포에 필요한 확정 값

“추론을 원본 사실로 승격하지 않는다”는 문구를 강조하세요.

### 신규 C. Source Adapter & Quality Levels
다음 4등급을 카드 또는 매트릭스로 표현하세요.

- L1 Structured: PPTX, draw.io, VSDX
- L2 Semi-structured: SVG, Vector PDF
- L3 Unstructured: PNG, JPG, Scanned PDF
- L4 Mixed: PPTX 안에 이미지 구성도

등급별로 Metadata, OCR, CV, VLM 사용 비중을 표시하세요.

### 신규 D. Multi-document Entity Resolution
동일 리소스가 여러 파일/슬라이드에서 다른 이름으로 등장하는 예를 시각화하세요.

예:
`FW01 = Hub Firewall = Azure Firewall = 보안 허브 방화벽`

사용 신호:
- name/alias
- icon
- position/container
- IP/hostname
- relationship neighborhood
- human-confirmed mapping

### 신규 E. Deployability Classification
다음 7개 분류를 카드형으로 표현하세요.

- FULL_IAC
- PARTIAL_IAC
- CONFIG_AUTOMATION
- EXISTING_RESOURCE
- MANUAL_OPERATION
- DOCUMENTATION_ONLY
- UNSUPPORTED / UNKNOWN

### 신규 F. Deployment Package
하이브리드 구성도의 출력 예시를 폴더 트리 또는 패키지 다이어그램으로 표현하세요.

- shared IR
- azure Bicep
- Terraform
- configuration automation
- manual runbook
- validation reports
- deployment plan
- architecture specification

### 신규 G. Harness Engineering
다음 공식을 중심에 배치하세요.

`Agent = Model + Harness`

5대 구성 요소:
- Context Delivery
- Tool Interfaces
- Feedback Loops
- State & Memory
- Governance

본 프로젝트의 각 구성요소와 1:1 매핑하세요.

### 신규 H. Development Loop
다음 반복 루프를 순환형으로 표현하세요.

`DEFINE → SCAFFOLD → WIRE → VERIFY → HARDEN → DEFINE`

각 단계에 대표 Artifact를 표시하세요.

### 신규 I. Golden Dataset & Metrics
평가 Fixture와 지표를 보여주세요.

Fixture:
- simple network
- grouped shapes
- unsnapped connectors
- multi-slide
- embedded image
- on-prem
- hybrid
- multi-cloud
- adversarial

Metrics:
- element precision/recall
- node/edge F1
- direction accuracy
- hallucinated edge rate
- resource mapping accuracy
- validation success
- traceability coverage
- silent-default count

초기 목표:
- editable-source node recall ≥ 95%
- edge F1 ≥ 90%
- hallucinated edge rate ≤ 1%
- blocker silent-default count = 0
- traceability coverage = 100%

### 신규 J. Security & Governance
다음 내용을 4개 영역으로 표현하세요.

- Data Protection
- Model Governance
- Code Safety
- Auditability

포함 내용:
- Local/private execution option
- sensitive data redaction
- no credential in IR
- diagram text prompt-injection isolation
- model/parser/prompt version recording
- human approval before deployment
- immutable evidence and audit log
- temporary crop/image deletion policy

### 신규 K. Runtime & Repository Architecture
다음 논리 컴포넌트를 보여주세요.

- CLI/API
- Project Orchestrator
- Source Adapters
- Evidence Store
- Graph Engine
- Reconciliation Engine
- IR Compiler
- Question Service
- Emitter Plugins
- Validator Plugins
- Report Generator
- Run Manifest / Observability

### 신규 L. Key Architecture Decisions
다음 결정을 표로 정리하세요.

- Metadata-first, VLM-second
- Provider-neutral Core IR
- Evidence/Semantic/Deployment truth separation
- CLI-first, library-first MVP
- Human approval gate
- No silent defaults for blockers
- Plugin-based adapters/emitters/validators
- Reproducible run manifest
- Deployment execution is out of MVP scope

## 디자인 및 편집 규칙

- 기존의 어두운 네이비/블루 기반 엔터프라이즈 디자인을 유지한다.
- 기존 16:9 슬라이드 크기를 유지한다.
- 모든 슬라이드는 한 가지 핵심 메시지만 전달한다.
- 텍스트만 길게 나열하지 않는다.
- 본문은 카드, 표, 파이프라인, 매트릭스, 계층도, 폴더 트리, 순환 다이어그램 중 하나로 시각화한다.
- 흐릿한 웹 이미지나 스크린샷을 사용하지 않는다.
- PowerPoint 기본 도형, 선명한 벡터 아이콘, 단순한 기하학 형태를 사용한다.
- 도형 겹침, 잘린 텍스트, 지나치게 작은 글자를 허용하지 않는다.
- 제목 28pt 이상, 핵심 본문 15~18pt 이상을 목표로 한다.
- 슬라이드 간 여백, 카드 높이, 라운드 값, 선 굵기, 번호 체계를 통일한다.
- 왼쪽 Highlight Box 형태의 목차는 사용하지 않거나, 사용하는 경우 모든 해당 슬라이드에서 크기·위치·스타일을 완전히 통일한다.
- 기존 Confidential Footer와 페이지 번호를 유지한다.
- 새 슬라이드에도 동일한 Footer와 페이지 체계를 적용한다.
- 과도한 장식보다 기술적 구조와 가독성을 우선한다.
- Azure 아이콘만으로 멀티클라우드/온프렘을 표현하지 않는다.
- 특정 Vendor 로고 사용이 불필요하면 Generic Icon을 우선한다.
- 모든 영어 용어는 첫 등장 시 한국어 설명 또는 의미를 함께 표시한다.

## 내용 안전 규칙

- 명확하지 않은 제품 기능이나 지원 범위를 사실처럼 추가하지 않는다.
- 실제로 결정되지 않은 기술 스택은 `Candidate` 또는 `ADR에서 확정`으로 표시한다.
- 온프렘 장비가 모두 IaC로 자동 생성된다고 표현하지 않는다.
- 코드 생성과 실제 배포 실행을 구분한다.
- Draft/Validated/Production-ready 상태를 구분한다.
- 보안 정책, CIDR, SKU, 리전 등 배포 필수 값은 질문 또는 결정 입력으로 관리한다고 명시한다.
- Azure가 중요한 초기 Target이지만 Core IR과 Understanding Engine은 Azure에 종속되지 않게 표현한다.

## 최종 산출 요구

1. 기존 17개 슬라이드를 삭제하지 말고 필요한 내용을 수정한다.
2. 신규 슬라이드를 적절한 위치에 삽입한다.
3. 전체 슬라이드 번호를 재정렬한다.
4. 마지막에 `Implementation Readiness Checklist` 슬라이드를 추가한다.
5. Checklist에는 다음 항목을 넣는다.
   - Provider-neutral IR 정의 완료
   - Source Adapter 계약 정의 완료
   - Evidence Schema 정의 완료
   - Graph Resolution 규칙 정의 완료
   - Question/Approval Gate 정의 완료
   - Emitter/Validator Plugin 계약 정의 완료
   - Golden Dataset 준비
   - Security/Governance 검토
   - MVP Acceptance Criteria 합의
   - Master Spec MD와 Traceability 확인
6. 발표자 노트가 지원된다면 각 신규 슬라이드의 노트에 다음을 추가한다.
   - 핵심 설명 3~5문장
   - 설계 의사결정
   - 구현 시 주의사항
   - 아직 확정되지 않은 항목

작업 후 전체 프레젠테이션을 검토해 중복 메시지를 제거하고, 슬라이드 순서가 `문제 → 연구 근거 → 설계 → 구현 계약 → 검증 → MVP → 로드맵 → 비전` 흐름을 따르도록 재배치해 주세요.

---

# 3. 단계별 분할 프롬프트

Copilot이 통합 프롬프트를 일부만 수행할 경우 아래 순서대로 실행한다.

## Prompt 1 — 범위와 핵심 메시지 수정

현재 프레젠테이션의 기존 1~6번 슬라이드를 유지하면서 Azure 단독 제품이 아니라 Provider-neutral Core와 Azure 초기 Target을 가진 제품으로 수정해 주세요. 문제 정의에 온프렘, 하이브리드, 멀티클라우드, 순수 온프렘 구성도의 문제를 포함하고, 2025년 arXiv:2502.04389 논문의 XML/Shape Metadata-first 접근과 한계를 연구 근거로 추가해 주세요. 텍스트 나열이 아니라 카드, 비교표, 파이프라인으로 표현하고 기존 디자인과 Footer를 유지해 주세요.

## Prompt 2 — Extractor와 Evidence 보강

기존 Extractor, Normalization, Graph 슬라이드를 보강해 주세요. Azure Icon Classifier를 Provider/Vendor Icon Classifier로 바꾸고 Source Adapter, Raw Evidence, Canonical Element, Semantic Candidate 계층을 추가해 주세요. Connector endpoint, 근접도, 방향, 분기, 컨테이너 교차, 레이블 연관성, 의미 호환성을 이용한 Graph Reconstruction 규칙을 시각화해 주세요. Confidence를 existence, text, classification, containment, connectivity, deployability로 분리해 주세요.

## Prompt 3 — Provider-neutral IR과 하이브리드 출력

Architecture IR을 Provider-neutral Core와 Provider Extension으로 분리해 주세요. Azure, AWS, GCP, VMware, Hyper-V, Kubernetes, Network Vendor, Custom/Unknown 확장을 표현하고, Deployability를 FULL_IAC, PARTIAL_IAC, CONFIG_AUTOMATION, EXISTING_RESOURCE, MANUAL_OPERATION, DOCUMENTATION_ONLY, UNSUPPORTED/UNKNOWN으로 분류하는 신규 슬라이드를 추가해 주세요. 하이브리드 구성도의 출력이 단일 코드 파일이 아니라 Azure 코드, Terraform, 설정 자동화, 수동 Runbook, 검증 보고서가 묶인 Deployment Package임을 표현해 주세요.

## Prompt 4 — 질문, 추적성, 검증

질문 모델에 Detected → Classified → Asked → Answered → Validated → Applied → Closed Lifecycle을 추가해 주세요. Blocker가 남으면 Production-ready 출력은 금지하지만 Draft와 질문 보고서는 생성 가능하다는 정책을 넣어 주세요. 원본 Object → Evidence → IR → Decision → Code → Validation의 Traceability Chain을 시각화하고, Schema/Graph/Semantic/IaC/Cross-domain 검증 계층을 추가해 주세요.

## Prompt 5 — Harness Engineering과 평가

`Agent = Model + Harness` 슬라이드를 추가해 Context Delivery, Tool Interfaces, Feedback Loops, State & Memory, Governance를 본 프로젝트 컴포넌트와 매핑해 주세요. `DEFINE → SCAFFOLD → WIRE → VERIFY → HARDEN` 반복 루프를 추가하고 Golden Dataset, Fixture 유형, Element/Edge/Mapping/IaC/Traceability 지표와 초기 합격 목표를 시각화해 주세요.

## Prompt 6 — 보안, 런타임, MVP, 로드맵

Security & Governance, Runtime Architecture, Repository/Plugin 구조, Key Architecture Decisions 슬라이드를 추가해 주세요. MVP Core는 Provider-neutral로 유지하되 실제 Emitter는 Azure Bicep과 AzureRM Terraform 중심으로 제한해 주세요. 순수 온프렘은 Spec/BOM/Runbook 출력을 우선하도록 명시하고, Roadmap을 Harness & Golden Dataset부터 Multi-cloud/On-prem Plugin과 CI/CD 자동화까지 Exit Criteria가 있는 단계로 수정해 주세요.

## Prompt 7 — 디자인 정리 및 최종 검토

전체 프레젠테이션의 레이아웃을 정리해 주세요. 텍스트 전용 슬라이드를 카드, 표, 파이프라인, 매트릭스 또는 계층도로 바꾸고, 흐릿한 이미지와 중복 도형을 제거해 주세요. 제목/본문 글꼴 크기, 카드 크기, 여백, 선 굵기, 번호, Footer를 통일하고 잘림이나 겹침이 없는지 확인해 주세요. 마지막에 Implementation Readiness Checklist를 추가하고 전체 흐름을 문제 → 연구 → 설계 → 구현 계약 → 검증 → MVP → 로드맵 → 비전 순서로 정리해 주세요.

---

# 4. 권장 최종 슬라이드 구성

Copilot의 결과가 아래와 정확히 같을 필요는 없지만, 주요 주제가 누락되지 않았는지 확인한다.

| 권장 순서 | 슬라이드 |
|---:|---|
| 1 | Cover |
| 2 | Problem Definition |
| 3 | Scope Matrix |
| 4 | Key Insight |
| 5 | Research Basis |
| 6 | Research Limitations vs Product Design |
| 7 | End-to-End Workflow |
| 8 | Source Adapter & Quality Levels |
| 9 | Multi-Extractor Layer |
| 10 | Three Truth Layers |
| 11 | Evidence Registry |
| 12 | Graph Reconstruction |
| 13 | Multi-document Entity Resolution |
| 14 | VLM Reconciliation |
| 15 | Provider-neutral Architecture IR |
| 16 | Provider Catalog / Ontology |
| 17 | Deployability Classification |
| 18 | Question & Approval Lifecycle |
| 19 | Multi-target Emitter Framework |
| 20 | Hybrid Deployment Package |
| 21 | Architecture Specification & Traceability |
| 22 | Validation Framework |
| 23 | Harness Engineering |
| 24 | Development Loop |
| 25 | Golden Dataset & Metrics |
| 26 | Security & Governance |
| 27 | Runtime Architecture |
| 28 | Revised MVP |
| 29 | Roadmap & Exit Criteria |
| 30 | Implementation Readiness Checklist |
| 31 | Vision |

---

# 5. 결과 검수 체크리스트

## 내용

- [ ] Azure 단독 표현이 Provider-neutral Core + Azure 초기 Target으로 수정되었다.
- [ ] 온프렘, 하이브리드, 멀티클라우드, 순수 온프렘을 명시적으로 다룬다.
- [ ] Evidence, Semantic, Deployment Truth가 분리되어 있다.
- [ ] Source Adapter와 입력 품질 등급이 있다.
- [ ] 연결선 복원 규칙이 구체화되어 있다.
- [ ] Multi-slide/Multi-file Entity Resolution이 있다.
- [ ] IR이 Provider-neutral Core와 Extension으로 분리되어 있다.
- [ ] Deployability 분류가 있다.
- [ ] 질문 Lifecycle과 Approval Gate가 있다.
- [ ] Multi-target Emitter와 Deployment Package가 있다.
- [ ] Harness Engineering과 개발 반복 루프가 있다.
- [ ] Golden Dataset과 수치형 합격 기준이 있다.
- [ ] 보안·Prompt Injection·감사·재현성 요구가 있다.
- [ ] MVP와 장기 비전이 구분되어 있다.
- [ ] 실제 자동 배포는 MVP 범위 밖으로 구분되어 있다.

## 디자인

- [ ] 텍스트만 나열한 슬라이드가 없다.
- [ ] 카드, 표, 파이프라인, 매트릭스가 목적에 맞게 사용되었다.
- [ ] 글자 잘림과 도형 겹침이 없다.
- [ ] 흐릿한 외부 이미지가 없다.
- [ ] Footer와 페이지 번호가 일관적이다.
- [ ] 제목·본문·캡션 크기가 일관적이다.
- [ ] 왼쪽 Highlight Box를 사용한다면 모든 슬라이드에서 동일하다.
- [ ] 기술 용어가 지나치게 작거나 빽빽하지 않다.
- [ ] 각 슬라이드가 하나의 핵심 메시지를 전달한다.

---

# 6. Copilot 결과가 부족할 때 사용할 수정 명령

## 내용이 너무 추상적일 때

현재 슬라이드의 추상적인 설명을 구현 계약 수준으로 구체화해 주세요. 각 컴포넌트마다 입력, 출력, 책임, 금지사항, 검증 방법을 최소 1개씩 표시하세요. 단, 슬라이드에는 긴 문장을 넣지 말고 4열 표 또는 카드로 압축해 주세요.

## Azure 중심 표현이 남아 있을 때

Azure는 초기 Emitter와 Provider Plugin 중 하나일 뿐입니다. Core Evidence Model, Graph Model, Architecture IR, Question Model은 Azure 제품명을 사용하지 않는 Provider-neutral 구조로 다시 표현해 주세요. Azure 고유 속성은 Provider Extension에만 남겨 주세요.

## 온프렘 자동화가 과장되었을 때

순수 온프렘의 모든 장비를 IaC로 자동 배포할 수 있다고 표현하지 마세요. 지원 정도를 FULL_IAC, PARTIAL_IAC, CONFIG_AUTOMATION, EXISTING_RESOURCE, MANUAL_OPERATION, DOCUMENTATION_ONLY, UNSUPPORTED/UNKNOWN으로 나누고, 코드가 불가능한 항목은 BOM, Runbook, Checklist, Architecture Spec으로 출력한다고 수정해 주세요.

## 디자인이 복잡할 때

한 슬라이드에 7개 이상의 핵심 객체를 배치하지 마세요. 내용을 두 장으로 나누고, 텍스트 대신 단순한 카드/계층도/흐름도를 사용하세요. 배경과 장식은 줄이고, 기술 구조와 가독성을 우선해 주세요.

## 중복이 생겼을 때

전체 슬라이드를 검토하여 동일한 설명을 반복하는 슬라이드를 병합하세요. 각 슬라이드의 목적을 한 문장으로 정의하고, 다른 슬라이드와 메시지가 겹치면 더 적합한 위치 한 곳에만 남겨 주세요.

---

# 7. 참고

PowerPoint Copilot의 실제 편집 범위는 조직의 Microsoft 365 설정, Copilot 라이선스, 앱 버전 및 배포 채널에 따라 달라질 수 있다. 한 번에 모든 구조 변경이 반영되지 않으면 **단계별 분할 프롬프트**를 사용하는 것이 안전하다.
