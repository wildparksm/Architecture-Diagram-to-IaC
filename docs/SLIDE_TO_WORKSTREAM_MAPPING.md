# Slide to Workstream Mapping

## 목적
PPTX의 메시지를 실제 구현 트랙으로 변환하기 위한 맵이다.

| Slide Theme | Workstream | 구현 포인트 |
|---|---|---|
| Problem / Scope | Product Definition | 지원 범위와 비범위 고정 |
| Key Insight / VLM Strategy | Reconciliation Engine | Evidence 우선 병합 규칙 |
| Workflow | Orchestrator | 단계별 artifact 계약 |
| Extractor Layer | Source Adapters + Extractors | Parser/CV/OCR/VLM 분리 |
| Normalization | Evidence Registry | stable ID, provenance, confidence |
| Graph | Graph Engine | edge 복원 규칙과 ambiguity 처리 |
| IR | IR Compiler | Core/Extension 분리 |
| Question Model | Question Service | Gate 정책과 lifecycle |
| Code Generation | Emitter Plugins | IR read-only emitter |
| Design Specification | Report Generator | traceability chain 문서화 |
| Validation | Validator Plugins | schema/semantic/iac 검증 |
| MVP / Roadmap | Delivery Plan | phase exit criteria |
| Vision | Governance | intent-first 원칙 유지 |

## 산출물 책임 분리
- Adapter: source parsing only
- Extractor: evidence creation only
- Reconciliation: conflict resolution only
- IR Compiler: semantic consolidation only
- Emitter: target code/document generation only
- Validator: quality and safety gates only
