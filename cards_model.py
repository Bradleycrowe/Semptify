"""
Cards model for organizing user-facing actions into groups with metadata.
Backed by SQLite using the same DB as user_database.
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional

from user_database import DB_PATH, init_database  # ensure base DB exists


def _db_connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_cards_tables():
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            icon TEXT,
            group_name TEXT NOT NULL,
            description TEXT,
            "what" TEXT,
            "who" TEXT,
            "why" TEXT,
            "when" TEXT,
            route TEXT,
            priority INTEGER DEFAULT 100,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


def seed_default_cards():
    """Seed a minimal set of default cards if none exist."""
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cards")
    count = cur.fetchone()[0]
    if count and count > 0:
        conn.close()
        return

    defaults: List[Dict[str, Any]] = [
        # Capture
        {
            "slug": "capture-photo-video", "title": "Record Photo/Video", "icon": "📷",
            "group_name": "Capture", "description": "Capture visual evidence on the spot.",
            "what": "Photo or video of issue/evidence", "who": "You or witness",
            "why": "Document conditions with timestamps", "when": "Immediately when observed",
            "route": "/vault" , "priority": 10
        },
        {"slug": "log-communication", "title": "Log Call/Message", "icon": "📞",
         "group_name": "Capture", "description": "Record calls, texts, emails.",
         "what": "Communication details and attachments", "who": "You and other party",
         "why": "Build a record of interactions", "when": "After each contact",
         "route": "/calendar-timeline", "priority": 20},
        {"slug": "upload-document", "title": "Upload Document", "icon": "📄",
         "group_name": "Capture", "description": "Upload letters, notices, receipts.",
         "what": "PDFs, images, office docs", "who": "You, landlord, court",
         "why": "Centralize all paperwork", "when": "When received or created",
         "route": "/vault", "priority": 30},

        # Organize
        {"slug": "evidence-gallery", "title": "Evidence Gallery", "icon": "🗂️",
         "group_name": "Organize", "description": "Browse and tag evidence.",
         "what": "All captured items", "who": "You",
         "why": "Find and group quickly", "when": "As needed",
         "route": "/vault", "priority": 40},
        {"slug": "tag-group", "title": "Tag & Group", "icon": "🏷️",
         "group_name": "Organize", "description": "Tag items by issue or case.",
         "what": "Tags like 'repairs', 'rent'", "who": "You",
         "why": "Sort for fast export", "when": "After uploads",
         "route": "/vault", "priority": 50},

        # Timeline
        {"slug": "calendar-deadlines", "title": "Calendar & Deadlines", "icon": "📅",
         "group_name": "Timeline", "description": "View dates and add events.",
         "what": "Events, notices, hearings", "who": "You",
         "why": "Never miss a deadline", "when": "Daily check-in",
         "route": "/calendar-timeline", "priority": 60},
        {"slug": "rent-ledger", "title": "Rent Ledger", "icon": "🧾",
         "group_name": "Timeline", "description": "Track payments and balances.",
         "what": "Payments, amounts, proof", "who": "You",
         "why": "Show consistent record", "when": "When paying",
         "route": "/ledger", "priority": 70},

        # Notify
        {"slug": "demand-letter", "title": "Send Demand Letter", "icon": "✉️",
         "group_name": "Notify", "description": "Create and send a notice.",
         "what": "Formal request text", "who": "You to landlord",
         "why": "Start the paper trail", "when": "After documenting issue",
         "route": "/demand-letter", "priority": 80},
        {"slug": "file-complaint", "title": "File Complaint", "icon": "⚖️",
         "group_name": "Notify", "description": "Prepare filing packet.",
         "what": "Complaint + evidence", "who": "You to agency/court",
         "why": "Escalate unresolved issues", "when": "After notice window",
         "route": "/complaint-filing", "priority": 90},

        # Export
        {"slug": "generate-packet", "title": "Generate Packet", "icon": "📦",
         "group_name": "Export", "description": "Export a clean evidence packet.",
         "what": "PDF bundle", "who": "You, advocate, court",
         "why": "Share or file quickly", "when": "Before submission",
         "route": "/packet/export", "priority": 100},

        # Learn
        {"slug": "know-rights", "title": "Know Your Rights", "icon": "📚",
         "group_name": "Learn", "description": "Read tailored guidance.",
         "what": "Plain-language guide", "who": "You",
         "why": "Make informed choices", "when": "Anytime",
         "route": "/rights", "priority": 110},
    ]

    cur.executemany(
        """
        INSERT OR IGNORE INTO cards
        (slug, title, icon, group_name, description, "what", "who", "why", "when", route, priority, active)
        VALUES (:slug, :title, :icon, :group_name, :description, :what, :who, :why, :when, :route, :priority, 1)
        """,
        defaults,
    )
    conn.commit()
    conn.close()


def seed_expanded_cards():
    """Ensure additional cards exist for privacy, research, laws, and courtroom tools."""
    conn = _db_connect()
    cur = conn.cursor()

    expanded: List[Dict[str, Any]] = [
        # Security & Privacy
        {"slug": "privacy-security", "title": "Privacy & Security", "icon": "🔒",
         "group_name": "Security", "description": "How we keep your data private and encrypted.",
         "what": "Anonymous IDs, token encryption, secure vault", "who": "You",
         "why": "Your info stays yours — even we can't access it", "when": "Anytime",
         "route": "/privacy", "priority": 5},

        # Law Library
        {"slug": "law-library", "title": "Law Library", "icon": "📚",
         "group_name": "Law Library", "description": "Local, state, and federal housing laws.",
         "what": "Tenant rights, ordinances, procedures", "who": "You",
         "why": "Know the rules. Make strong decisions.", "when": "Before acting",
         "route": "/laws", "priority": 10},
        {"slug": "jurisdiction-finder", "title": "Find Your Jurisdiction", "icon": "🧭",
         "group_name": "Law Library", "description": "Identify the right court and agency.",
         "what": "Court, agency, filing location", "who": "You",
         "why": "Use the correct forms and deadlines", "when": "Before filing",
         "route": "/jurisdiction", "priority": 20},

        # Research
        {"slug": "landlord-research", "title": "Research Landlord", "icon": "🔎",
         "group_name": "Research", "description": "Reputation, prior complaints, and records.",
         "what": "Public records and reputation", "who": "You",
         "why": "Prepare for patterns and defenses", "when": "Before escalation",
         "route": "/landlord-research", "priority": 10},
        {"slug": "research-assistant", "title": "Research Assistant", "icon": "🤖",
         "group_name": "Research", "description": "AI helper to find facts for your case.",
         "what": "Guided research by issue", "who": "You",
         "why": "Answers fast with sources", "when": "Anytime",
         "route": "/research", "priority": 20},

        # Courtroom
        {"slug": "courtroom-procedures", "title": "Courtroom Procedures", "icon": "🏛️",
         "group_name": "Courtroom", "description": "What to expect and how to prepare.",
         "what": "Procedure, etiquette, exhibits", "who": "You",
         "why": "Be ready and confident", "when": "Before court",
         "route": "/courtroom", "priority": 10},
        {"slug": "court-packet-wizard", "title": "Court Packet Wizard", "icon": "📁",
         "group_name": "Courtroom", "description": "Assemble evidence into court-ready packets.",
         "what": "Organized evidence with cover page", "who": "You",
         "why": "Present your case professionally", "when": "Before filing or hearing",
         "route": "/court-packet", "priority": 15},
        {"slug": "attorney-connect", "title": "Attorney Connect", "icon": "👩‍⚖️",
         "group_name": "Courtroom", "description": "Share your packet with an attorney.",
         "what": "Secure share to counsel", "who": "You",
         "why": "Get legal help quickly", "when": "When escalating",
         "route": "/attorney", "priority": 20},

        # Checklist & Inbox
        {"slug": "move-in-checklist", "title": "Move-In Checklist", "icon": "✅",
         "group_name": "Checklist", "description": "Guided checklist with photos and notes.",
         "what": "Rooms, fixtures, conditions", "who": "You",
         "why": "Protect your deposit from day one", "when": "Move-in day",
         "route": "/move-in", "priority": 5},
        {"slug": "smart-inbox", "title": "Smart Inbox", "icon": "📥",
         "group_name": "Checklist", "description": "Auto-capture emails, texts, and voicemails.",
         "what": "Message import & tagging", "who": "You",
         "why": "Never lose important messages", "when": "Daily",
         "route": "/smart-inbox", "priority": 15},

        # Capture helpers
        {"slug": "voice-capture", "title": "Voice Capture", "icon": "🎤",
         "group_name": "Capture", "description": "Record notes and calls to your vault.",
         "what": "Audio notes & call logs", "who": "You",
         "why": "Document conversations easily", "when": "After calls",
         "route": "/voice-capture", "priority": 25},
        {"slug": "ocr-doc-manager", "title": "OCR Document Manager", "icon": "🧠",
         "group_name": "Organize", "description": "Scan, extract text, and auto-tag documents.",
         "what": "OCR + AI tagging", "who": "You",
         "why": "Find documents fast", "when": "After uploads",
         "route": "/ocr", "priority": 55},
    ]

    cur.executemany(
        """
        INSERT OR IGNORE INTO cards
        (slug, title, icon, group_name, description, "what", "who", "why", "when", route, priority, active)
        VALUES (:slug, :title, :icon, :group_name, :description, :what, :who, :why, :when, :route, :priority, 1)
        """,
        expanded,
    )
    conn.commit()
    conn.close()


def get_cards(group: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = _db_connect()
    cur = conn.cursor()
    if group:
        cur.execute(
            "SELECT * FROM cards WHERE active=1 AND group_name=? ORDER BY priority, title",
            (group,),
        )
    else:
        cur.execute("SELECT * FROM cards WHERE active=1 ORDER BY group_name, priority, title")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_cards_grouped() -> Dict[str, List[Dict[str, Any]]]:
    data = get_cards()
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in data:
        grouped.setdefault(row["group_name"], []).append(row)
    return grouped


# Ensure base DB and cards table exist on import, then seed defaults
try:
    init_database()
    init_cards_tables()
    seed_default_cards()
except Exception:
    # Avoid import-time hard failures; routes can trigger initialization later if needed
    pass
