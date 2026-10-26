"""Offline tests: synthetic DLL only; no Autodesk binaries required."""
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "reference_manager.py"
spec = importlib.util.spec_from_file_location("reference_manager", MODULE)
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)

def mock_pe_dll(path):
    buf = bytearray(512)
    buf[:2] = b"MZ"
    struct.pack_into("<I", buf, 0x3c, 128)
    buf[128:132] = b"PE\0\0"
    struct.pack_into("<H", buf, 132, 0x8664)
    struct.pack_into("<H", buf, 150, 0x2000)
    path.write_bytes(buf)

class ReferenceManagerTests(unittest.TestCase):
    def test_import_and_preflight(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            dll = root / "Example.dll"
            mock_pe_dll(dll)
            manager.add_reference(root, 2025, dll)
            self.assertEqual(manager.check(root, 2025, ["Example.dll"]), 0)
            self.assertEqual(manager.check(root, 2025, ["Missing.dll"]), 2)
            self.assertTrue((root / "references/2025/.reference-index.json").is_file())

    def test_reject_invalid(self):
        with tempfile.TemporaryDirectory() as t:
            dll = Path(t) / "Fake.dll"
            dll.write_bytes(b"not a DLL")
            with self.assertRaises(ValueError):
                manager.validate_dll(dll)
        with self.assertRaises(ValueError):
            manager.dll_name("../Oops.dll")

    def test_reads_project_reference(self):
        with tempfile.TemporaryDirectory() as t:
            project = Path(t) / "host.csproj"
            project.write_text('<Project><ItemGroup><Reference Include="AcDbMgd"/><Reference Include="acdbmgdbrep"/><Reference Include="System.Xml"/></ItemGroup></Project>')
            self.assertEqual(manager.refs_from_project(project), {"AcDbMgd.dll", "acdbmgdbrep.dll"})

if __name__ == "__main__":
    unittest.main()
