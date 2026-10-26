#!/usr/bin/env python3
"""Generate a current-only Civil 3D algorithm inventory from live C# source metadata.

This checker detects source changes but cannot infer the semantic truth of function descriptions.
"""
import argparse
import hashlib
from pathlib import Path
import re
import sys

META_NAME = re.compile(r"^\s*//\s*HDV-ALGO-NAME:\s*(.*?)\s*$", re.M)
META_FUNCTION = re.compile(r"^\s*//\s*HDV-ALGO-FUNCTION:\s*(.*?)\s*$", re.M)
META_STATUS = re.compile(r"^\s*//\s*HDV-ALGO-STATUS:\s*(.*?)\s*$", re.M)
EXCLUDED_DIRS = {"bin", "obj", ".git", "node_modules", "legacy", "old", "archive", "archived", "backup", "backups", "tests", "test"}


def collect(root, source, compiled_files=None):
    errors, items, attest = [], [], []
    if not source.exists():
        return items, attest, errors, 0
    candidates = sorted(p for p in source.rglob("*.cs") if p.is_file()
                        and not set(x.lower() for x in p.relative_to(source).parts[:-1]) & EXCLUDED_DIRS)
    allowed = None
    if compiled_files is not None:
        if not compiled_files.exists():
            raise ValueError(f"Không tìm thấy danh sách compiled source: {compiled_files}")
        allowed = {line.strip().replace('\\', '/') for line in compiled_files.read_text(encoding="utf8").splitlines()
                   if line.strip() and not line.lstrip().startswith('#')}
    scanned = 0
    for path in candidates:
        relative = path.relative_to(root).as_posix()
        if allowed is not None and relative not in allowed:
            continue
        scanned += 1
        txt = path.read_text(encoding="utf-8-sig")
        names = META_NAME.findall(txt)
        funcs = META_FUNCTION.findall(txt)
        status = META_STATUS.findall(txt)
        if status and any(x.strip().lower() not in ("active", "current") for x in status):
            errors.append(f"{relative}: file thuật toán cũ/không active còn trong source: {status}")
            continue
        in_algorithms_folder = any(x.lower() in ("algorithms", "algorithm") for x in path.relative_to(source).parts[:-1])
        if not names and not funcs:
            if in_algorithms_folder:
                errors.append(f"{relative}: thuật toán thiếu HDV-ALGO-NAME và HDV-ALGO-FUNCTION")
            continue
        if len(names) != len(funcs) or not names or not funcs:
            errors.append(f"{relative}: metadata NAME/FUNCTION không đủ cặp")
            continue
        if any(not x.strip() for x in names + funcs):
            errors.append(f"{relative}: NAME/FUNCTION bị trống")
            continue
        for n, f in zip(names, funcs):
            items.append((n.strip(), f.strip(), relative))
        attest.append((relative, hashlib.sha256(path.read_bytes()).hexdigest()))
    seen = {}
    for name, _, file in items:
        key = name.casefold()
        if key in seen:
            errors.append(f"Trùng tên thuật toán '{name}' ở {seen[key]} và {file}")
        seen[key] = file
    return sorted(items, key=lambda z: (z[0].casefold(), z[2])), sorted(attest), errors, scanned


def output(items, attest, scan_count, source_label):
    out = [
        "# DANH MỤC THUẬT TOÁN HIỆN HÀNH — CIVIL 3D TOOL",
        "",
        "**Đây là danh mục tạo từ mã C# đang có, không phải lịch sử thuật toán.**",
        "",
        f"- Thư mục quét: `{source_label}`",
        f"- Số tệp C# đã quét: **{scan_count}**",
        f"- Số thuật toán có metadata hợp lệ: **{len(items)}**",
        "",
        "| Tên thuật toán | Chức năng |",
        "|---|---|",
    ]
    for name, function, _ in items:
        esc = lambda x: x.replace(chr(92), chr(92)+chr(92)).replace("|", chr(92)+"|").replace(chr(10), " ")
        out.append(f"| `{esc(name)}` | {esc(function)} |")
    if not items:
        out.extend(["", "*Chưa có thuật toán được xác nhận từ mã nguồn trong phạm vi quét. Không tự thêm các thuật toán theo đặc tả hoặc ZIP cũ.*"])
    out.extend(["", "<!-- HDV-ALGO-SOURCE-ATTESTATION", *[f"{path} sha256:{digest}" for path, digest in attest], "END-HDV-ALGO-SOURCE-ATTESTATION -->", ""])
    return "\n".join(out)


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Sinh lại danh mục thuật toán chỉ từ mã nguồn hiện hành")
    parser.add_argument("--source-root", default="src", help="Thư mục mã nguồn C# bên trong tool")
    parser.add_argument("--output", default="ALGORITHM_INVENTORY.md", help="Tệp danh mục đầu ra")
    parser.add_argument("--compiled-files", help="Danh sách đường dẫn *.cs thực tế được biên dịch (đường dẫn tương đối so với root), một tệp/dòng")
    parser.add_argument("--require-source", action="store_true", help="Bắt buộc có source C# khi bàn giao tool")
    parser.add_argument("--check", action="store_true", help="Không sửa file; trả mã lỗi nếu chưa cập nhật")
    args = parser.parse_args()
    source = (root / args.source_root).resolve()
    output_file = (root / args.output).resolve()
    try:
        source.relative_to(root)
        output_file.relative_to(root)
        compiled = (root / args.compiled_files).resolve() if args.compiled_files else None
        items, attest, errors, scan_count = collect(root, source, compiled)
    except (ValueError, OSError, UnicodeError) as error:
        print("ERROR:", error, file=sys.stderr)
        return 2
    if args.require_source and scan_count == 0:
        errors.append("Không tìm thấy file nguồn C# thực tế để lập bảng thuật toán")
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 2
    body = output(items, attest, scan_count, Path(args.source_root).as_posix())
    if args.check:
        if not output_file.exists() or output_file.read_text(encoding="utf8") != body:
            print(f"FAIL: {args.output} chưa đồng bộ với mã nguồn (hãy chạy script không có --check)", file=sys.stderr)
            return 1
        print(f"PASS: {args.output} đồng bộ, {len(items)} thuật toán trong {scan_count} tệp C#")
        return 0
    if not output_file.exists() or output_file.read_text(encoding="utf8") != body:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(body, encoding="utf8")
        print(f"UPDATED: {args.output} — {len(items)} thuật toán")
    else:
        print(f"UNCHANGED: {args.output} — {len(items)} thuật toán")
    return 0

if __name__ == "__main__":
    sys.exit(main())
