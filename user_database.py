"""
User database for Semptify using SQLite
More robust than JSON for learning system and concurrent access
"""
import sqlite3
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import os

DB_PATH = "security/users.db"

def _get_db():
    """Get database connection"""
    os.makedirs("security", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    return conn

def init_database():
    """Initialize database tables"""
    conn = _get_db()
    cursor = conn.cursor()

    # Pending users table (for verification)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            county TEXT NOT NULL,
            state TEXT NOT NULL,
            zip TEXT NOT NULL,
            verification_method TEXT NOT NULL,
            code_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            attempts INTEGER DEFAULT 0
        )
    ''')

    # Verified users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            county TEXT NOT NULL,
            state TEXT NOT NULL,
            zip TEXT NOT NULL,
            verified_at TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            last_login TEXT,
            login_count INTEGER DEFAULT 0
        )
    ''')
    
    # Add dashboard columns if they don't exist (migration for learning dashboard)
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'location' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN location TEXT DEFAULT 'MN'")
    if 'issue_type' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN issue_type TEXT DEFAULT 'rent'")
    if 'stage' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN stage TEXT DEFAULT 'SEARCHING'")
    if 'created_at' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN created_at TEXT")

    # User learning profile table (for adaptive learning system)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_learning_profiles (
            user_id TEXT PRIMARY KEY,
            complexity_preference TEXT DEFAULT 'medium',
            learning_style TEXT DEFAULT 'balanced',
            completed_modules TEXT DEFAULT '[]',
            current_journey TEXT,
            journey_progress INTEGER DEFAULT 0,
            last_activity TEXT,
            total_sessions INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # User interactions log (for learning system to adapt)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            interaction_type TEXT NOT NULL,
            module_name TEXT,
            timestamp TEXT NOT NULL,
            duration_seconds INTEGER,
            success BOOLEAN,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # User situation data (captured during onboarding/setup)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_situations (
            user_id TEXT PRIMARY KEY,
            issue_type TEXT,
            urgency TEXT,
            notice_date TEXT,
            has_evidence INTEGER DEFAULT 0,
            has_attorney INTEGER DEFAULT 0,
            situation_details TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def hash_code(code: str) -> str:
    """Hash a verification code for storage"""
    return hashlib.sha256(code.encode()).hexdigest()

def check_existing_user(email: str, phone: str) -> bool:
    """
    Check if email or phone already exists in verified users table
    Returns: True if user exists, False otherwise
    """
    conn = _get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id FROM users 
        WHERE email = ? OR phone = ?
    ''', (email, phone))
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def create_pending_user(form_data: dict, verification_method: str) -> Tuple[str, str]:
    """
    Create a pending user registration
    Returns: (user_id, verification_code)
    """
    conn = _get_db()
    cursor = conn.cursor()

    # Generate unique user ID
    user_id = secrets.token_urlsafe(16)

    # Generate verification code
    code = generate_verification_code()

    # Store pending user with hashed code
    cursor.execute('''
        INSERT INTO pending_users (
            user_id, first_name, last_name, email, phone,
            address, city, county, state, zip,
            verification_method, code_hash, created_at, expires_at, attempts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    ''', (
        user_id,
        form_data.get('first_name'),
        form_data.get('last_name'),
        form_data.get('email'),
        form_data.get('phone'),
        form_data.get('address'),
        form_data.get('city'),
        form_data.get('county'),
        form_data.get('state'),
        form_data.get('zip'),
        verification_method,
        hash_code(code),
        datetime.now().isoformat(),
        (datetime.now() + timedelta(minutes=10)).isoformat()
    ))

    conn.commit()
    conn.close()

    return user_id, code

def verify_code(user_id: str, code: str) -> Tuple[bool, Optional[str]]:
    """
    Verify a code for a pending user
    Returns: (success, error_message)
    """
    conn = _get_db()
    cursor = conn.cursor()

    # Get pending user
    cursor.execute('SELECT * FROM pending_users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        conn.close()
        return False, "Invalid verification session"

    # Check expiration
    expires_at = datetime.fromisoformat(user_data['expires_at'])
    if datetime.now() > expires_at:
        conn.close()
        return False, "Verification code expired. Please register again."

    # Check attempts
    if user_data['attempts'] >= 5:
        conn.close()
        return False, "Too many attempts. Please register again."

    # Verify code
    if hash_code(code) != user_data['code_hash']:
        # Increment attempts
        cursor.execute(
            'UPDATE pending_users SET attempts = attempts + 1 WHERE user_id = ?',
            (user_id,)
        )
        conn.commit()
        remaining = 5 - (user_data['attempts'] + 1)
        conn.close()
        return False, f"Invalid code. {remaining} attempts remaining."

    # Code is valid - activate user OR treat as login if already exists
    try:
        # Check if user already exists (login flow)
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        existing = cursor.fetchone()

        if existing:
            # Existing verified user: update login stats and remove pending
            cursor.execute(
                'UPDATE users SET last_login = ?, login_count = login_count + 1 WHERE user_id = ?',
                (datetime.now().isoformat(), user_id)
            )
            cursor.execute('DELETE FROM pending_users WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True, None

        # New user: insert record
        cursor.execute('''
            INSERT INTO users (
                user_id, first_name, last_name, email, phone,
                address, city, county, state, zip,
                verified_at, status, login_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', 1)
        ''', (
            user_id,
            user_data['first_name'],
            user_data['last_name'],
            user_data['email'],
            user_data['phone'],
            user_data['address'],
            user_data['city'],
            user_data['county'],
            user_data['state'],
            user_data['zip'],
            datetime.now().isoformat()
        ))

        # Create learning profile for user
        cursor.execute('''
            INSERT INTO user_learning_profiles (
                user_id, last_activity, total_sessions
            ) VALUES (?, ?, 0)
        ''', (user_id, datetime.now().isoformat()))

        # Remove from pending
        cursor.execute('DELETE FROM pending_users WHERE user_id = ?', (user_id,))

        conn.commit()
        conn.close()

        # Sync to R2 after successful verification
        _sync_to_r2_if_enabled()
        
        return True, None

    except sqlite3.IntegrityError as e:
        conn.close()
        if 'email' in str(e):
            return False, "Email already registered. Please log in instead."
        return False, "Registration error. Please try again."

def get_pending_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get pending user data"""
    conn = _get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM pending_users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    conn.close()

    if user_data:
        return dict(user_data)
    return None

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get verified user data"""
    conn = _get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    conn.close()

    if user_data:
        return dict(user_data)
    return None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    conn = _get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_data = cursor.fetchone()

    conn.close()

    if user_data:
        return dict(user_data)
    return None

def update_user_login(user_id: str):
    """Update user's last login and increment login count"""
    conn = _get_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET last_login = ?, login_count = login_count + 1
        WHERE user_id = ?
    ''', (datetime.now().isoformat(), user_id))

    conn.commit()
    conn.close()

def resend_verification_code(user_id: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Resend verification code to a pending user
    Returns: (success, new_code, error_message)
    """
    conn = _get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM pending_users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        conn.close()
        return False, None, "Invalid verification session"

    # Generate new code
    code = generate_verification_code()

    # Update pending user with new code and extended expiration
    cursor.execute('''
        UPDATE pending_users
        SET code_hash = ?, expires_at = ?, attempts = 0
        WHERE user_id = ?
    ''', (
        hash_code(code),
        (datetime.now() + timedelta(minutes=10)).isoformat(),
        user_id
    ))

    conn.commit()
    conn.close()

    return True, code, None

def create_login_pending_entry(user: Dict[str, Any]) -> Tuple[str, str]:
    """Create or replace a pending verification entry for an existing user.

    Used by the returning user login flow to issue a fresh code while keeping
    the same user_id. This avoids duplicate user creation during verify.
    """
    conn = _get_db()
    cursor = conn.cursor()

    user_id = user['user_id']
    code = generate_verification_code()

    cursor.execute('''
        INSERT INTO pending_users (
            user_id, first_name, last_name, email, phone,
            address, city, county, state, zip,
            verification_method, code_hash, created_at, expires_at, attempts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'email', ?, ?, ?, 0)
        ON CONFLICT(user_id) DO UPDATE SET
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            email=excluded.email,
            phone=excluded.phone,
            address=excluded.address,
            city=excluded.city,
            county=excluded.county,
            state=excluded.state,
            zip=excluded.zip,
            verification_method='email',
            code_hash=excluded.code_hash,
            created_at=excluded.created_at,
            expires_at=excluded.expires_at,
            attempts=0
    ''', (
        user_id,
        user.get('first_name'),
        user.get('last_name'),
        user.get('email'),
        user.get('phone'),
        user.get('address'),
        user.get('city'),
        user.get('county'),
        user.get('state'),
        user.get('zip'),
        hash_code(code),
        datetime.now().isoformat(),
        (datetime.now() + timedelta(minutes=10)).isoformat()
    ))

    conn.commit()
    conn.close()

    return user_id, code

def log_user_interaction(user_id: str, interaction_type: str, module_name: str = None,
                        duration_seconds: int = None, success: bool = None, metadata: str = None):
    """Log user interaction for learning system"""
    conn = _get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO user_interactions (
            user_id, interaction_type, module_name, timestamp,
            duration_seconds, success, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, interaction_type, module_name,
        datetime.now().isoformat(),
        duration_seconds, success, metadata
    ))

    conn.commit()
    conn.close()

def mask_contact(contact: str, method: str) -> str:
    """Mask email or phone for display on verification page."""
    if method == 'email' and '@' in contact:
        local, domain = contact.split('@')
        return f"{local[:2]}***@{domain}"
    elif method == 'phone' and len(contact) >= 4:
        return f"***{contact[-4:]}"
    return '***'


def get_user_by_id(user_id: str):
    """Retrieve user record by user_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def save_user_situation(user_id: str, situation_data: Dict[str, Any]):
    """Save or update user situation data."""
    import json
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_situations (user_id, issue_type, urgency, notice_date, has_evidence, has_attorney, situation_details, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(user_id) DO UPDATE SET
            issue_type=excluded.issue_type,
            urgency=excluded.urgency,
            notice_date=excluded.notice_date,
            has_evidence=excluded.has_evidence,
            has_attorney=excluded.has_attorney,
            situation_details=excluded.situation_details,
            updated_at=datetime('now')
    ''', (
        user_id,
        situation_data.get('issue_type'),
        situation_data.get('urgency'),
        situation_data.get('notice_date'),
        1 if situation_data.get('has_evidence') else 0,
        1 if situation_data.get('has_attorney') else 0,
        json.dumps(situation_data.get('details', {}))
    ))
    conn.commit()
    conn.close()


def get_user_situation(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve user situation data."""
    import json
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_situations WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        'user_id': row[0],
        'issue_type': row[1],
        'urgency': row[2],
        'notice_date': row[3],
        'has_evidence': bool(row[4]),
        'has_attorney': bool(row[5]),
        'details': json.loads(row[6]) if row[6] else {},
        'created_at': row[7],
        'updated_at': row[8]
    }

# Initialize database on import
init_database()

# Initialize R2 persistence (if configured)
try:
    from r2_database_adapter import init_r2_database, sync_database_to_r2
    _r2_adapter = init_r2_database()
    
    # Helper to sync after critical operations
    def _sync_to_r2_if_enabled():
        """Sync database to R2 after writes (non-blocking)."""
        try:
            sync_database_to_r2()
        except Exception:
            pass  # Don't fail operations if R2 sync fails
            
except ImportError:
    def _sync_to_r2_if_enabled():
        pass  # R2 adapter not available



def init_remember_tokens_table():
    """Initialize remember tokens table for persistent login"""
    conn = _get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS remember_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            token_hash TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            last_used TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create index for faster lookups
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_remember_tokens_hash 
        ON remember_tokens(token_hash)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_remember_tokens_user 
        ON remember_tokens(user_id)
    ''')
    
    conn.commit()
    conn.close()
