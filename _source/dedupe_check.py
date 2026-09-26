# -*- coding: utf-8 -*-
"""QX规则去重校验：检测使用中规则文件内的重复条目与跨文件重复。"""
import os, re, sys
from collections import defaultdict

ROOT = r"E:\tools\Work\QuantumultX"

# 使用中规则文件范围
REWRITE_FILES = ["MyAdBlock.conf", "test.conf", "MyProfile.conf"]
REWRITE_FILES += [os.path.join("rewrites", f) for f in os.listdir(os.path.join(ROOT, "rewrites")) if f.endswith(".conf")]
FILTER_FILES = ["MyProfile.conf"]
FILTER_FILES += [os.path.join("filters", f) for f in os.listdir(os.path.join(ROOT, "filters")) if f.endswith((".list", ".conf"))]

def read_lines(path):
    with open(os.path.join(ROOT, path), encoding="utf-8-sig", errors="replace") as f:
        return [ln.rstrip("\n\r") for ln in f]

def is_comment(line):
    s = line.strip()
    return (not s) or s.startswith(("#", "//", ";")) or (s.startswith("[") and s.endswith("]"))

def norm_rule(line):
    """规范化：去首尾空格、压缩连续空白"""
    s = line.strip()
    return re.sub(r"\s+", " ", s)

def extract_rules(lines):
    rules = []
    in_section = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("[") and s.endswith("]"):
            in_section = s[1:-1]
            continue
        if is_comment(ln):
            continue
        # 跳过 hostname/资源解析器行
        if s.startswith(("hostname", "host,", "host-suffix", "resource_parser")):
            continue
        # 仅收录规则形态的行
        if re.match(r"^(https?://|\^)", s, re.I) or re.match(r"^(DOMAIN|IP-CIDR|GEOIP|FINAL|USER-AGENT|URL-REGEX|HOST),", s, re.I):
            rules.append(norm_rule(s))
        else:
            # 收集无法归类的非注释行，供人工核对（可能漏网规则）
            rules.append(("[UNCLASSIFIED] " + s))
    return rules

report = []
# 1) 文件内重复
for path in REWRITE_FILES + FILTER_FILES:
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        continue
    lines = read_lines(path)
    rules = extract_rules(lines)
    cnt = defaultdict(int)
    for r in rules:
        cnt[r] += 1
    dups = {r: c for r, c in cnt.items() if c > 1}
    if dups:
        report.append(f"\n[文件内重复] {path} 共{len(rules)}条规则, {len(dups)}条重复:")
        for r, c in sorted(dups.items(), key=lambda x: -x[1]):
            report.append(f"  x{c}  {r[:130]}")
    else:
        report.append(f"\n[文件内重复] {path} 共{len(rules)}条规则: 无重复 ✓")

# 2) 跨文件重复
all_rules = defaultdict(list)  # rule -> [files]
for path in REWRITE_FILES + FILTER_FILES:
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        continue
    for r in extract_rules(read_lines(path)):
        all_rules[r].append(path)

report.append("\n" + "=" * 60 + "\n[跨文件重复]")
cross = {r: fs for r, fs in all_rules.items() if len(fs) > 1}
# 分组：rewrites内部 / rewrites vs 大配置 / 大配置之间 / filters
groups = {"rewrites内部": [], "rewrites↔MyAdBlock/test": [], "MyAdBlock↔test": [], "filters内部": [], "其他": []}
for r, fs in cross.items():
    rews = [f for f in fs if f.startswith("rewrites")]
    bigs = [f for f in fs if f in ("MyAdBlock.conf", "test.conf")]
    filt = [f for f in fs if f.startswith("filters")]
    if len(rews) > 1:
        groups["rewrites内部"].append((r, fs))
    elif rews and bigs:
        groups["rewrites↔MyAdBlock/test"].append((r, fs))
    elif len(bigs) > 1:
        groups["MyAdBlock↔test"].append((r, fs))
    elif len(filt) > 1:
        groups["filters内部"].append((r, fs))
    else:
        groups["其他"].append((r, fs))

for gname, items in groups.items():
    report.append(f"\n--- {gname}: {len(items)} 条 ---")
    for r, fs in items[:40]:
        report.append(f"  [{','.join(fs)}] {r[:120]}")
    if len(items) > 40:
        report.append(f"  ... 共{len(items)}条, 仅显示前40条")

out = "\n".join(report)
print(out)
with open(os.path.join(ROOT, "_source", "dedupe-report.txt"), "w", encoding="utf-8") as f:
    f.write(out)
print(f"\n\n报告已写入: _source/dedupe-report.txt")
