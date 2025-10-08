#!/usr/bin/env python
import sys, json, collections

if len(sys.argv) != 3:
    print("Usage: sbom_diff.py <old.json> <new.json>", file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1],'r') as f: old = json.load(f)
with open(sys.argv[2],'r') as f: new = json.load(f)

# Try to support Syft & CycloneDX minimal shapes (very loose heuristic)

def extract_components(doc):
    comps = []
    if isinstance(doc, dict):
        if 'components' in doc and isinstance(doc['components'], list):
            for c in doc['components']:
                name = c.get('name') or c.get('componentName') or c.get('id')
                version = c.get('version') or c.get('componentVersion')
                purl = c.get('purl')
                if name:
                    comps.append((name, version, purl))
        elif 'artifacts' in doc and isinstance(doc['artifacts'], list):  # syft JSON
            for a in doc['artifacts']:
                name = a.get('name')
                version = a.get('version')
                purl = None
                if name:
                    comps.append((name, version, purl))
    return comps

old_set = set(extract_components(old))
new_set = set(extract_components(new))
added = sorted(new_set - old_set)
removed = sorted(old_set - new_set)

print("SBOM DIFF SUMMARY\n=================")
print(f"Old file: {sys.argv[1]}")
print(f"New file: {sys.argv[2]}\n")
print(f"Added components: {len(added)}")
for a in added[:50]:
    print(" +", a[0], a[1] or '')
print(f"\nRemoved components: {len(removed)}")
for r in removed[:50]:
    print(" -", r[0], r[1] or '')

if len(added) > 50 or len(removed) > 50:
    print("\n(Results truncated)")
