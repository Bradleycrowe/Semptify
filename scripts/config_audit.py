"""Config audit script

Scans the repository for environment variable access, external API mentions, and runtime paths.
Generates a JSON report at `logs/config_audit_report.json` and prints a human summary.

Usage:
    python scripts/config_audit.py

This script is intentionally conservative and runs without network access.
"""
import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ENV_PATTERNS = [
    re.compile(r"os\.environ\.get\(['\"]([A-Z0-9_]+)['\"]"),
    re.compile(r"os\.environ\[['\"]([A-Z0-9_]+)['\"]\]"),
    re.compile(r"os\.getenv\(['\"]([A-Z0-9_]+)['\"]"),
]

EXTERNAL_HINTS = [
    'openai', 'azure', 'ollama', 'github', 'bluenotary', 'requests', 'http', 'https', 'api'
]

report = {
    'env_vars': {},
    'files_scanned': 0,
    'external_hints': {},
}

def scan_file(p: Path):
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        return
    report['files_scanned'] += 1
    for pat in ENV_PATTERNS:
        for m in pat.finditer(text):
            name = m.group(1)
            report['env_vars'].setdefault(name, []).append(str(p))
    for hint in EXTERNAL_HINTS:
        if hint in text.lower():
            report['external_hints'].setdefault(hint, []).append(str(p))

def main():
    for p in ROOT.rglob('*.py'):
        scan_file(p)

    # Add common runtime dirs check
    runtime_dirs = ['uploads', 'logs', 'copilot_sync', 'final_notices', 'security']
    runtime = {}
    for d in runtime_dirs:
        p = ROOT.joinpath(d)
        runtime[d] = {
            'exists': p.exists(),
            'writable': os.access(str(p), os.W_OK) if p.exists() else False,
            'path': str(p),
        }
    report['runtime_directories'] = runtime

    out_path = ROOT.joinpath('logs', 'config_audit_report.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')

    print("Config audit complete")
    print(f"Files scanned: {report['files_scanned']}")
    print(f"Unique env vars found: {len(report['env_vars'])}")
    if report['external_hints']:
        print("External service hints:")
        for k, v in report['external_hints'].items():
            print(f" - {k}: {len(v)} files")
    print(f"Report written: {out_path}")


if __name__ == '__main__':
    main()
