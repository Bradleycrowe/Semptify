"""
Ledger Tracking Module

Provides ledger management for money, time, and service dates.
Tracks statutes of limitations.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import uuid
import json
import os


@dataclass
class Transaction:
    """A ledger transaction entry."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    actor_id: str = ""
    description: str = ""
    amount: float = 0.0
    unit: str = "USD"
    timestamp: datetime = field(default_factory=datetime.now)
    related_doc_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "description": self.description,
            "amount": self.amount,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "related_doc_id": self.related_doc_id,
            "context": self.context
        }


class Ledger:
    """Generic ledger for tracking transactions."""
    
    def __init__(self, name: str):
        self.name = name
        self.transactions: List[Transaction] = []
    
    def add_transaction(
        self,
        actor_id: str,
        description: str,
        amount: float,
        unit: str = "USD",
        related_doc_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Transaction:
        """Add a transaction to the ledger."""
        trans = Transaction(
            actor_id=actor_id,
            description=description,
            amount=amount,
            unit=unit,
            related_doc_id=related_doc_id,
            context=context or {}
        )
        self.transactions.append(trans)
        return trans
    
    def get_balance(self, actor_id: str) -> float:
        """Get total balance for an actor."""
        return sum(
            t.amount for t in self.transactions if t.actor_id == actor_id
        )
    
    def get_transactions(
        self,
        actor_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Transaction]:
        """Get transactions for an actor within a date range."""
        results = [t for t in self.transactions if t.actor_id == actor_id]
        
        if start_date:
            results = [t for t in results if t.timestamp >= start_date]
        
        if end_date:
            results = [t for t in results if t.timestamp <= end_date]
        
        return results
    
    def get_summary(self, actor_id: str, days: int = 90) -> dict:
        """Get summary of transactions for an actor."""
        cutoff = datetime.now() - timedelta(days=days)
        transactions = self.get_transactions(actor_id, start_date=cutoff)
        
        return {
            "actor_id": actor_id,
            "period_days": days,
            "transaction_count": len(transactions),
            "total": sum(t.amount for t in transactions),
            "unit": self.transactions[0].unit if self.transactions else "USD"
        }


@dataclass
class Statute:
    """Statute of limitations tracker."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str = ""
    start_date: datetime = field(default_factory=datetime.now)
    jurisdiction: str = "US"
    doc_id: Optional[str] = None
    expiration_date: Optional[datetime] = None
    is_tolled: bool = False
    toll_reason: str = ""
    
    def to_dict(self) -> dict:
        """Convert statute to dictionary."""
        return {
            "id": self.id,
            "action_type": self.action_type,
            "start_date": self.start_date.isoformat(),
            "jurisdiction": self.jurisdiction,
            "doc_id": self.doc_id,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "is_tolled": self.is_tolled,
            "toll_reason": self.toll_reason
        }


class StatuteTracker:
    """Tracks statutes of limitations."""
    
    def __init__(self):
        self.statutes: Dict[str, Statute] = {}
        # Default statute periods by action type (in years)
        self.default_periods = {
            "eviction_notice": 3,
            "debt_collection": 6,
            "personal_injury": 2,
            "contract_breach": 4,
            "property_damage": 3,
        }
    
    def create_statute(
        self,
        action_type: str,
        start_date: datetime,
        jurisdiction: str = "US",
        doc_id: Optional[str] = None
    ) -> Statute:
        """Create a new statute tracker."""
        years = self.default_periods.get(action_type, 3)
        expiration = start_date + timedelta(days=365 * years)
        
        statute = Statute(
            action_type=action_type,
            start_date=start_date,
            jurisdiction=jurisdiction,
            doc_id=doc_id,
            expiration_date=expiration
        )
        
        self.statutes[statute.id] = statute
        return statute
    
    def get_active_statutes(self) -> List[Statute]:
        """Get all non-expired statutes."""
        now = datetime.now()
        return [
            s for s in self.statutes.values()
            if s.expiration_date and s.expiration_date > now
        ]
    
    def get_expiring_soon(self, days: int = 30) -> List[Statute]:
        """Get statutes expiring within N days."""
        now = datetime.now()
        threshold = now + timedelta(days=days)
        
        return [
            s for s in self.statutes.values()
            if s.expiration_date and now < s.expiration_date <= threshold
        ]
    
    def toll_statute(self, statute_id: str, reason: str = "") -> bool:
        """Pause the clock on a statute (tolling)."""
        if statute_id in self.statutes:
            self.statutes[statute_id].is_tolled = True
            self.statutes[statute_id].toll_reason = reason
            return True
        return False


# Singleton instances
_money_ledger: Optional[Ledger] = None
_time_ledger: Optional[Ledger] = None
_service_date_ledger: Optional[Ledger] = None
_statute_tracker: Optional[StatuteTracker] = None


def get_money_ledger() -> Ledger:
    """Get the money ledger singleton."""
    global _money_ledger
    if _money_ledger is None:
        _money_ledger = Ledger("money")
    return _money_ledger


def get_time_ledger() -> Ledger:
    """Get the time ledger singleton."""
    global _time_ledger
    if _time_ledger is None:
        _time_ledger = Ledger("time")
    return _time_ledger


def get_service_date_ledger() -> Ledger:
    """Get the service date ledger singleton."""
    global _service_date_ledger
    if _service_date_ledger is None:
        _service_date_ledger = Ledger("service_date")
    return _service_date_ledger


def get_statute_tracker() -> StatuteTracker:
    """Get the statute tracker singleton."""
    global _statute_tracker
    if _statute_tracker is None:
        _statute_tracker = StatuteTracker()
    return _statute_tracker
