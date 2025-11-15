"""
Feature Status Tracking System
Tracks auto-generated features and their implementation status.
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

class FeatureStatus(Enum):
    STUB = "stub"              # Just generated, placeholder logic
    DEVELOPMENT = "development" # Being actively worked on
    BETA = "beta"              # Functional but needs testing
    PRODUCTION = "production"   # Fully implemented and tested
    DEPRECATED = "deprecated"   # Being phased out

class FeatureHealthCheck(Enum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BROKEN = "broken"

class FeatureRegistry:
    """Tracks all auto-generated and manually created features."""
    
    def __init__(self, db_path='data/features.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize feature tracking database."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                feature_type TEXT NOT NULL,
                status TEXT NOT NULL,
                health TEXT DEFAULT 'unknown',
                completion_percent INTEGER DEFAULT 0,
                generated_at TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                blueprint_path TEXT,
                engine_path TEXT,
                template_path TEXT,
                has_tests BOOLEAN DEFAULT 0,
                test_coverage REAL DEFAULT 0.0,
                requires_db BOOLEAN DEFAULT 0,
                requires_api BOOLEAN DEFAULT 0,
                requires_config TEXT,
                validation_errors TEXT,
                usage_count INTEGER DEFAULT 0,
                last_used TEXT,
                notes TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feature_dependencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_name TEXT NOT NULL,
                dependency_type TEXT NOT NULL,
                dependency_name TEXT NOT NULL,
                is_satisfied BOOLEAN DEFAULT 0,
                checked_at TEXT,
                error_message TEXT,
                FOREIGN KEY (feature_name) REFERENCES features(name)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feature_validations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_name TEXT NOT NULL,
                validation_type TEXT NOT NULL,
                passed BOOLEAN NOT NULL,
                message TEXT,
                validated_at TEXT NOT NULL,
                FOREIGN KEY (feature_name) REFERENCES features(name)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_feature(self, name: str, feature_type: str, 
                        status: FeatureStatus = FeatureStatus.STUB,
                        **metadata) -> Dict:
        """Register a new auto-generated feature."""
        conn = sqlite3.connect(self.db_path)
        now = datetime.now().isoformat()
        
        try:
            conn.execute('''
                INSERT INTO features (name, feature_type, status, generated_at, last_updated,
                                    blueprint_path, engine_path, template_path, requires_config)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, feature_type, status.value, now, now,
                metadata.get('blueprint_path'),
                metadata.get('engine_path'),
                metadata.get('template_path'),
                json.dumps(metadata.get('requires_config', {}))
            ))
            conn.commit()
            return {"status": "success", "message": f"Registered {name}"}
        except sqlite3.IntegrityError:
            return {"status": "exists", "message": f"{name} already registered"}
        finally:
            conn.close()
    
    def update_status(self, name: str, status: FeatureStatus, 
                     completion_percent: Optional[int] = None):
        """Update feature implementation status."""
        conn = sqlite3.connect(self.db_path)
        updates = ['status = ?', 'last_updated = ?']
        params = [status.value, datetime.now().isoformat()]
        
        if completion_percent is not None:
            updates.append('completion_percent = ?')
            params.append(completion_percent)
        
        params.append(name)
        conn.execute(f"UPDATE features SET {', '.join(updates)} WHERE name = ?", params)
        conn.commit()
        conn.close()
    
    def add_dependency(self, feature_name: str, dep_type: str, 
                      dep_name: str, is_satisfied: bool = False,
                      error_message: Optional[str] = None):
        """Record a feature dependency."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO feature_dependencies 
            (feature_name, dependency_type, dependency_name, is_satisfied, 
             checked_at, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (feature_name, dep_type, dep_name, is_satisfied, 
              datetime.now().isoformat(), error_message))
        conn.commit()
        conn.close()
    
    def validate_feature(self, name: str, validation_type: str, 
                        passed: bool, message: str):
        """Record validation result."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO feature_validations 
            (feature_name, validation_type, passed, message, validated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, validation_type, passed, message, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_feature(self, name: str) -> Optional[Dict]:
        """Get feature details."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM features WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_features(self, status: Optional[FeatureStatus] = None) -> List[Dict]:
        """Get all features, optionally filtered by status."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        if status:
            cursor = conn.execute('SELECT * FROM features WHERE status = ?', (status.value,))
        else:
            cursor = conn.execute('SELECT * FROM features ORDER BY generated_at DESC')
        
        features = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return features
    
    def get_stub_features(self) -> List[Dict]:
        """Get all stub features that need implementation."""
        return self.get_all_features(FeatureStatus.STUB)
    
    def get_feature_health(self, name: str) -> Dict:
        """Get feature health status with validation results."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Get latest validations
        cursor = conn.execute('''
            SELECT validation_type, passed, message, validated_at
            FROM feature_validations
            WHERE feature_name = ?
            ORDER BY validated_at DESC
            LIMIT 10
        ''', (name,))
        validations = [dict(row) for row in cursor.fetchall()]
        
        # Get unmet dependencies
        cursor = conn.execute('''
            SELECT dependency_type, dependency_name, error_message
            FROM feature_dependencies
            WHERE feature_name = ? AND is_satisfied = 0
        ''', (name,))
        unmet_deps = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Determine health
        if any(not v['passed'] for v in validations):
            health = FeatureHealthCheck.BROKEN
        elif unmet_deps:
            health = FeatureHealthCheck.DEGRADED
        elif validations:
            health = FeatureHealthCheck.HEALTHY
        else:
            health = FeatureHealthCheck.UNKNOWN
        
        return {
            'health': health.value,
            'validations': validations,
            'unmet_dependencies': unmet_deps
        }
    
    def increment_usage(self, name: str):
        """Track feature usage."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            UPDATE features 
            SET usage_count = usage_count + 1,
                last_used = ?
            WHERE name = ?
        ''', (datetime.now().isoformat(), name))
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """Get overall feature statistics."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        stats = {}
        cursor = conn.execute('SELECT status, COUNT(*) as count FROM features GROUP BY status')
        stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
        
        cursor = conn.execute('SELECT AVG(completion_percent) as avg FROM features')
        stats['avg_completion'] = cursor.fetchone()['avg'] or 0
        
        cursor = conn.execute('SELECT COUNT(*) as count FROM features WHERE has_tests = 0')
        stats['missing_tests'] = cursor.fetchone()['count']
        
        cursor = conn.execute('SELECT COUNT(*) as count FROM features WHERE completion_percent < 50')
        stats['needs_work'] = cursor.fetchone()['count']
        
        conn.close()
        return stats


# Global registry instance
_registry = None

def get_feature_registry() -> FeatureRegistry:
    """Get or create the global feature registry."""
    global _registry
    if _registry is None:
        _registry = FeatureRegistry()
    return _registry
