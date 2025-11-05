"""
Ledger Tracking Module

Provides double-entry ledger tracking for:
- Money (rent, fees, payments)
- Time (days, attempts, hours)
- Service dates (process service attempts/completions)
- Statute of limitations tracking

All ledger entries are tied to calendar events and document IDs for evidence chain.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


# =====================
# DATA CLASSES
# =====================


@dataclass
class LedgerTransaction:
    """Represents a single ledger transaction."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    actor_id: str = ""  # Tenant, landlord, process server, etc.
    description: str = ""
    amount: float = 0.0
    unit: str = "USD"  # USD, days, attempts, hours, etc.
    timestamp: datetime = field(default_factory=datetime.now)
    related_doc_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class Statute:
    """Statute of limitations tracker."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = ""  # eviction_notice, lawsuit_filing, etc.
    start_date: datetime = field(default_factory=datetime.now)
    deadline: datetime = field(default_factory=datetime.now)
    jurisdiction: str = "US"
    doc_id: Optional[str] = None
    tolled: bool = False
    tolled_date: Optional[datetime] = None
    tolled_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["start_date"] = self.start_date.isoformat()
        data["deadline"] = self.deadline.isoformat()
        if self.tolled_date:
            data["tolled_date"] = self.tolled_date.isoformat()
        return data

    @property
    def days_remaining(self) -> int:
        """Days until deadline (or negative if expired)."""
        if self.tolled:
            # Clock is paused
            return (self.deadline - self.tolled_date).days if self.tolled_date else 0
        return (self.deadline - datetime.now()).days

    @property
    def is_expired(self) -> bool:
        """Check if statute has expired."""
        if self.tolled:
            return False
        return datetime.now() > self.deadline


# =====================
# LEDGER CLASSES
# =====================


class BaseLedger:
    """Base class for all ledger types."""

    def __init__(self, ledger_type: str):
        self.ledger_type = ledger_type
        self.transactions: List[LedgerTransaction] = []

    def add_transaction(
        self,
        actor_id: str,
        description: str,
        amount: float,
        unit: str = "USD",
        related_doc_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> LedgerTransaction:
        """Add a transaction to the ledger."""
        trans = LedgerTransaction(
            actor_id=actor_id,
            description=description,
            amount=amount,
            unit=unit,
            related_doc_id=related_doc_id,
            context=context or {},
        )
        self.transactions.append(trans)
        return trans

    def get_balance(self, actor_id: str) -> float:
        """Get total balance for an actor."""
        return sum(t.amount for t in self.transactions if t.actor_id == actor_id)

    def get_transactions(
        self,
        actor_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[LedgerTransaction]:
        """Get transactions for an actor within date range."""
        filtered = [t for t in self.transactions if t.actor_id == actor_id]

        if start_date:
            filtered = [t for t in filtered if t.timestamp >= start_date]
        if end_date:
            filtered = [t for t in filtered if t.timestamp <= end_date]

        return filtered

    def get_summary(self, actor_id: str, days: int = 90) -> Dict[str, Any]:
        """Get summary statistics for an actor."""
        cutoff = datetime.now() - timedelta(days=days)
        transactions = self.get_transactions(actor_id, start_date=cutoff)

        return {
            "actor_id": actor_id,
            "ledger_type": self.ledger_type,
            "period_days": days,
            "transaction_count": len(transactions),
            "total": sum(t.amount for t in transactions),
            "balance": self.get_balance(actor_id),
            "first_transaction": transactions[0].to_dict() if transactions else None,
            "last_transaction": transactions[-1].to_dict() if transactions else None,
        }


class MoneyLedger(BaseLedger):
    """Tracks money transactions (rent, fees, payments)."""

    def __init__(self):
        super().__init__("money")


class TimeLedger(BaseLedger):
    """Tracks time-based transactions (days, attempts, hours)."""

    def __init__(self):
        super().__init__("time")


class ServiceDateLedger(BaseLedger):
    """Tracks service attempts and completions."""

    def __init__(self):
        super().__init__("service_date")


class StatuteTracker:
    """Tracks statutes of limitations."""

    # Default statute periods by action type (in days)
    DEFAULT_PERIODS = {
        "eviction_notice": 60,
        "unlawful_detainer": 5,
        "answer_to_complaint": 30,
        "appeal_filing": 60,
        "discovery_motion": 45,
        "default_judgment": 10,
        "rent_demand": 3,
        "cure_or_quit": 30,
    }

    def __init__(self):
        self.statutes: Dict[str, Statute] = {}

    def create_statute(
        self,
        action_type: str,
        start_date: datetime,
        jurisdiction: str = "US",
        doc_id: Optional[str] = None,
        custom_days: Optional[int] = None,
    ) -> Statute:
        """Create a new statute of limitations tracker."""
        # Calculate deadline
        days = custom_days or self.DEFAULT_PERIODS.get(action_type, 30)
        deadline = start_date + timedelta(days=days)

        statute = Statute(
            action_type=action_type,
            start_date=start_date,
            deadline=deadline,
            jurisdiction=jurisdiction,
            doc_id=doc_id,
        )

        self.statutes[statute.id] = statute
        return statute

    def get_active_statutes(self) -> List[Statute]:
        """Get all non-expired statutes."""
        return [s for s in self.statutes.values() if not s.is_expired]

    def get_expiring_soon(self, days: int = 30) -> List[Statute]:
        """Get statutes expiring within N days."""
        cutoff = datetime.now() + timedelta(days=days)
        return [
            s for s in self.statutes.values()
            if not s.is_expired and s.deadline <= cutoff
        ]

    def toll_statute(self, statute_id: str, reason: str = "") -> None:
        """Pause the clock on a statute (tolling)."""
        if statute_id in self.statutes:
            statute = self.statutes[statute_id]
            statute.tolled = True
            statute.tolled_date = datetime.now()
            statute.tolled_reason = reason

    def resume_statute(self, statute_id: str) -> None:
        """Resume the clock after tolling."""
        if statute_id in self.statutes:
            statute = self.statutes[statute_id]
            if statute.tolled and statute.tolled_date:
                # Calculate how much time was left when tolled
                time_left = statute.deadline - statute.tolled_date
                # Set new deadline from now
                statute.deadline = datetime.now() + time_left
                statute.tolled = False
                statute.tolled_date = None


# =====================
# SINGLETON INSTANCES
# =====================

_money_ledger: Optional[MoneyLedger] = None
_time_ledger: Optional[TimeLedger] = None
_service_date_ledger: Optional[ServiceDateLedger] = None
_statute_tracker: Optional[StatuteTracker] = None


def get_money_ledger() -> MoneyLedger:
    """Get the singleton money ledger instance."""
    global _money_ledger
    if _money_ledger is None:
        _money_ledger = MoneyLedger()
    return _money_ledger


def get_time_ledger() -> TimeLedger:
    """Get the singleton time ledger instance."""
    global _time_ledger
    if _time_ledger is None:
        _time_ledger = TimeLedger()
    return _time_ledger


def get_service_date_ledger() -> ServiceDateLedger:
    """Get the singleton service date ledger instance."""
    global _service_date_ledger
    if _service_date_ledger is None:
        _service_date_ledger = ServiceDateLedger()
    return _service_date_ledger


def get_statute_tracker() -> StatuteTracker:
    """Get the singleton statute tracker instance."""
    global _statute_tracker
    if _statute_tracker is None:
        _statute_tracker = StatuteTracker()
    return _statute_tracker


# =====================
# UTILITY FUNCTIONS
# =====================


def reset_all_ledgers() -> None:
    """Reset all ledgers (useful for testing)."""
    global _money_ledger, _time_ledger, _service_date_ledger, _statute_tracker
    _money_ledger = None
    _time_ledger = None
    _service_date_ledger = None
    _statute_tracker = None
