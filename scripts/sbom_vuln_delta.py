#!/usr/bin/env python
"""Compare two Trivy JSON reports (old, new) and emit a brief delta summary.

Usage: sbom_vuln_delta.py <old_trivy.json> <new_trivy.json> [--allowlist security/vuln_allowlist.json] [--json-out delta.json]
Exits non-zero (2) if new critical/high count increased (after allowlist suppression).
"""
from __future__ import annotations
import sys, json, argparse, datetime

def load(path: str):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: failed reading {path}: {e}", file=sys.stderr)
        sys.exit(1)

def summarize(doc):
    # Trivy SARIF or JSON scanning output forms vary; handle basic JSON (results list)
    critical = high = 0
    if isinstance(doc, dict):
        # syft/trivy action may put results under 'Results'
        results = doc.get('Results') or []
        for r in results:
            vulns = r.get('Vulnerabilities') or []
            for v in vulns:
                sev = (v.get('Severity') or '').upper()
                if sev == 'CRITICAL':
                    critical += 1
                elif sev == 'HIGH':
                    high += 1
    return critical, high

def load_allowlist(path: str):
    try:
        with open(path,'r') as f:
            data = json.load(f)
        entries = {}
        today = datetime.date.today()
        for item in data:
            cve = item.get('cve')
            expires = item.get('expires')
            if not cve:
                continue
            if expires:
                try:
                    exp_date = datetime.date.fromisoformat(expires)
                    if exp_date < today:
                        continue  # expired allowlist entry
                except Exception:
                    pass
            entries[cve] = item
        return entries
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"WARN: allowlist load failed: {e}", file=sys.stderr)
        return {}

def extract_vulns(doc):
    vulns = []
    if isinstance(doc, dict):
        results = doc.get('Results') or []
        for r in results:
            for v in r.get('Vulnerabilities') or []:
                vulns.append(v)
    return vulns

def apply_allowlist(vulns, allow):
    kept = []
    suppressed = []
    for v in vulns:
        cve = v.get('VulnerabilityID') or v.get('CVEID')
        if cve and cve in allow:
            suppressed.append(v)
        else:
            kept.append(v)
    return kept, suppressed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('old')
    ap.add_argument('new')
    ap.add_argument('--allowlist', default='security/vuln_allowlist.json')
    ap.add_argument('--json-out', default=None)
    args = ap.parse_args()
    old = load(args.old)
    new = load(args.new)
    ocrit, ohigh = summarize(old)
    ncrit, nhigh = summarize(new)
    dcrit = ncrit - ocrit
    dhigh = nhigh - ohigh
    allow = load_allowlist(args.allowlist)
    old_vulns = extract_vulns(old)
    new_vulns = extract_vulns(new)
    new_kept, new_supp = apply_allowlist(new_vulns, allow)
    # Recompute counts after suppression
    ncrit_eff = sum(1 for v in new_kept if (v.get('Severity') or '').upper()=='CRITICAL')
    nhigh_eff = sum(1 for v in new_kept if (v.get('Severity') or '').upper()=='HIGH')
    dcrit_eff = ncrit_eff - ocrit
    dhigh_eff = nhigh_eff - ohigh
    status = 'OK'
    exit_code = 0
    if dcrit_eff > 0 or dhigh_eff > 0:
        status = 'REGRESSION'
        exit_code = 2
    print('TRIVY VULN DELTA\n================')
    print(f'Old: critical={ocrit} high={ohigh}')
    print(f'New(raw): critical={ncrit} high={nhigh}')
    print(f'New(effective): critical={ncrit_eff} high={nhigh_eff} (allowlist suppressed {len(new_supp)})')
    print(f'Delta(effective): critical={dcrit_eff:+} high={dhigh_eff:+}')
    print(f'Status: {status}')
    if args.json_out:
        out = {
            'old': {'critical': ocrit, 'high': ohigh},
            'new_raw': {'critical': ncrit, 'high': nhigh},
            'new_effective': {'critical': ncrit_eff, 'high': nhigh_eff},
            'delta_effective': {'critical': dcrit_eff, 'high': dhigh_eff},
            'suppressed': len(new_supp),
            'status': status
        }
        with open(args.json_out,'w') as f:
            json.dump(out, f, indent=2)
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
