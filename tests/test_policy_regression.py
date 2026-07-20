from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT_DIR = Path(__file__).resolve().parents[1]
PPTX_RUNNER = ROOT_DIR / "src" / "run_pptx_evidence.py"
PPTX_INPUT = ROOT_DIR / "Architecture Diagram to IaC Compiler.pptx"

FIREWALL_TOKEN = "Microsoft.Network/azureFirewalls@2023-11-01"
AVD_HOSTPOOL_TOKEN = "Microsoft.DesktopVirtualization/hostPools@2024-04-03"


class PolicyRegressionTest(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_root = Path(tempfile.mkdtemp(prefix="policy-regression-"))
        self.runs_dir = self._temp_root / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self._temp_root, ignore_errors=True)

    def _run_case(self, run_suffix: str, allowed_categories: list[str]) -> dict[str, object]:
        run_id = f"regression-{run_suffix}"
        cmd = [
            sys.executable,
            str(PPTX_RUNNER),
            "--input",
            str(PPTX_INPUT),
            "--runs-dir",
            str(self.runs_dir),
            "--run-id",
            run_id,
        ]
        for category in allowed_categories:
            cmd.extend(["--allow-category", category])

        result = subprocess.run(
            cmd,
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"runner failed for {run_id}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

        run_dir = self.runs_dir / run_id
        manifest_path = run_dir / "run-manifest.json"
        bicep_path = run_dir / "main.bicep"
        self.assertTrue(manifest_path.exists(), msg=f"missing manifest for {run_id}")
        self.assertTrue(bicep_path.exists(), msg=f"missing bicep for {run_id}")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bicep = bicep_path.read_text(encoding="utf-8")

        self.assertNotIn(FIREWALL_TOKEN, bicep, msg=f"firewall emitted in {run_id}")
        self.assertNotIn(AVD_HOSTPOOL_TOKEN, bicep, msg=f"AVD host pool emitted in {run_id}")

        policy_snapshot = manifest.get("codegenPolicySnapshot", {})
        runtime_fingerprint = manifest.get("runtimeFingerprint", {})
        self.assertIsInstance(policy_snapshot, dict)
        self.assertIsInstance(runtime_fingerprint, dict)
        self.assertIn("effectiveAllowedCategories", policy_snapshot)
        self.assertIn("moduleFiles", runtime_fingerprint)

        return {
            "manifest": manifest,
            "effective": policy_snapshot.get("effectiveAllowedCategories", []),
        }

    def test_report_only_policy_snapshot(self) -> None:
        payload = self._run_case("report-only", [])
        self.assertEqual(payload["effective"], [])

    def test_network_bundle_only_policy_snapshot(self) -> None:
        payload = self._run_case("network-bundle", ["azure.networkBundle"])
        self.assertEqual(payload["effective"], ["azure.networkBundle"])

    def test_composite_allowlist_policy_snapshot(self) -> None:
        payload = self._run_case(
            "composite",
            [
                "azure.virtualNetwork",
                "azure.networkSecurityGroup",
                "azure.routeTable",
            ],
        )
        self.assertEqual(
            payload["effective"],
            ["azure.networkSecurityGroup", "azure.routeTable", "azure.virtualNetwork"],
        )


if __name__ == "__main__":
    unittest.main()
