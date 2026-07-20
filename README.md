# Architecture Diagram to IaC

아키텍처 다이어그램을 Azure Bicep IaC(Infrastructure as Code)로 자동 변환하는 파이프라인입니다.

**지원 입력 형식**
- PPTX (PowerPoint 슬라이드)
- Draw.io (`.drawio`, `.xml`)
- **PNG / JPG / WEBP 이미지** (Gemini Vision 기반 VLM 처리)

---

## 주요 기능

| 기능 | 설명 |
|---|---|
| 멀티 소스 파싱 | PPTX, Draw.io, **이미지(PNG/JPG)** 처리 |
| IR 컴파일 | 30+ Azure 서비스 + 온프레미스/외부/Naver 분류 |
| Bicep 에미터 | 엄격한 차단(Strict Suppression) 정책 |
| Policy 허용 목록 | allowedCategories 기반 코드 생성 통제 |
| Drift 탐지 | 묵시적 리소스 차단 + validation-report.md 경고 |
| 품질 게이트 | Golden Diff CI, 회귀 테스트, Invalid Input Gate |
| Web UI | 운영 콘솔 (Bicep 미리보기, Drift 경고, 컴플라이언스 요약) |

---

## 지원 Azure 서비스 (분류 가능)

### Tier 1 — Safe
`azure.virtualNetwork` · `azure.networkSecurityGroup` · `azure.routeTable` · `azure.keyVault` · `azure.storageAccount` · `azure.adlsGen2` · `azure.bastionHost` · `azure.publicIp` · `azure.networkBundle` · `azure.logAnalyticsWorkspace`

### Tier 2 — Compute / Data
`azure.containerApp` · `azure.containerRegistry` · `azure.aksCluster` · `azure.loadBalancer` · `azure.applicationGateway` · `azure.redisCache` · `azure.cosmosDb` · `azure.postgresFlexible` · `azure.sqlDatabase` · `azure.databricks` · `azure.cognitiveSearch` · `azure.openAI` · `azure.apiManagement` · `azure.functionApp` · `azure.appService` · `azure.virtualMachine`

### Tier 3 — Risky / Manual approval
`azure.firewall` · `azure.avdBundle` · `azure.avdWorkspace` · `azure.avdHostPool` · `azure.ddosProtection` · `azure.privateEndpoint`

### 非Azure (문서화 전용, Bicep 생성 없음)
`onprem.system` (NH투자, AI LAB 등) · `external.service` (인터넷, MTS 등) · `naver.cloud` (네이버 클라우드)

---

## 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. API 서버 실행
```bash
uvicorn src.api_server:app --reload --port 8000
```

브라우저에서 http://localhost:8000 을 열어 파일을 업로드하세요.

### 3. CLI 직접 실행

#### PPTX
```bash
python src/run_pptx_evidence.py \
  --input "Architecture Diagram to IaC Compiler.pptx" \
  --allow-category azure.virtualNetwork \
  --allow-category azure.firewall
```

#### Draw.io
```bash
python src/run_drawio_evidence.py \
  --input samples/network.drawio \
  --allow-category azure.networkBundle
```

#### 이미지 (PNG/JPG)
```bash
# GEMINI_API_KEY 환경변수 필요
$env:GEMINI_API_KEY = "your-api-key"

python src/run_image_evidence.py \
  --input architecture.png \
  --allow-category azure.containerApp \
  --allow-category azure.openAI \
  --allow-category azure.apiManagement
```

---

## 이미지 파이프라인 설명

PNG/JPG/WEBP 이미지를 업로드하면:

1. **Gemini Vision** 이 다이어그램을 분석하여 모든 컴포넌트 추출
2. Azure 리소스 → IR 분류 (30+ 카테고리)
3. 非Azure 리소스 → `onprem.system` / `external.service` / `naver.cloud` 로 분류, 문서화 전용 처리
4. 정책 허용 목록에 따라 Bicep 생성 대상 결정 (Strict Suppression)
5. `main.bicep` + `validation-report.md` + `architecture.ir.json` 산출

```
GEMINI_API_KEY 환경 변수를 서버에 설정해야 이미지 처리가 동작합니다.
```

---

## 산출물

각 실행(run)마다 `runs/{run-id}/` 폴더에 다음 산출물이 생성됩니다:

| 파일 | 설명 |
|---|---|
| `raw-evidence.json` | 원시 추출 증거 |
| `architecture.graph.json` | 그래프 재구성 |
| `architecture.ir.json` | Provider-neutral IR |
| `main.bicep` | 생성된 Bicep 코드 |
| `traceability-matrix.csv` | 추적성 매트릭스 |
| `validation-report.md` | 검증 결과 + Drift 경고 |
| `iac-readiness-report.md` | IaC 준비도 리포트 |
| `unresolved-questions.md` | 미해결 질문 목록 |
| `run-manifest.json` | 실행 메타데이터 + Policy Snapshot |

---

## 품질 게이트

```bash
python scripts/run_policy_quality_gates.py
```

3개 단계:
1. **Policy Regression Suite** — 허용/차단 정책 회귀 테스트
2. **Invalid Input Gate** — 잘못된 카테고리 입력 거부 확인
3. **Golden Snapshot Diff Gate** — 동일 입력에서 동일 출력 보장

---

## 아키텍처

```
입력(PPTX/Draw.io/Image)
  ↓
Adapter (PptxAdapter / DrawioAdapter / ImageAdapter[Gemini Vision])
  ↓
EvidenceRecords
  ↓
Graph Reconstruction
  ↓
IR Compiler (30+ Azure 분류 + onprem/external/naver)
  ↓
Policy Pre-filter (allowedCategories)
  ↓
Bicep Emitter (Strict Suppression + Drift Events)
  ↓
Reports (validation-report, traceability, readiness)
```

---

## 환경 변수

| 변수 | 설명 | 필수 |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API 키 (이미지 처리용) | 이미지 입력 시 필수 |
