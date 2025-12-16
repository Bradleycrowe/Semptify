import requests

errors = ["/app/vault", "/journey/", "/admin/master", "/maintenance/"]
base = "http://127.0.0.1:5000"

for path in errors:
    try:
        r = requests.get(base + path, timeout=3)
        if r.status_code == 500:
            print(f"\n{path}:")
            # Try to extract error from HTML
            if "Traceback" in r.text:
                lines = r.text.split("\n")
                for i, line in enumerate(lines):
                    if "Traceback" in line or "Error" in line or "File " in line:
                        print(f"  {lines[i][:100]}")
                        if i < len(lines)-1:
                            print(f"  {lines[i+1][:100]}")
                        break
            else:
                print("  (No traceback in response)")
        else:
            print(f"\n{path}: {r.status_code}")
    except Exception as e:
        print(f"\n{path}: {e}")
