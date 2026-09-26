# -*- coding: utf-8 -*-
"""
QX 规则库校验脚本 v2
- 真实错误（阻断）：正则无法编译 / 动作非法 / HTTP明文规则出现在hostname(防呆) / hostname=写在rewrite段内
- 警告：规则域名模式超出 hostname 覆盖范围（可能漏拦截，墨鱼官方原样则提示但不阻断）
- 兼容：filter行(host-suffix等)、IP-ASN 为 QX 合法写法，不报错
用法：python validate_rules.py
"""
import os, re, sys, subprocess

BASE = r"E:\tools\Work\QuantumultX"
REWRITE_DIR = os.path.join(BASE, "rewrites")
FILTER_DIR = os.path.join(BASE, "filters")
SCRIPT_DIR = os.path.join(BASE, "scripts")

VALID_ACTIONS = {
    "reject", "reject-200", "reject-img", "reject-dict", "reject-array",
    "jsonjq-response-body", "script-response-body", "script-response-header",
    "script-request-header", "script-analyze-echo-response", "echo-response",
    "response-body", "request-body", "script-echo-response",
    "302", "307",  # QX URL 重定向
}

FILTER_KEYWORDS = {"host-suffix", "host", "host-keyword", "domain", "domain-suffix",
                   "domain-keyword", "ip-cidr", "ip-cidr6", "ip-asn", "geoip",
                   "user-agent", "url-regex", "final"}

def hostname_match(pattern, host):
    if pattern.startswith("*."):
        base = pattern[2:]
        return host == base or host.endswith("." + base)
    return pattern == host

def extract_host_pattern(regex):
    """从规则正则提取主机模式，返回 (is_http_only, host_pattern)。
    is_http_only=True 表示明文 HTTP 规则。host_pattern 可能含通配(*.)或字符类占位。"""
    r = regex
    is_http = r.startswith("^http:") or (r.startswith("^https?:") and False)
    if r.startswith("^https?:"):
        is_http = False
    elif r.startswith("^http:"):
        is_http = True
    # 去掉协议头
    m = re.search(r'\^https?:\/\/', r)
    if not m:
        return is_http, None
    rest = r[m.end():]
    # 主机部分到第一个 / ? : # 为止
    host_part = re.split(r'[\/\?:#]', rest)[0]
    if not host_part:
        return is_http, None
    # 全部字符类/捕获组占位 → 完全泛化，无法核验
    if host_part.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("*", "").replace("+", "").replace("?", "").replace("{", "").replace("}", "").replace(".", "").replace("-", "").replace("0", "").replace("9", "").replace("|", "") == "":
        return is_http, None
    # 清理转义
    host_part = host_part.replace("\\.", ".")
    # 若含字符类/捕获组，尝试提取最长字面后缀（如 .amap.com / .dsx.ac）
    if "[" in host_part or "(" in host_part or "*" in host_part:
        lit = re.findall(r'([a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.[a-z0-9-]+)', host_part, re.IGNORECASE)
        if lit:
            return is_http, "*." + lit[-1].lower()
        # 提取最后一层域名部分
        doms = re.findall(r'\.([a-z0-9-]+\.[a-z0-9-]{2,24})', host_part, re.IGNORECASE)
        if doms:
            return is_http, "*." + doms[-1].lower()
        return is_http, None
    return is_http, host_part.lower()

def parse_conf(path):
    """解析墨鱼格式 conf。返回 (hostnames, excludes, issues, warnings, stats)"""
    hostnames, excludes = [], []
    errors, warnings = [], []
    rule_count = filter_count = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//") or line.startswith(";"):
            continue
        m = re.match(r'^hostname\s*=\s*(.+)$', line)
        if m:
            for item in m.group(1).split(","):
                item = item.strip()
                if not item:
                    continue
                if item.startswith("-"):
                    excludes.append(item[1:].strip())
                else:
                    hostnames.append(item)
            continue
        # filter 兼容行（host-suffix, xxx, policy）
        first_kw = line.split(",", 1)[0].strip().lower()
        if first_kw in FILTER_KEYWORDS:
            filter_count += 1
            continue
        parts = line.split(None, 3)
        if len(parts) < 3:
            errors.append(f"L{i+1}: 无法解析的规则行: {line[:80]}")
            continue
        regex, kw, action = parts[0], parts[1], parts[2]
        if kw != "url":
            # 可能是其他 filter 语法（如 DOMAIN,xxx,policy）
            if kw.lower() in FILTER_KEYWORDS or first_kw in FILTER_KEYWORDS:
                filter_count += 1
                continue
            errors.append(f"L{i+1}: 第2字段应为 'url'，实际为 '{kw}': {line[:80]}")
            continue
        if action not in VALID_ACTIONS:
            errors.append(f"L{i+1}: 未知动作 '{action}': {line[:80]}")
            continue
        try:
            re.compile(regex)
        except re.error as e:
            errors.append(f"L{i+1}: 正则错误 [{e}]: {regex[:80]}")
            continue
        rule_count += 1
        params = parts[3].strip() if len(parts) > 3 else ""
        # hostname 覆盖核验
        is_http, host_pat = extract_host_pattern(regex)
        if host_pat is None:
            continue
        matched = any(hostname_match(h, host_pat) for h in hostnames)
        if is_http:
            if matched:
                errors.append(f"L{i+1}: [防呆] HTTP明文规则 {host_pat} 出现在 hostname 列表！(HTTP无需MITM)")
        else:
            if not matched:
                # 二次尝试：host_pat 是 *.suffix 时检查是否有同类后缀域名
                warnings.append(f"L{i+1}: 规则主机 {host_pat} 不在 hostname 列表(可能漏拦截) {regex[:60]}")
    return hostnames, excludes, errors, warnings, rule_count, filter_count

def validate_rewrites():
    print("=" * 70)
    print("[1] rewrites/*.conf 重写规则校验")
    print("=" * 70)
    total_e = total_w = 0
    for fname in sorted(os.listdir(REWRITE_DIR)):
        if not fname.endswith(".conf"):
            continue
        path = os.path.join(REWRITE_DIR, fname)
        h, ex, errs, warns, rc, fc = parse_conf(path)
        total_e += len(errs); total_w += len(warns)
        flag = "OK " if not errs else "ERR"
        print(f"[{flag}] {fname} (规则{rc}条/兼容filter行{fc}条/hostname{len(h)}项)")
        for e in errs:
            print(f"    ✗ {e}")
        for w in warns:
            print(f"    ⚠ {w}")
    print(f"\n重写: 错误{total_e} / 警告{total_w}")
    return total_e, total_w

def validate_filters():
    print("=" * 70)
    print("[2] filters/*.list 分流规则格式校验")
    print("=" * 70)
    valid_kw = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6",
                "IP-ASN", "GEOIP", "HOST", "HOST-SUFFIX", "HOST-KEYWORD", "USER-AGENT",
                "URL-REGEX", "IP-ASN6", "PROCESS-NAME", "FINAL", "HOST-WILDCARD", "IP6-CIDR"}
    total_e = 0
    for fname in sorted(os.listdir(FILTER_DIR)):
        path = os.path.join(FILTER_DIR, fname)
        issues = []
        rule_count = 0
        is_yaml = fname.endswith(".yaml") or fname.endswith(".yml")
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for i, raw in enumerate(f):
                line = raw.strip()
                if not line or line.startswith("#") or line.startswith("//") or line.startswith(";"):
                    continue
                # QX filter 可含注释在行内（如 IP-ASN,xxx // 注释）
                body = line.split("//")[0].strip()
                if not body:
                    continue
                # Clash YAML 格式：payload: 头 + "- TYPE,VALUE" 行
                if is_yaml:
                    if body == "payload:":
                        continue
                    if body.startswith("- "):
                        body = body[2:].strip()
                        rule_count += 1
                        parts = body.split(",")
                        kw = parts[0].strip().upper()
                        clash_kw = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR",
                                    "IP-CIDR6", "GEOIP", "SRC-IP-CIDR", "DST-PORT", "PROCESS-NAME",
                                    "MATCH", "RULE-SET"}
                        if kw not in clash_kw:
                            issues.append(f"L{i+1}: 未知Clash类型 '{parts[0]}': {body[:60]}")
                        continue
                    # YAML 非规则行（如 rules: 等）
                    continue
                rule_count += 1
                parts = body.split(",")
                if len(parts) < 2:
                    issues.append(f"L{i+1}: 格式过短: {body[:60]}")
                    continue
                kw = parts[0].strip().upper()
                if kw not in valid_kw:
                    issues.append(f"L{i+1}: 未知类型 '{parts[0]}': {body[:60]}")
        flag = "OK " if not issues else "ERR"
        print(f"[{flag}] {fname} (规则{rule_count}条)")
        for it in issues:
            print(f"    ✗ {it}")
        total_e += len(issues)
    print(f"\n分流: 错误{total_e}")
    return total_e

def validate_scripts():
    print("=" * 70)
    print("[3] scripts/*.js node --check 语法校验")
    print("=" * 70)
    total_e = 0
    for fname in sorted(os.listdir(SCRIPT_DIR)):
        if not fname.endswith(".js"):
            continue
        path = os.path.join(SCRIPT_DIR, fname)
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"[OK ] {fname}")
        else:
            print(f"[ERR] {fname}")
            print(f"    ✗ {r.stderr.strip()[:200]}")
            total_e += 1
    print(f"\n脚本: 错误{total_e}")
    return total_e

if __name__ == "__main__":
    e1, w1 = validate_rewrites()
    e2 = validate_filters()
    e3 = validate_scripts()
    print("=" * 70)
    print(f"校验完成: 错误 {e1 + e2 + e3} / 警告 {w1}")
    print("警告 = 规则主机不在hostname列表，可能漏拦截（墨鱼原样规则按提示处理）")
    sys.exit(1 if (e1 + e2 + e3) > 0 else 0)
