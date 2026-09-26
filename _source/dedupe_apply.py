# -*- coding: utf-8 -*-
"""文件内重复规则去重：保留每个规则行首次出现的位置，删除后续完全相同的重复行。
仅处理规则行（非注释/空行/段名/hostname），保留原文格式不变。"""
import os, re
from collections import defaultdict

ROOT = r"E:\tools\Work\QuantumultX"
TARGETS = [
    "MyAdBlock.conf",
    "test.conf",
    os.path.join("rewrites", "startup-ads.conf"),
    os.path.join("filters", "streaming.list"),
    os.path.join("filters", "unbreak.list"),
    os.path.join("filters", "global-proxy.list"),
]

def is_nonrule(line):
    s = line.strip()
    if not s:
        return True
    if s.startswith(("#", "//", ";")):
        return True
    if s.startswith("[") and s.endswith("]"):
        return True
    if s.startswith(("hostname", "host,", "host-suffix", "resource_parser")):
        return True
    return False

def norm(s):
    return re.sub(r"\s+", " ", s.strip())

total_removed = 0
for rel in TARGETS:
    full = os.path.join(ROOT, rel)
    if not os.path.exists(full):
        print(f"[跳过] {rel} 不存在")
        continue
    with open(full, encoding="utf-8-sig", errors="replace") as f:
        lines = f.readlines()
    seen = set()
    kept = []
    removed = 0
    for ln in lines:
        body = ln.rstrip("\r\n")
        if is_nonrule(body):
            kept.append(ln)
            continue
        key = norm(body)
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        kept.append(ln)
    if removed:
        with open(full, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(kept)
        total_removed += removed
        print(f"[已清理] {rel}: 移除 {removed} 条重复")
    else:
        print(f"[无需处理] {rel}")
print(f"\n共移除 {total_removed} 条重复规则")
