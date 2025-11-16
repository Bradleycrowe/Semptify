"""Self Maintenance Engine
Performs automated cleanup, health checks, and preparatory update tasks.
"""
from __future__ import annotations
import os, sqlite3, hashlib, json, time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

LOG_DIR = Path('logs')
UPLOAD_DIR = Path('uploads')
DATA_DIR = Path('data')
VAULT_DIR = UPLOAD_DIR / 'vault'

class MaintenanceEngine:
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.tasks_run: List[str] = []

    def _record(self, key: str, value: Any):
        self.results[key] = value
        self.tasks_run.append(key)

    # Task: Rotate logs (simple size/date archival)
    def rotate_logs(self) -> Dict[str, Any]:
        LOG_DIR.mkdir(exist_ok=True)
        archived = []
        for p in LOG_DIR.glob('*.log'):
            if p.stat().st_size > 1_000_000:  # >1MB
                ts = datetime.utcnow().strftime('%Y%m%d%H%M')
                new_name = p.with_name(p.stem + f'-archive-{ts}.log')
                p.rename(new_name)
                archived.append(str(new_name))
        result = {'archived': archived, 'count': len(archived)}
        self._record('rotate_logs', result)
        return result

    # Task: Database vacuum (if sqlite present)
    def vacuum_db(self) -> Dict[str, Any]:
        db_path = Path('users.db')
        if not db_path.exists():
            result = {'status':'missing'}
        else:
            before = db_path.stat().st_size
            conn = sqlite3.connect(str(db_path))
            conn.execute('VACUUM')
            conn.close()
            after = db_path.stat().st_size
            result = {'status':'ok','before_bytes': before,'after_bytes': after,'bytes_reclaimed': before-after}
        self._record('vacuum_db', result)
        return result

    # Task: Cleanup orphaned evolution artifacts (>14 days)
    def cleanup_orphans(self) -> Dict[str, Any]:
        target = DATA_DIR / 'evolution_history.json'
        removed = []
        # Example: remove stale temp files in data/tmp
        tmp_dir = DATA_DIR / 'tmp'
        if tmp_dir.exists():
            cutoff = time.time() - (14*86400)
            for f in tmp_dir.glob('*'):
                if f.is_file() and f.stat().st_mtime < cutoff:
                    removed.append(str(f))
                    f.unlink(missing_ok=True)
        result = {'removed': removed, 'count': len(removed)}
        self._record('cleanup_orphans', result)
        return result

    # Task: Remove zero-byte uploads
    def cleanup_zero_byte_uploads(self) -> Dict[str, Any]:
        deleted = []
        if VAULT_DIR.exists():
            for root, _, files in os.walk(VAULT_DIR):
                for f in files:
                    p = Path(root) / f
                    try:
                        if p.stat().st_size == 0:
                            deleted.append(str(p))
                            p.unlink(missing_ok=True)
                    except FileNotFoundError:
                        pass
        result = {'deleted': deleted,'count': len(deleted)}
        self._record('cleanup_zero_byte_uploads', result)
        return result

    # Task: Verify storage hashes (placeholder)
    def verify_storage_hashes(self) -> Dict[str, Any]:
        checked = 0
        mismatches = []
        # Future: read certificate JSONs and recompute hash
        result = {'checked': checked,'mismatches': mismatches}
        self._record('verify_storage_hashes', result)
        return result

    # Task: Dependency audit stub
    def dependency_audit_stub(self) -> Dict[str, Any]:
        req = Path('requirements.txt')
        outdated = []
        if req.exists():
            for line in req.read_text().splitlines():
                if '==' in line:
                    pkg, ver = line.split('==',1)
                    # Placeholder heuristic: flag version lower than arbitrary threshold
                    if any(ver.startswith(prefix) for prefix in ['0','1.0']):
                        outdated.append({'package': pkg,'version': ver,'suggestion':'Check for newer stable release'})
        result = {'outdated': outdated,'count': len(outdated)}
        self._record('dependency_audit_stub', result)
        return result

    # Task: Feature registry refresh (stub: count features)
    def feature_registry_refresh(self) -> Dict[str, Any]:
        reg_file = DATA_DIR / 'features.db'
        status = 'present' if reg_file.exists() else 'missing'
        result = {'registry_status': status}
        self._record('feature_registry_refresh', result)
        return result

    # Task: Security stub scan
    def security_stub_scan(self) -> Dict[str, Any]:
        suspicious = []
        for py in Path('.').glob('*.py'):
            txt = py.read_text(errors='ignore')
            if 'exec(' in txt or 'eval(' in txt:
                suspicious.append(str(py))
        result = {'suspicious_files': suspicious,'count': len(suspicious)}
        self._record('security_stub_scan', result)
        return result

    def run_all(self) -> Dict[str, Any]:
        self.results = {}
        self.tasks_run = []
        self.rotate_logs()
        self.vacuum_db()
        self.cleanup_orphans()
        self.cleanup_zero_byte_uploads()
        self.verify_storage_hashes()
        self.dependency_audit_stub()
        self.feature_registry_refresh()
        self.security_stub_scan()
        summary = {
            'run_at': datetime.utcnow().isoformat(),
            'tasks': self.tasks_run,
            'results': self.results
        }
        return summary

# Singleton accessor
_instance: MaintenanceEngine | None = None

def get_maintenance_engine() -> MaintenanceEngine:
    global _instance
    if _instance is None:
        _instance = MaintenanceEngine()
    return _instance
