              ype for Semptify

Run (Windows PowerShell):

```powershell
Set-Location -LiteralPath 'D:\Semptify\SemptifyGUI\app-backend'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000
