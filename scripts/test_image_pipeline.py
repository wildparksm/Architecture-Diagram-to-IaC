"""test_image_pipeline.py — 이미지 파이프라인 빠른 테스트 스크립트

사용법:
    python scripts/test_image_pipeline.py --input path/to/diagram.png
    python scripts/test_image_pipeline.py --input path/to/diagram.png --allow azure.firewall azure.containerApp

.env 파일에 AZURE_OPENAI 설정이 필요합니다.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# .env 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# src 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from adapters.image_adapter import ImageAdapter
from graph.reconstruction import build_graph
from ir.compiler import compile_ir
from policy.codegen_policy import validate_allowed_categories


def main() -> int:
    parser = argparse.ArgumentParser(description="이미지 파이프라인 빠른 테스트")
    parser.add_argument("--input", required=True, help="PNG/JPG 이미지 경로")
    parser.add_argument(
        "--allow", nargs="*", default=[], metavar="CATEGORY",
        help="Bicep 생성 허용 카테고리 (없으면 report-only)"
    )
    args = parser.parse_args()

    image_path = Path(args.input)
    if not image_path.exists():
        print(f"[ERROR] 파일 없음: {image_path}", file=sys.stderr)
        return 1

    print(f"\n{'='*60}")
    print(f"  Image Pipeline Test")
    print(f"  Input: {image_path.name}")
    print(f"{'='*60}\n")

    # 1. VLM 추출
    print(f"[1/4] Extracting resources with Azure Vision ({image_path.name})...")
    adapter = ImageAdapter(run_id="test-run")
    try:
        records = adapter.extract(image_path)
    except RuntimeError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    print(f"      -> {len(records)} elements extracted\n")

    # 2. 분류 결과 출력
    print("[2/4] VLM extraction results:")
    providers: dict[str, list[str]] = {}
    for r in records:
        prov = r.get("provenance", {}).get("detectedProvider", "unknown")
        name = r.get("text", "(unnamed)")
        providers.setdefault(prov, []).append(name)

    for prov, names in sorted(providers.items()):
        icon = {"azure": "[AZURE]", "onprem": "[ONPREM]", "external": "[EXT]", "naver": "[NAVER]"}.get(prov, "[?]")
        print(f"      {icon} ({len(names)})")
        for n in names[:8]:
            print(f"           - {n}")
        if len(names) > 8:
            print(f"           ... +{len(names)-8}")
    print()

    # 3. IR 컴파일
    print("[3/4] Compiling IR...")
    graph = build_graph(records)
    ir = compile_ir(graph)
    resources = ir.get("providerNeutralCore", {}).get("resources", [])

    azure_res   = [r for r in resources if str(r.get("category","")).startswith("azure.") and r.get("category") != "azure.resourceGroup"]
    onprem_res  = [r for r in resources if r.get("provider") == "onprem"]
    ext_res     = [r for r in resources if r.get("provider") == "external"]
    unknown_res = [r for r in resources if r.get("category") == "unknown"]

    print(f"      -> Azure resources:   {len(azure_res)}")
    print(f"      -> On-premises:       {len(onprem_res)}")
    print(f"      -> External services: {len(ext_res)}")
    print(f"      -> Unclassified:      {len(unknown_res)}")
    print()

    # 4. IR에서 인식된 Azure 카테고리 목록
    categories = sorted({r.get("category","") for r in azure_res if r.get("category","") != "unknown"})
    if categories:
        print("      Detected Azure categories:")
        for c in categories:
            count = sum(1 for r in azure_res if r.get("category") == c)
            print(f"           OK  {c}  ({count})")
    print()

    # 5. allowlist 처리
    if args.allow:
        try:
            allowed = validate_allowed_categories(args.allow)
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
        eligible = [r for r in azure_res if r.get("category") in allowed]
        suppressed = [r for r in azure_res if r.get("category") not in allowed]
        print(f"[4/4] Policy applied (allowlist={allowed}):")
        print(f"      -> Bicep targets:  {len(eligible)}")
        print(f"      -> Suppressed:     {len(suppressed)}")
    else:
        print("[4/4] Policy: report-only mode (no --allow flag)")
        print("      -> To generate Bicep, re-run with:")
        for c in categories[:10]:
            print(f"           --allow {c}")

    print("\n" + "="*60)
    print("  TEST COMPLETE")
    print("="*60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
