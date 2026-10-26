#!/usr/bin/env python3
# Restore byte-identical large release assets stored as consecutive GitHub parts.
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "assets/HDV_LOGO_ORIGINAL_2048.png": {
        "parts": 8,
        "bytes": 5433767,
        "sha256": "1aae883214da4a2d23e7178c7a7f43983d683e23bad68681389c8d759a67b77a",
    },
    "release/C3D_TOOL_STANDARD_V1_1_HDV_LOGO.zip": {
        "parts": 9,
        "bytes": 5996287,
        "sha256": "016653a79345db406bc4c942c01c14e721eea58d2e231854c51bcb4081acb983",
    },
}

def restore(name, info):
    target = ROOT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest == info["sha256"] and target.stat().st_size == info["bytes"]:
            print(f"OK (existing): {name}")
            return
        raise ValueError(f"Existing file has different content: {target}")
    temporary = target.with_name(target.name + ".tmp")
    try:
        with temporary.open("wb") as output:
            for i in range(1, info["parts"] + 1):
                part = target.with_name(target.name + f".part{i:03d}")
                with part.open("rb") as source:
                    while True:
                        block = source.read(1024 * 1024)
                        if not block:
                            break
                        output.write(block)
        if temporary.stat().st_size != info["bytes"]:
            raise ValueError(f"Size mismatch: {name}")
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        if digest != info["sha256"]:
            raise ValueError(f"SHA256 mismatch: {name}")
        temporary.replace(target)
        print(f"RESTORED: {name} (SHA256 OK)")
    finally:
        if temporary.exists():
            temporary.unlink()

def main():
    failed = 0
    for name, info in FILES.items():
        try:
            restore(name, info)
        except (OSError, ValueError) as exc:
            failed += 1
            print(f"FAILED: {exc}", file=sys.stderr)
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
