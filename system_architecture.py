"""
Unified Semptify System Architecture
Integrates all GUIs with comprehensive attribute system
"""

# ============================================================================
# SYSTEM-WIDE ENUMS AND CONSTANTS
# ============================================================================

class UserRole:
    """User roles defining access levels"""
    TENANT = "tenant"              # Individual tenant (basic access)
    ADVOCATE = "advocate"          # Case worker/helper (multi-client)
    ATTORNEY = "attorney"          # Legal professional (full access)
    ADMIN = "admin"                # System administrator
    LANDLORD = "landlord"          # Landlord (limited, mediation access)

class CaseStatus:
    """Current status of tenant case"""
    INTAKE = "intake"              # Initial information gathering
    ACTIVE = "active"              # Ongoing case management
    PRE_COURT = "pre_court"        # Preparing for court
    IN_COURT = "in_court"          # Active litigation
    MEDIATION = "mediation"        # Settlement negotiations
    RESOLVED = "resolved"          # Case closed successfully
    CLOSED = "closed"              # Case closed (any reason)

class DocumentType:
    """Categories of documents"""
    LEASE = "lease"                # Rental agreement
    NOTICE = "notice"              # Eviction/violation notice
    COMMUNICATION = "communication" # Emails, texts, letters
    PAYMENT_PROOF = "payment_proof" # Rent receipts, bank statements
    PHOTO_EVIDENCE = "photo_evidence" # Photos of conditions
    VIDEO_EVIDENCE = "video_evidence" # Video documentation
    WITNESS_STATEMENT = "witness_statement" # Sworn statements
    COURT_FILING = "court_filing"   # Court documents
    INSPECTION_REPORT = "inspection_report" # Official inspections
    MEDICAL_RECORD = "medical_record" # Health impacts
    CORRESPONDENCE = "correspondence" # General communications

class EventCategory:
    """Timeline event types"""
    RENT_DUE = "rent_due"
    RENT_PAID = "rent_paid"
    NOTICE_RECEIVED = "notice_received"
    COMPLAINT_FILED = "complaint_filed"
    INSPECTION = "inspection"
    COURT_HEARING = "court_hearing"
    DEADLINE = "deadline"
    COMMUNICATION = "communication"
    REPAIR_REQUEST = "repair_request"
    INCIDENT = "incident"

class PriorityLevel:
    """Urgency/importance ratings"""
    CRITICAL = "critical"          # Immediate action required (< 24hrs)
    URGENT = "urgent"              # Very important (< 3 days)
    HIGH = "high"                  # Important (< 7 days)
    NORMAL = "normal"              # Standard priority
    LOW = "low"                    # When time permits

class CompletionStatus:
    """Progress tracking"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    BLOCKED = "blocked"            # Cannot proceed

class EvidenceQuality:
    """Strength of evidence"""
    STRONG = "strong"              # Clear, documented, dated
    MODERATE = "moderate"          # Documented but incomplete
    WEAK = "weak"                  # Anecdotal, no backup
    INSUFFICIENT = "insufficient"   # Not usable

class LegalStage:
    """Where in the legal process"""
    PRE_NOTICE = "pre_notice"      # Before eviction notice
    POST_NOTICE = "post_notice"    # After notice, before court
    PRE_TRIAL = "pre_trial"        # Court filed, before hearing
    TRIAL = "trial"                # During hearing/trial
    POST_TRIAL = "post_trial"      # After judgment
    APPEAL = "appeal"              # Appeals process

# ============================================================================
# UNIFIED USER PROFILE
# ============================================================================

class UserProfile:
    """Complete user profile spanning all GUIs"""
    
    def __init__(self, user_id, role=UserRole.TENANT):
        self.user_id = user_id
        self.role = role
        
        # Identity
        self.name = None
        self.email = None
        self.phone = None
        self.preferred_language = "en"
        
        # Address
        self.rental_address = None
        self.mailing_address = None
        self.jurisdiction = None  # City/county for court rules
        
        # Case info
        self.case_status = CaseStatus.INTAKE
        self.legal_stage = LegalStage.PRE_NOTICE
        self.case_opened = None
        self.case_priority = PriorityLevel.NORMAL
        
        # Landlord info
        self.landlord_name = None
        self.landlord_contact = None
        self.property_manager = None
        
        # Financial
        self.monthly_rent = 0
        self.security_deposit = 0
        self.lease_start = None
        self.lease_end = None
        
        # Progress tracking
        self.completion_percent = 0
        self.documents_collected = 0
        self.timeline_events = 0
        self.legal_checklist_done = []
        
        # Learning profile
        self.learning_level = "beginner"  # beginner, intermediate, advanced
        self.topics_mastered = []
        self.help_views = []
        
        # Preferences
        self.preferred_gui = "main_dashboard"
        self.notifications_enabled = True
        self.accessibility_needs = []

# ============================================================================
# CASE ATTRIBUTES
# ============================================================================

class CaseAttributes:
    """Core attributes for a tenant justice case"""
    
    # Issue categories (can be multiple)
    ISSUES = [
        "eviction",
        "non_payment_claim",
        "repairs_needed",
        "habitability",
        "harassment",
        "discrimination",
        "security_deposit",
        "lease_violation",
        "retaliation",
        "illegal_entry",
        "utility_shutoff",
        "lockout"
    ]
    
    # Required documents by issue type
    REQUIRED_DOCS = {
        "eviction": [DocumentType.NOTICE, DocumentType.LEASE, DocumentType.PAYMENT_PROOF],
        "repairs_needed": [DocumentType.PHOTO_EVIDENCE, DocumentType.COMMUNICATION, DocumentType.INSPECTION_REPORT],
        "security_deposit": [DocumentType.LEASE, DocumentType.PAYMENT_PROOF, DocumentType.PHOTO_EVIDENCE],
        "harassment": [DocumentType.COMMUNICATION, DocumentType.WITNESS_STATEMENT, EventCategory.INCIDENT],
    }
    
    # Court deadlines by jurisdiction (days)
    COURT_DEADLINES = {
        "answer_deadline": 7,      # Days to answer eviction
        "discovery_deadline": 30,   # Days for evidence exchange
        "trial_notice": 14,        # Days before trial notice
    }

# ============================================================================
# SYSTEM INTEGRATION
# ============================================================================

class SystemState:
    """Unified state management across all GUIs"""
    
    def __init__(self):
        self.active_users = {}     # user_id -> UserProfile
        self.active_cases = {}     # case_id -> CaseAttributes
        self.notifications = []    # Pending notifications
        self.task_queue = []       # Background tasks
        
    def get_user_context(self, user_id):
        """Get all context for a user across the system"""
        return {
            "profile": self.active_users.get(user_id),
            "documents": [],  # From vault
            "timeline": [],   # From calendar
            "ledger": [],     # From financial tracking
            "learning": {},   # From learning engine
            "tasks": [],      # Pending action items
        }
    
    def get_gui_for_task(self, task_type):
        """Route tasks to appropriate GUI"""
        routing = {
            "document_upload": "/vault",
            "timeline_entry": "/timeline/assistant",
            "learn_rights": "/app",  # Modern GUI with learning
            "multi_client": "/brad", # Advocate interface
            "court_packet": "/complaint_filing",
            "evidence": "/witness_statement",
        }
        return routing.get(task_type, "/")

# ============================================================================
# NAVIGATION SYSTEM
# ============================================================================

class NavigationMenu:
    """Unified navigation across all interfaces"""
    
    @staticmethod
    def get_menu_for_role(role):
        """Get appropriate menu items by role"""
        base_menu = [
            {"label": "Home", "url": "/", "icon": "home"},
            {"label": "My Documents", "url": "/vault", "icon": "folder"},
            {"label": "Timeline", "url": "/timeline/assistant", "icon": "calendar"},
            {"label": "Learn Your Rights", "url": "/app", "icon": "book"},
        ]
        
        if role == UserRole.ADVOCATE or role == UserRole.ATTORNEY:
            base_menu.extend([
                {"label": "Client Dashboard", "url": "/brad", "icon": "users"},
                {"label": "Case Management", "url": "/brad/clients", "icon": "briefcase"},
            ])
        
        if role == UserRole.ADMIN:
            base_menu.extend([
                {"label": "Admin", "url": "/admin", "icon": "settings"},
                {"label": "Metrics", "url": "/metrics", "icon": "chart"},
            ])
        
        return base_menu

# ============================================================================
# NOTIFICATION SYSTEM
# ============================================================================

class NotificationPriority:
    CRITICAL = "critical"  # Red, immediate
    HIGH = "high"          # Orange, urgent
    NORMAL = "normal"      # Blue, informational
    LOW = "low"            # Gray, FYI

class Notification:
    """Unified notification across system"""
    
    def __init__(self, user_id, title, message, priority=NotificationPriority.NORMAL):
        self.user_id = user_id
        self.title = title
        self.message = message
        self.priority = priority
        self.created_at = None
        self.read = False
        self.action_url = None
        self.action_label = None

# Export all classes
__all__ = [
    'UserRole', 'CaseStatus', 'DocumentType', 'EventCategory',
    'PriorityLevel', 'CompletionStatus', 'EvidenceQuality', 'LegalStage',
    'UserProfile', 'CaseAttributes', 'SystemState', 'NavigationMenu',
    'NotificationPriority', 'Notification'
]

