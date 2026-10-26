"""Contract checks for generic BuildKit bridge; no Autodesk or compiler binaries needed."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import json
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "buildkit_bridge.py"
spec = importlib.util.spec_from_file_location("bridge", path)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

class BridgeTests(unittest.TestCase):
    def fake_inspect(self, tfm, machine="Amd64"):
        return SimpleNamespace(stdout=json.dumps([
            {"file":"Example.dll","name":"Example","version":"25.0.0.0",
             "targetFramework":tfm,"machine":machine}
        ]))

    def test_accepts_2025_net8(self):
        with patch.object(bridge, "run_kit", return_value=self.fake_inspect(".NETCoreApp,Version=v8.0")):
            self.assertEqual(len(bridge.inspect_assembly(Path("."), [Path("Example.dll")], 2025)), 1)

    def test_2025_net10_is_valid_for_host_updated_to_2025_1_4(self):
        with patch.object(bridge, "run_kit", return_value=self.fake_inspect(".NETCoreApp,Version=v10.0")):
            self.assertEqual(len(bridge.inspect_assembly(Path("."), [Path("Example.dll")], 2025, "net10")), 1)

    def test_rejects_2025_net10_when_runtime_is_net8(self):
        with patch.object(bridge, "run_kit", return_value=self.fake_inspect(".NETCoreApp,Version=v10.0")):
            with self.assertRaisesRegex(ValueError, "selected 2025 runtime net8"):
                bridge.inspect_assembly(Path("."), [Path("Example.dll")], 2025, "net8")

    def test_v1_kit_lacks_net10_build_profile(self):
        with self.assertRaisesRegex(ValueError, "BuildKit v1 only compiles net8"):
            bridge.preflight(Path("."), Path("."), 2025, None, False, "net10")

    def test_rejects_2024_net8(self):
        with patch.object(bridge, "run_kit", return_value=self.fake_inspect(".NETCoreApp,Version=v8.0")):
            with self.assertRaises(ValueError):
                bridge.inspect_assembly(Path("."), [Path("Example.dll")], 2024)

    def test_requires_x64(self):
        with patch.object(bridge, "run_kit", return_value=self.fake_inspect(".NETCoreApp,Version=v8.0", "I386")):
            with self.assertRaisesRegex(ValueError, "x64"):
                bridge.inspect_assembly(Path("."), [Path("Example.dll")], 2025)

    def test_recipe_is_project_neutral(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "buildkit.project.json"
            path.write_text(json.dumps({"schema":1, "projects":[
                {"id":"One","autodesk":["AcMgd.dll","SomeApi.dll"]},
                {"id":"Two","autodesk":["acmgd.dll"]}
            ]}), encoding="utf8")
            self.assertEqual(bridge.recipe_references(path), ["acmgd.dll", "someapi.dll"])

    def test_rejects_undeclared_2026_profile(self):
        with self.assertRaisesRegex(ValueError, "only 2024/2025"):
            bridge.preflight(Path("."), Path("."), 2026, None, False)

if __name__ == "__main__":
    unittest.main()
