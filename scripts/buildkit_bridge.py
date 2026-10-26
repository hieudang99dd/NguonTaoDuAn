#!/usr/bin/env python3
"""Generic bridge: use authorized local BuildKit with per-host Autodesk DLL references."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

YEARS = (2024, 2025)

def fail(message):
    raise ValueError(message)

def checksum(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def run_kit(kit, argv, capture=False):
    build = kit / "scripts" / "build.py"
    if not build.is_file() or not (kit / "PAYLOAD_SHA256.json").is_file():
        fail("Full authorized BuildKit must be extracted before use.")
    p = subprocess.run([sys.executable, str(build), *argv], cwd=kit,
                       capture_output=capture, text=True, encoding="utf8", errors="replace")
    if p.returncode:
        fail("BuildKit command failed: " + " ".join(argv) + "\n" + (p.stdout or "") + (p.stderr or ""))
    return p

def recipe_references(path):
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("schema") != 1 or not isinstance(data.get("projects"), list):
        fail("Expected BuildKit schema=1 and projects list.")
    requested = set()
    for project in data["projects"]:
        for name in project.get("autodesk", []):
            if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+\.dll", name, re.I):
                fail("Invalid assembly filename: " + repr(name))
            requested.add(name.lower())
    return sorted(requested)

def inspect_assembly(kit, dlls, year):
    if not dlls:
        return []
    records = json.loads(run_kit(kit, ["inspect", *[str(p) for p in dlls]], capture=True).stdout)
    if len(records) != len(dlls):
        fail("BuildKit inspector did not return one record per assembly.")
    for record in records:
        tfm = (record.get("targetFramework") or "").replace(" ", "")
        arch = (record.get("machine") or "").lower()
        name = record.get("file", "Unknown.dll")
        if arch not in ("amd64", "x64"):
            fail(name + ": x64 reference required; found " + arch)
        if year == 2024 and not re.match(r"^\.NETFramework,Version=v4\.[0-9]+", tfm):
            fail(name + ": target " + tfm + " is not for the 2024 .NET Framework host.")
        if year == 2025 and tfm != ".NETCoreApp,Version=v8.0":
            fail(name + ": target " + tfm + " is not for the 2025 .NET 8 host; do not copy.")
    return records

def preflight(standard, kit, year, project, sync):
    if year not in YEARS:
        fail("BuildKit v1 supports only 2024/2025; verified 2026 profile is not present.")
    target = kit / "references" / str(year)
    shared = standard / "references" / str(year)
    owned = {x.name.lower(): x for x in target.glob("*.dll")}
    supplied = {x.name.lower(): x for x in shared.glob("*.dll")} if shared.is_dir() else {}
    targets = []
    for name in recipe_references(project):
        old = owned.get(name)
        new = supplied.get(name)
        if old is None and new is None:
            fail("Missing Autodesk DLL " + name + " for " + str(year) + "; supply an authorized reference.")
        if old and new and checksum(old) != checksum(new):
            fail("Conflicting hashes for " + name + "; review before overwriting.")
        targets.append((name, old or new, old is None))
    inspect_assembly(kit, [x[1] for x in targets], year)
    if not sync and any(x[2] for x in targets):
        fail("New compatible references found; run sync before doctor/build.")
    run_kit(kit, ["verify"], capture=True)
    run_kit(kit, ["doctor", "--year", str(year)], capture=True)
    if sync:
        target.mkdir(parents=True, exist_ok=True)
        for name, original, missing in targets:
            if not missing:
                continue
            destination = target / original.name
            with tempfile.NamedTemporaryFile(dir=target, suffix=".tmp", delete=False) as f:
                temp = Path(f.name)
            try:
                shutil.copyfile(original, temp)
                if checksum(original) != checksum(temp):
                    fail("Checksum changed while copying " + name)
                os.replace(temp, destination)
            finally:
                temp.unlink(missing_ok=True)
            print("SYNCED", destination.name, checksum(destination))
    print("REFERENCE_PREFLIGHT_PASS", year, len(targets), "declared assemblies (not NETLOAD)")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["verify", "inspect", "sync", "doctor", "build"])
    ap.add_argument("--kit", type=Path, required=True)
    ap.add_argument("--year", type=int, default=2025)
    ap.add_argument("--project", type=Path)
    ap.add_argument("--dll", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--standard", type=Path, default=Path(__file__).resolve().parents[1])
    a = ap.parse_args()
    kit = a.kit.resolve(strict=True)
    try:
        if a.command == "verify":
            run_kit(kit, ["verify"])
            return 0
        if a.command == "inspect":
            if a.dll is None:
                fail("inspect requires --dll")
            result = inspect_assembly(kit, [a.dll.resolve(strict=True)], a.year)[0]
            print(json.dumps({k: result.get(k) for k in ("file", "name", "version", "targetFramework", "machine")}, indent=2))
            return 0
        project = a.project.resolve(strict=True) if a.project else None
        if a.command in ("sync", "build") and not project:
            fail(a.command + " requires --project recipe")
        preflight(a.standard.resolve(strict=True), kit, a.year, project, a.command == "sync")
        if a.command in ("doctor", "build"):
            cmd = [a.command, "--year", str(a.year)]
            if project:
                cmd += ["--project", str(project)]
            if a.command == "build" and a.out:
                cmd += ["--out", str(a.out.resolve())]
            run_kit(kit, cmd)
        return 0
    except (ValueError, OSError, json.JSONDecodeError, subprocess.SubprocessError) as ex:
        print("BUILD_BRIDGE_ERROR:", ex, file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
