"""
Semptify Ledger Tracking Module

Tracks money, time, and other measurable quantities with:
- Append-only transaction logs (tamper-proof)
- Balance calculations (current state)
- Statute of limitations tracking
- Time-sensitivity logic for deadlines
- Weather and environmental conditions
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
import threading

# Thread-safe ledger operations
_ledger_lock = threading.Lock()

LEDGERS_DIR = Path("ledgers")
LEDGERS_DIR.mkdir(exist_ok=True)


@dataclass
class Transaction:
    """Single transaction in a ledger (money, time, etc.)"""

    id: str
    timestamp: datetime
    ledger_type: str  # "money", "time", "service_date", "weather", "sensitivity"
    actor_id: str
    description: str
    amount: float  # For money: dollars; For time: days/hours; For service: count
    unit: str  # "USD", "days", "hours", "attempts", "conditions"
    related_doc_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    hash: str = ""  # SHA256 of all fields for tamper detection

    def calculate_hash(self) -> str:
        """Calculate SHA256 hash of transaction."""
        fields = [
            self.id,
            self.timestamp.isoformat(),
            self.ledger_type,
            self.actor_id,
            self.description,
            str(self.amount),
            self.unit,
            self.related_doc_id or "",
            json.dumps(self.context, sort_keys=True),
        ]
        hash_input = "|".join(fields)
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "ledger_type": self.ledger_type,
            "actor_id": self.actor_id,
            "description": self.description,
            "amount": self.amount,
            "unit": self.unit,
            "related_doc_id": self.related_doc_id,
            "context": self.context,
            "hash": self.hash,
        }


@dataclass
class StatuteOfLimitations:
    """Tracks when statute of limitations expires for an action."""

    id: str
    action_type: str  # "eviction", "complaint", "damage_claim", "lease_dispute"
    start_date: datetime
    duration_days: int  # How many days until statute expires
    jurisdiction: str  # State/country code
    expiration_date: Optional[datetime] = None
    is_tolled: bool = False  # Is the clock paused (tolled)?
    toll_reason: Optional[str] = None
    days_remaining: int = 0

    def __post_init__(self):
        """Calculate expiration date."""
        if not self.expiration_date:
            if self.is_tolled:
                # Clock is paused, no expiration yet
                self.expiration_date = None
            else:
                self.expiration_date = self.start_date + timedelta(days=self.duration_days)
                self.days_remaining = self.duration_days
        else:
            delta = self.expiration_date - datetime.now()
            self.days_remaining = max(0, delta.days)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "action_type": self.action_type,
            "start_date": self.start_date.isoformat(),
            "duration_days": self.duration_days,
            "jurisdiction": self.jurisdiction,
            "expiration_date": self.expiration_date.isoformat()
            if self.expiration_date
            else None,
            "is_tolled": self.is_tolled,
            "toll_reason": self.toll_reason,
            "days_remaining": self.days_remaining,
            "has_expired": datetime.now() > self.expiration_date
            if self.expiration_date
            else False,
        }


class LedgerTracker:
    """Tracks money, time, and other measurable quantities."""

    def __init__(self, ledger_type: str):
        """Initialize ledger tracker.

        Args:
            ledger_type: Type of ledger ("money", "time", "service_date", "weather", etc.)
        """
        self.ledger_type = ledger_type
        self.ledger_file = LEDGERS_DIR / f"{ledger_type}_ledger.json"
        self.transactions: List[Transaction] = []
        self.load()

    def add_transaction(
        self,
        actor_id: str,
        description: str,
        amount: float,
        unit: str,
        related_doc_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Transaction:
        """Add transaction to ledger (append-only).

        Args:
            actor_id: Who made the transaction
            description: What happened
            amount: Quantity (dollars, days, hours, etc.)
            unit: Unit of measurement
            related_doc_id: Linked document
            context: Additional data (property, jurisdiction, etc.)

        Returns: Created transaction
        """
        with _ledger_lock:
            import uuid

            trans = Transaction(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                ledger_type=self.ledger_type,
                actor_id=actor_id,
                description=description,
                amount=amount,
                unit=unit,
                related_doc_id=related_doc_id,
                context=context or {},
            )
            trans.hash = trans.calculate_hash()
            self.transactions.append(trans)
            self._persist()
            return trans

    def get_balance(self, actor_id: Optional[str] = None) -> float:
        """Get current balance for actor or total.

        For money ledger: total balance in dollars
        For time ledger: total days/hours tracked
        """
        with _ledger_lock:
            transactions = self.transactions
            if actor_id:
                transactions = [t for t in transactions if t.actor_id == actor_id]

            total = sum(t.amount for t in transactions)
            return total

    def get_transactions(
        self,
        actor_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        description_filter: Optional[str] = None,
    ) -> List[Transaction]:
        """Query transactions with optional filters."""
        with _ledger_lock:
            results = self.transactions

            if actor_id:
                results = [t for t in results if t.actor_id == actor_id]

            if start_date:
                results = [t for t in results if t.timestamp >= start_date]

            if end_date:
                results = [t for t in results if t.timestamp <= end_date]

            if description_filter:
                results = [
                    t
                    for t in results
                    if description_filter.lower() in t.description.lower()
                ]

            return results

    def get_summary(
        self, actor_id: Optional[str] = None, days: int = 90
    ) -> Dict[str, Any]:
        """Get summary of ledger activity for time period."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = self.get_transactions(actor_id=actor_id, start_date=cutoff)

        return {
            "ledger_type": self.ledger_type,
            "actor_id": actor_id,
            "period_days": days,
            "transaction_count": len(recent),
            "total_amount": sum(t.amount for t in recent),
            "unit": recent[0].unit if recent else None,
            "earliest": recent[0].timestamp.isoformat() if recent else None,
            "latest": recent[-1].timestamp.isoformat() if recent else None,
            "transactions": [t.to_dict() for t in recent],
        }

    def load(self):
        """Load ledger from persistent storage."""
        with _ledger_lock:
            if self.ledger_file.exists():
                try:
                    data = json.loads(self.ledger_file.read_text())
                    self.transactions = [
                        Transaction(
                            id=t["id"],
                            timestamp=datetime.fromisoformat(t["timestamp"]),
                            ledger_type=t["ledger_type"],
                            actor_id=t["actor_id"],
                            description=t["description"],
                            amount=t["amount"],
                            unit=t["unit"],
                            related_doc_id=t.get("related_doc_id"),
                            context=t.get("context", {}),
                            hash=t.get("hash", ""),
                        )
                        for t in data
                    ]
                except Exception as e:
                    print(f"Error loading {self.ledger_type} ledger: {e}")
                    self.transactions = []
            else:
                self.transactions = []

    def _persist(self):
        """Save ledger to persistent storage."""
        with _ledger_lock:
            data = [t.to_dict() for t in self.transactions]
            self.ledger_file.write_text(json.dumps(data, indent=2))


class StatuteOfLimitationsTracker:
    """Tracks statute of limitations expiration dates."""

    def __init__(self):
        from ledger_config import get_ledger_config
        
        self.file = LEDGERS_DIR / "statute_of_limitations.json"
        self.statutes: Dict[str, StatuteOfLimitations] = {}
        self.config = get_ledger_config()
        self.load()

    def create_statute(
        self,
        action_type: str,
        start_date: datetime,
        jurisdiction: str,
        doc_id: Optional[str] = None,
    ) -> StatuteOfLimitations:
        """Create a statute of limitations tracker.

        Args:
            action_type: Type of action (eviction_notice, complaint, etc.)
            start_date: When the clock started
            jurisdiction: State/country code
            doc_id: Related document ID

        Returns: StatuteOfLimitations object
        """
        with _ledger_lock:
            import uuid

            # Get duration from config (allows admin to adjust)
            duration = self.config.get_statute_duration(action_type)
            statute = StatuteOfLimitations(
                id=str(uuid.uuid4()),
                action_type=action_type,
                start_date=start_date,
                duration_days=duration,
                jurisdiction=jurisdiction,
            )
            self.statutes[statute.id] = statute
            self._persist()
            return statute

    def get_active_statutes(self) -> List[StatuteOfLimitations]:
        """Get all non-expired statutes."""
        with _ledger_lock:
            return [
                s
                for s in self.statutes.values()
                if s.expiration_date and datetime.now() <= s.expiration_date
            ]

    def get_expiring_soon(self, days: int = 30) -> List[StatuteOfLimitations]:
        """Get statutes expiring within N days."""
        with _ledger_lock:
            cutoff = datetime.now() + timedelta(days=days)
            return [
                s
                for s in self.statutes.values()
                if s.expiration_date and datetime.now() <= s.expiration_date <= cutoff
            ]

    def toll_statute(self, statute_id: str, reason: str):
        """Pause the clock on a statute (tolling)."""
        with _ledger_lock:
            if statute_id in self.statutes:
                self.statutes[statute_id].is_tolled = True
                self.statutes[statute_id].toll_reason = reason
                self._persist()

    def load(self):
        """Load from persistent storage."""
        with _ledger_lock:
            if self.file.exists():
                try:
                    data = json.loads(self.file.read_text())
                    for s in data:
                        self.statutes[s["id"]] = StatuteOfLimitations(
                            id=s["id"],
                            action_type=s["action_type"],
                            start_date=datetime.fromisoformat(s["start_date"]),
                            duration_days=s["duration_days"],
                            jurisdiction=s["jurisdiction"],
                            expiration_date=datetime.fromisoformat(s["expiration_date"])
                            if s.get("expiration_date")
                            else None,
                            is_tolled=s.get("is_tolled", False),
                            toll_reason=s.get("toll_reason"),
                        )
                except Exception as e:
                    print(f"Error loading statute tracker: {e}")

    def _persist(self):
        """Save to persistent storage."""
        with _ledger_lock:
            data = [s.to_dict() for s in self.statutes.values()]
            self.file.write_text(json.dumps(data, indent=2))


# Global instances
_money_ledger: Optional[LedgerTracker] = None
_time_ledger: Optional[LedgerTracker] = None
_service_date_ledger: Optional[LedgerTracker] = None
_statute_tracker: Optional[StatuteOfLimitationsTracker] = None


def get_money_ledger() -> LedgerTracker:
    """Get or create money ledger."""
    global _money_ledger
    if _money_ledger is None:
        _money_ledger = LedgerTracker("money")
    return _money_ledger


def get_time_ledger() -> LedgerTracker:
    """Get or create time ledger."""
    global _time_ledger
    if _time_ledger is None:
        _time_ledger = LedgerTracker("time")
    return _time_ledger


def get_service_date_ledger() -> LedgerTracker:
    """Get or create service date ledger."""
    global _service_date_ledger
    if _service_date_ledger is None:
        _service_date_ledger = LedgerTracker("service_date")
    return _service_date_ledger


def get_statute_tracker() -> StatuteOfLimitationsTracker:
    """Get or create statute tracker."""
    global _statute_tracker
    if _statute_tracker is None:
        _statute_tracker = StatuteOfLimitationsTracker()
    return _statute_tracker
