import sys
sys.path.insert(0, "C:\\Semptify\\Semptify")

# Suppress startup output
import io
import contextlib

f = io.StringIO()
with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
    from Semptify import app

print("Testing /app/vault route...")
with app.test_client() as client:
    try:
        response = client.get("/app/vault")
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print("ERROR DETAILS:")
            data = response.get_data(as_text=True)
            # Extract error from response
            import re
            if "NameError" in data:
                match = re.search(r"NameError: (.+?)(?:<|$)", data)
                if match:
                    print(f"  NameError: {match.group(1)}")
            if "KeyError" in data:
                match = re.search(r"KeyError: (.+?)(?:<|$)", data)
                if match:
                    print(f"  KeyError: {match.group(1)}")
            # Find the line number
            match = re.search(r'File ".*vault\.py", line (\d+)', data)
            if match:
                print(f"  Location: vault.py line {match.group(1)}")
    except Exception as e:
        print(f"Exception: {e}")
