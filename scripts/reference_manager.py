#!/usr/bin/env python3
"""Local Autodesk reference manager for Civil 3D 2024/2025/2026 (stdlib only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET

HOST_YEARS = (2024, 2025, 2026)
INDEX_NAME = ".reference-index.json"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as src:
        for block in iter(lambda: src.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def validate_dll(path):
    # Container sanity check only: this does NOT verify Autodesk origin or host-year compatibility.
    with path.open("rb") as src:
        head = src.read(4096)
    if len(head) < 256 or head[:2] != b"MZ":
        raise ValueError("Not a Windows PE DLL: " + str(path))
    offset = struct.unpack_from("<I", head, 0x3c)[0]
    if offset + 26 >= len(head) or head[offset:offset+4] != b"PE\0\0":
        raise ValueError("Invalid PE header: " + str(path))
    machine = struct.unpack_from("<H", head, offset + 4)[0]
    flags = struct.unpack_from("<H", head, offset + 22)[0]
    if not flags & 0x2000 or machine not in (0x8664, 0x14c, 0xaa64):
        raise ValueError("Unsupported DLL machine or missing DLL flag: " + str(path))
    return {"machine": "0x%04x" % machine, "bytes": path.stat().st_size}

def dll_name(text):
    if Path(text).name != text or not re.fullmatch(r"[\w.-]+\.dll", text, re.I):
        raise ValueError("Invalid DLL filename: " + text)
    return text

def folder_for(root, year, runtime=None):
    if year not in HOST_YEARS:
        raise ValueError("Expected Civil 3D host year 2024/2025/2026")
    if runtime is not None:
        if year != 2025 or runtime not in ("net8", "net10"):
            raise ValueError("Runtime folders are currently defined only for 2025: net8/net10")
        return root / "references" / str(year) / runtime
    return root / "references" / str(year)

def read_index(folder):
    p = folder / INDEX_NAME
    return json.loads(p.read_text(encoding="utf8")) if p.exists() else {"schemaVersion": 1, "assemblies": {}}

def write_index(folder, index):
    with tempfile.NamedTemporaryFile("w", encoding="utf8", dir=folder, suffix=".tmp", delete=False) as f:
        json.dump(index, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
        name = Path(f.name)
    os.replace(name, folder / INDEX_NAME)

def add_reference(root, year, source, replace=False, runtime=None):
    source = source.expanduser().resolve(strict=True)
    dll_name(source.name)
    meta = validate_dll(source)
    folder = folder_for(root, year, runtime)
    folder.mkdir(parents=True, exist_ok=True)
    matches = [p for p in folder.glob("*.dll") if p.name.lower() == source.name.lower()]
    target = matches[0] if matches else folder / source.name
    digest = sha256(source)
    if target.exists() and sha256(target) != digest and not replace:
        raise ValueError("Already exists with different hash; use --replace after review: " + target.name)
    if source != target and (not target.exists() or sha256(target) != digest):
        with tempfile.NamedTemporaryFile("wb", dir=folder, suffix=".tmp", delete=False) as f:
            temp = Path(f.name)
        try:
            shutil.copyfile(source, temp)
            if sha256(temp) != digest:
                raise ValueError("Hash mismatch copying " + source.name)
            os.replace(temp, target)
        finally:
            temp.unlink(missing_ok=True)
    idx = read_index(folder)
    idx["declaredHostYear"] = year
    if runtime:
        idx["declaredRuntime"] = runtime
    idx.setdefault("assemblies", {})[target.name] = {"sha256": digest, **meta}
    write_index(folder, idx)
    print("IMPORTED %s %s SHA256 %s" % (year, target.name, digest))
    print("Autodesk origin/version/NETLOAD compatibility are NOT established by this check.")

def refs_from_project(path):
    names = set()
    for node in ET.parse(path).iter():
        if node.tag.rsplit("}", 1)[-1] != "Reference":
            continue
        name = (node.get("Include") or "").split(",", 1)[0].strip()
        if re.match(r"(?i)^(ac(core|db)?mgd|acdbmgd\w*|aec\w*mgd|aecc\w*mgd|autodesk\.)", name):
            names.add(name if name.lower().endswith(".dll") else name + ".dll")
    return names

def needed(args):
    values = set(args.require or [])
    if args.requirements_json:
        rows = json.loads(args.requirements_json.read_text(encoding="utf8")).get("requiredAssemblies")
        if not isinstance(rows, list):
            raise ValueError("requirements JSON must contain requiredAssemblies array")
        values.update(rows)
    for project in args.project or []:
        values.update(refs_from_project(project))
    return sorted({dll_name(x) for x in values}, key=str.lower)

def check(root, year, required, runtime=None):
    folder = folder_for(root, year, runtime)
    installed = {p.name.lower(): p for p in folder.glob("*.dll")} if folder.exists() else {}
    index = read_index(folder)
    indexed = {key.lower(): val for key, val in index.get("assemblies", {}).items()}
    problems = []
    if not required:
        print("WARNING: No required assemblies declared; completeness not checked.")
    for name in required:
        p = installed.get(name.lower())
        if not p:
            problems.append("MISSING %s: %s" % (year, name))
            continue
        try:
            validate_dll(p)
            digest = sha256(p)
            if name.lower() in indexed and digest != indexed[name.lower()].get("sha256"):
                problems.append("HASH CHANGED " + p.name)
            else:
                print("FOUND %s: %s SHA256 %s" % (year, p.name, digest))
        except (OSError, ValueError) as error:
            problems.append(str(error))
    for problem in problems:
        print("ERROR:", problem, file=sys.stderr)
    if problems:
        return 2
    print("PASS: %d declared references present; build and NETLOAD not verified." % len(required))
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = ap.add_subparsers(dest="action", required=True)
    imp = sub.add_parser("import")
    imp.add_argument("--year", type=int, required=True)
    imp.add_argument("--source", type=Path, required=True)
    imp.add_argument("--replace", action="store_true")
    imp.add_argument("--runtime", choices=["net8", "net10"], help="Civil 3D 2025 update profile; recommended for new reference sets")
    chk = sub.add_parser("check")
    chk.add_argument("--year", type=int, required=True)
    chk.add_argument("--runtime", choices=["net8", "net10"])
    chk.add_argument("--require", action="append", default=[])
    chk.add_argument("--requirements-json", type=Path)
    chk.add_argument("--project", type=Path, action="append")
    listed = sub.add_parser("list")
    listed.add_argument("--year", type=int, required=True)
    listed.add_argument("--runtime", choices=["net8", "net10"])
    a = ap.parse_args()
    try:
        root = a.root.resolve()
        if a.action == "import":
            add_reference(root, a.year, a.source, a.replace, a.runtime)
        elif a.action == "check":
            return check(root, a.year, needed(a), a.runtime)
        else:
            folder = folder_for(root, a.year, a.runtime)
            dlls = sorted(folder.glob("*.dll")) if folder.exists() else []
            for p in dlls:
                print("%s %d %s" % (p.name, p.stat().st_size, sha256(p)))
            print("%d local reference(s)" % len(dlls))
        return 0
    except (ValueError, OSError, ET.ParseError, json.JSONDecodeError) as error:
        print("ERROR:", error, file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
