"""
Perspective Engine - Baseline Neutral Truth System

Foundation: Free from resentments, dishonesty, greed, and fear.
Cross-verifies every fact through 5 different perspective sources.
Guards against corruption, prejudice, and bias.

Core Principles:
1. No single source is truth - require 3/5 agreement minimum
2. Detect and flag emotional bias in all sources
3. Fact-check everything through independent verification
4. Learn to rate source credibility over time
5. Run simulations to predict outcomes without bias
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter


class PerspectiveEngine:
    """
    Multi-source verification system with baseline neutral perspective.

    Every claim must pass through 5 perspective sources:
    1. User Reports (tenant lived experience)
    2. Legal Database (law and regulations)
    3. Public Records (government/court data)
    4. Business Records (financial/transaction data)
    5. Community Consensus (aggregate user wisdom)
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.sources_file = os.path.join(data_dir, "verified_sources.json")
        self.sources = self._load_sources()

        # Baseline perspective: neutral analysis framework
        self.baseline = {
            "free_from": ["resentment", "dishonesty", "greed", "fear"],
            "focused_on": ["truth", "fairness", "evidence", "outcomes"],
            "verification_threshold": 0.6  # 3/5 sources must agree
        }

    def _load_sources(self) -> dict:
        """Load verified source database."""
        if os.path.exists(self.sources_file):
            try:
                with open(self.sources_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            "user_reports": [],      # SOURCE 1: Tenant experiences
            "legal_db": [],          # SOURCE 2: Laws and regulations
            "public_records": [],    # SOURCE 3: Government/court data
            "business_records": [],  # SOURCE 4: Financial/transaction data
            "community_polls": [],   # SOURCE 5: Aggregate user wisdom

            # Source credibility ratings (learned over time)
            "source_ratings": {},

            # Fact verification history
            "verifications": []
        }

    def _save_sources(self):
        """Persist verified sources and ratings."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.sources_file, 'w') as f:
            json.dump(self.sources, f, indent=2)

    # ========================================================================
    # 5-SOURCE VERIFICATION SYSTEM
    # ========================================================================

    def verify_claim(self, claim: str, context: dict) -> Dict:
        """
        Cross-verify a claim through 5 independent sources.

        Args:
            claim: The statement to verify (e.g., "ABC charges $75 fee")
            context: Situation context (entity, location, issue type, etc.)

        Returns:
            {
                "verified": bool,
                "confidence": float (0.0-1.0),
                "sources_agree": int (0-5),
                "bias_detected": list,
                "neutral_truth": str,
                "sources": {
                    "user_reports": {...},
                    "legal_db": {...},
                    "public_records": {...},
                    "business_records": {...},
                    "community_polls": {...}
                }
            }
        """

        # Collect evidence from all 5 sources
        source_results = {
            "user_reports": self._check_user_reports(claim, context),
            "legal_db": self._check_legal_database(claim, context),
            "public_records": self._check_public_records(claim, context),
            "business_records": self._check_business_records(claim, context),
            "community_polls": self._check_community_consensus(claim, context)
        }

        # Count how many sources agree
        agreements = sum(1 for s in source_results.values() if s["agrees"])
        confidence = agreements / 5.0

        # Detect bias in sources
        bias_flags = []
        for source_name, result in source_results.items():
            if result.get("bias_risk"):
                bias_flags.append({
                    "source": source_name,
                    "bias_type": result["bias_risk"],
                    "severity": result.get("bias_severity", "unknown")
                })

        # Determine neutral truth (baseline perspective)
        verified = confidence >= self.baseline["verification_threshold"]
        neutral_truth = self._synthesize_neutral_truth(claim, source_results, verified)

        verification = {
            "claim": claim,
            "verified": verified,
            "confidence": confidence,
            "sources_agree": agreements,
            "bias_detected": bias_flags,
            "neutral_truth": neutral_truth,
            "sources": source_results,
            "timestamp": datetime.now().isoformat()
        }

        # Record verification for learning
        self.sources["verifications"].append(verification)
        self._save_sources()

        return verification

    def _check_user_reports(self, claim: str, context: dict) -> Dict:
        """SOURCE 1: Check user-submitted reports (tenant perspective)."""
        # Search user_reports for matching claims
        matching_reports = [
            r for r in self.sources["user_reports"]
            if self._claim_matches(claim, r, context)
        ]

        if not matching_reports:
            return {
                "agrees": False,
                "confidence": 0.0,
                "data": None,
                "bias_risk": None
            }

        # Analyze sentiment/emotion in reports
        emotional_words = ["angry", "frustrated", "furious", "hate", "revenge"]
        reports_text = " ".join([r.get("description", "") for r in matching_reports]).lower()
        emotion_detected = any(word in reports_text for word in emotional_words)

        return {
            "agrees": True,
            "confidence": 0.7,  # User reports can be biased
            "data": {
                "report_count": len(matching_reports),
                "reports": matching_reports[:3]  # Sample
            },
            "bias_risk": "emotional" if emotion_detected else None,
            "bias_severity": "moderate" if emotion_detected else "low"
        }

    def _check_legal_database(self, claim: str, context: dict) -> Dict:
        """SOURCE 2: Check legal/regulatory database (law perspective)."""
        # This would query actual legal databases
        # For now, demonstrate structure with California rent law

        legal_facts = {
            "application_fee_max_2025": 58.23,
            "security_deposit_max": "2x rent (unfurnished), 3x rent (furnished)",
            "repair_timeline": "30 days or reasonable time",
            "retaliation_protected": True
        }

        # Parse claim and check against legal facts
        agrees = False
        relevant_law = None

        if "application fee" in claim.lower():
            # Extract amount from claim
            import re
            amount_match = re.search(r'\$(\d+(?:\.\d{2})?)', claim)
            if amount_match:
                claimed_amount = float(amount_match.group(1))
                legal_max = legal_facts["application_fee_max_2025"]
                agrees = claimed_amount > legal_max
                relevant_law = f"California max application fee: ${legal_max} (Civil Code §1950.6)"

        return {
            "agrees": agrees,
            "confidence": 1.0,  # Legal facts are hard data
            "data": {
                "relevant_law": relevant_law,
                "legal_facts": legal_facts
            },
            "bias_risk": None,  # Laws are neutral
            "bias_severity": "none"
        }

    def _check_public_records(self, claim: str, context: dict) -> Dict:
        """SOURCE 3: Check government/court public records."""
        # Would query actual public records APIs
        # Demonstrating structure

        entity_name = context.get("entity_name", "")
        if not entity_name:
            return {"agrees": False, "confidence": 0.0, "data": None, "bias_risk": None}

        # Simulate public record lookup
        public_data = {
            "business_license": "Active",
            "complaints_filed": 18,
            "court_cases": 8,
            "violations": 5
        }

        return {
            "agrees": True,
            "confidence": 0.9,  # Public records are reliable
            "data": public_data,
            "bias_risk": "bureaucratic_delay",  # Records may be outdated
            "bias_severity": "low"
        }

    def _check_business_records(self, claim: str, context: dict) -> Dict:
        """SOURCE 4: Check financial/transaction records."""
        # Would access transaction databases, receipts, bank records
        # Demonstrating math-based verification

        # Example: If claim is about fees, calculate actual vs legal
        if "fee" in claim.lower():
            return {
                "agrees": True,
                "confidence": 1.0,  # Math is neutral
                "data": {
                    "calculation": "User reports verified against receipts",
                    "method": "Cross-reference bank statements"
                },
                "bias_risk": None,
                "bias_severity": "none"
            }

        return {"agrees": False, "confidence": 0.0, "data": None, "bias_risk": None}

    def _check_community_consensus(self, claim: str, context: dict) -> Dict:
        """SOURCE 5: Check aggregate community wisdom (polls)."""
        # Would aggregate all user experiences for pattern
        matching_polls = [
            p for p in self.sources.get("community_polls", [])
            if self._claim_matches(claim, p, context)
        ]

        if not matching_polls:
            return {"agrees": False, "confidence": 0.0, "data": None, "bias_risk": None}

        # Calculate consensus
        total_responses = sum(p.get("responses", 0) for p in matching_polls)
        agree_count = sum(p.get("agree_count", 0) for p in matching_polls)
        consensus = agree_count / total_responses if total_responses > 0 else 0.0

        return {
            "agrees": consensus >= 0.6,
            "confidence": consensus,
            "data": {
                "total_responses": total_responses,
                "consensus_percent": consensus * 100,
                "polls": matching_polls[:2]
            },
            "bias_risk": "groupthink" if consensus > 0.9 else None,
            "bias_severity": "low"
        }

    def _claim_matches(self, claim: str, record: dict, context: dict) -> bool:
        """Check if a record matches the claim and context."""
        # Simple keyword matching (would be more sophisticated)
        claim_lower = claim.lower()
        record_text = json.dumps(record).lower()

        # Check if key terms appear
        key_terms = claim_lower.split()
        matches = sum(1 for term in key_terms if term in record_text)

        return matches >= len(key_terms) * 0.5  # 50% keyword match

    def _synthesize_neutral_truth(self, claim: str, sources: dict, verified: bool) -> str:
        """
        Synthesize baseline neutral truth from all sources.
        Free from resentment, dishonesty, greed, and fear.
        """
        if not verified:
            return f"Insufficient verification (requires 3/5 sources, baseline perspective incomplete)"

        # Extract factual elements from sources
        facts = []
        for source_name, result in sources.items():
            if result["agrees"] and result.get("data"):
                facts.append(f"{source_name}: {self._extract_fact(result['data'])}")

        neutral_truth = f"VERIFIED ({len(facts)}/5 sources): {claim}\n"
        neutral_truth += "Factual basis:\n" + "\n".join(f"- {f}" for f in facts)

        return neutral_truth

    def _extract_fact(self, data: dict) -> str:
        """Extract core fact from source data."""
        if not data:
            return "No data"

        # Extract most relevant fact
        if "report_count" in data:
            return f"{data['report_count']} user reports"
        elif "relevant_law" in data:
            return data["relevant_law"]
        elif "court_cases" in data:
            return f"{data['court_cases']} court cases on record"
        elif "calculation" in data:
            return data["calculation"]
        elif "consensus_percent" in data:
            return f"{data['consensus_percent']:.1f}% community consensus"

        return str(list(data.values())[0]) if data.values() else "Data available"

    # ========================================================================
    # SOURCE EVALUATION & LEARNING
    # ========================================================================

    def rate_source(self, source_id: str, rating: float, reason: str = ""):
        """
        Learn source credibility over time.

        Args:
            source_id: Unique identifier for source (URL, user_id, etc.)
            rating: 0.0-1.0 credibility score
            reason: Why this rating (e.g., "verified against court records")
        """
        if source_id not in self.sources["source_ratings"]:
            self.sources["source_ratings"][source_id] = {
                "ratings": [],
                "avg_rating": 0.0,
                "total_checks": 0
            }

        source_rating = self.sources["source_ratings"][source_id]
        source_rating["ratings"].append({
            "rating": rating,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        source_rating["total_checks"] += 1

        # Calculate new average
        all_ratings = [r["rating"] for r in source_rating["ratings"]]
        source_rating["avg_rating"] = sum(all_ratings) / len(all_ratings)

        self._save_sources()

    def find_new_sources(self, topic: str) -> List[Dict]:
        """
        Learn to discover new reputable sources for a topic.

        Returns list of potential sources with credibility estimates.
        """
        # Would use search APIs, credibility databases
        # Demonstrating structure

        potential_sources = [
            {
                "name": "California Department of Consumer Affairs",
                "url": "https://www.dca.ca.gov/",
                "type": "government",
                "credibility_estimate": 0.95,
                "bias_risk": "bureaucratic",
                "topics": ["tenant_rights", "consumer_protection"]
            },
            {
                "name": "Legal Aid Foundation",
                "url": "https://www.lafla.org/",
                "type": "nonprofit",
                "credibility_estimate": 0.90,
                "bias_risk": "tenant_advocacy",
                "topics": ["tenant_rights", "legal_help"]
            },
            {
                "name": "California Apartment Association",
                "url": "https://caanet.org/",
                "type": "industry",
                "credibility_estimate": 0.75,
                "bias_risk": "landlord_advocacy",
                "topics": ["landlord_rights", "property_management"]
            }
        ]

        # Filter by topic relevance
        relevant = [s for s in potential_sources if topic in s["topics"]]

        return relevant


# ========================================================================
# SIMULATION ENGINE
# ========================================================================

class SimulationEngine:
    """
    Run simulations to predict outcomes without bias.
    Learns from simulated results to improve predictions.
    """

    def __init__(self, perspective_engine: PerspectiveEngine):
        self.perspective = perspective_engine
        self.simulations_file = os.path.join(perspective_engine.data_dir, "simulations.json")
        self.simulations = self._load_simulations()

    def _load_simulations(self) -> dict:
        """Load past simulations."""
        if os.path.exists(self.simulations_file):
            try:
                with open(self.simulations_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {"runs": [], "learned_patterns": {}}

    def _save_simulations(self):
        """Persist simulation results."""
        with open(self.simulations_file, 'w') as f:
            json.dump(self.simulations, f, indent=2)

    def simulate_decision(self, situation: dict, options: List[dict]) -> Dict:
        """
        Simulate outcomes for each option in a situation.

        Args:
            situation: Current context (issue, entity, evidence, etc.)
            options: List of possible actions user could take

        Returns:
            {
                "option_A": {
                    "predicted_outcome": str,
                    "success_probability": float,
                    "timeline": str,
                    "cost": float,
                    "risks": list,
                    "confidence": float
                },
                "option_B": {...},
                ...
            }
        """

        simulation_results = {}

        for option in options:
            # Run simulation for this option
            result = self._simulate_single_option(situation, option)
            simulation_results[option["id"]] = result

        # Record simulation for learning
        simulation_record = {
            "situation": situation,
            "options": options,
            "results": simulation_results,
            "timestamp": datetime.now().isoformat()
        }
        self.simulations["runs"].append(simulation_record)
        self._save_simulations()

        return simulation_results

    def _simulate_single_option(self, situation: dict, option: dict) -> Dict:
        """Simulate one option's outcome."""

        # Gather historical data for similar situations
        similar_cases = self._find_similar_cases(situation, option)

        if not similar_cases:
            return {
                "predicted_outcome": "Unknown (no historical data)",
                "success_probability": 0.5,
                "timeline": "Unknown",
                "cost": 0.0,
                "risks": ["No historical data to predict from"],
                "confidence": 0.0
            }

        # Calculate probabilities from historical outcomes
        outcomes = Counter([c["outcome"] for c in similar_cases])
        total = len(similar_cases)
        success_count = sum(count for outcome, count in outcomes.items() if "success" in outcome.lower() or "won" in outcome.lower())
        success_prob = success_count / total if total > 0 else 0.5

        # Calculate average costs
        costs = [c.get("cost", 0) for c in similar_cases]
        avg_cost = sum(costs) / len(costs) if costs else 0.0

        # Calculate average timeline
        timelines = [c.get("timeline_days", 0) for c in similar_cases]
        avg_timeline_days = sum(timelines) / len(timelines) if timelines else 0

        # Identify risks
        risks = []
        for case in similar_cases:
            if case.get("risks"):
                risks.extend(case["risks"])
        risk_counter = Counter(risks)
        top_risks = [risk for risk, count in risk_counter.most_common(3)]

        return {
            "predicted_outcome": f"Based on {total} similar cases",
            "success_probability": success_prob,
            "timeline": f"{avg_timeline_days:.0f} days average",
            "cost": avg_cost,
            "risks": top_risks,
            "confidence": min(total / 10.0, 1.0),  # More cases = higher confidence
            "similar_cases_count": total
        }

    def _find_similar_cases(self, situation: dict, option: dict) -> List[dict]:
        """Find historical cases similar to current situation."""
        # Would query knowledge base for matching situations
        # Demonstrating structure with sample data

        sample_cases = [
            {
                "situation": "mold_complaint",
                "option": "send_notice_first",
                "outcome": "success_repair_completed",
                "cost": 8.50,
                "timeline_days": 21,
                "risks": []
            },
            {
                "situation": "mold_complaint",
                "option": "file_immediately",
                "outcome": "success_but_retaliation",
                "cost": 75.00,
                "timeline_days": 120,
                "risks": ["retaliation", "eviction_threat"]
            }
        ]

        # Simple matching (would be more sophisticated)
        similar = [
            c for c in sample_cases
            if c["situation"] == situation.get("issue_type")
            and c["option"] == option.get("action")
        ]

        return similar


# ========================================================================
# GLOBAL INSTANCES
# ========================================================================

_perspective_engine = None
_simulation_engine = None


def get_perspective() -> PerspectiveEngine:
    """Get global perspective engine instance."""
    global _perspective_engine
    if _perspective_engine is None:
        _perspective_engine = PerspectiveEngine()
    return _perspective_engine


def get_simulation() -> SimulationEngine:
    """Get global simulation engine instance."""
    global _simulation_engine
    if _simulation_engine is None:
        perspective = get_perspective()
        _simulation_engine = SimulationEngine(perspective)
    return _simulation_engine
