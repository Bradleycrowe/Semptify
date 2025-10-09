#!/usr/bin/env python
"""Compare two Trivy JSON reports (old, new) and emit a brief delta summary.

Usage: sbom_vuln_delta.py <old_trivy.json> <new_trivy.json>
Exits non-zero (2) if new critical/high count increased.
"""
from __future__ import annotations
import sys, json

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

def main():
    if len(sys.argv) != 3:
        print("Usage: sbom_vuln_delta.py <old_trivy.json> <new_trivy.json>", file=sys.stderr)
        return 1
    old = load(sys.argv[1])
    new = load(sys.argv[2])
    ocrit, ohigh = summarize(old)
    ncrit, nhigh = summarize(new)
    dcrit = ncrit - ocrit
    dhigh = nhigh - ohigh
    status = 'OK'
    exit_code = 0
    if dcrit > 0 or dhigh > 0:
        status = 'REGRESSION'
        exit_code = 2
    print('TRIVY VULN DELTA\n================')
    print(f'Old: critical={ocrit} high={ohigh}')
    print(f'New: critical={ncrit} high={nhigh}')
    print(f'Delta: critical={dcrit:+} high={dhigh:+}')
    print(f'Status: {status}')
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
