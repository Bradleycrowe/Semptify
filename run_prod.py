"""
Semptify Production Server
Run with: python run_prod.py
"""
import os
import uvicorn

# Production settings
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))
WORKERS = int(os.environ.get("WORKERS", 4))

# R2 defaults (set these in environment)
os.environ.setdefault("R2_ACCOUNT_ID", "be2a39cd3624261169fa8e800d75923f")
os.environ.setdefault("R2_BUCKET", "semptify")
os.environ.setdefault("STORAGE_TYPE", "r2")

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    SEMPTIFY PRODUCTION                       ║
║              Storage-as-Identity Platform                    ║
╠══════════════════════════════════════════════════════════════╣
║  Host: {HOST}                                              
║  Port: {PORT}                                              
║  Workers: {WORKERS}                                        
║  Storage: {os.environ.get('STORAGE_TYPE', 'r2')}           
║  R2 Bucket: {os.environ.get('R2_BUCKET', 'semptify')}      
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        workers=WORKERS,
        log_level="info",
        access_log=True,
    )
