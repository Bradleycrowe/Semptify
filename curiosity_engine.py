"""
Curiosity Engine for Semptify
The app learns through curiosity - asking questions, researching, and improving.
Self-learning system that identifies knowledge gaps and seeks answers.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict, Counter


class CuriosityEngine:
    """
    Drives autonomous learning through curiosity.
    Identifies knowledge gaps → Generates questions → Researches answers → Improves predictions
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.questions_file = os.path.join(data_dir, "research_questions.json")
        self.knowledge_file = os.path.join(data_dir, "learned_knowledge.json")
        self.questions = self._load_questions()
        self.knowledge = self._load_knowledge()

    def _load_questions(self) -> Dict:
        """Load pending research questions."""
        if os.path.exists(self.questions_file):
            try:
                with open(self.questions_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "pending": [],     # Questions waiting for research
            "researching": [], # Currently researching
            "answered": []     # Completed research
        }

    def _load_knowledge(self) -> Dict:
        """Load learned knowledge base."""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "facts": {},           # Verified facts
            "patterns": {},        # Observed patterns
            "theories": {},        # Hypotheses being tested
            "improvements": [],    # How app improved over time
            "research_log": []     # History of curiosity-driven research
        }

    def _save_questions(self):
        """Persist research questions."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.questions_file, 'w') as f:
            json.dump(self.questions, f, indent=2)

    def _save_knowledge(self):
        """Persist learned knowledge."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)

    # ========================================================================
    # CURIOSITY TRIGGERS: What makes the app curious?
    # ========================================================================

    def detect_prediction_failure(
        self,
        prediction: Dict,
        actual_outcome: Dict
    ) -> Optional[str]:
        """
        When prediction is wrong, get curious about why.
        Returns: Question to research
        """
        predicted = prediction.get("outcome")
        actual = actual_outcome.get("outcome")

        if predicted == actual:
            return None  # Prediction was correct, no curiosity needed

        # App was wrong - generate curiosity question
        question = {
            "id": f"pf_{datetime.now().timestamp()}",
            "type": "prediction_failure",
            "trigger": "App predicted wrong outcome",
            "question": f"Why did we predict '{predicted}' but actual was '{actual}'?",
            "context": {
                "prediction": prediction,
                "actual": actual_outcome
            },
            "research_paths": [
                "Analyze case factors we missed",
                "Check if user deviated from suggested path",
                "Look for similar failed predictions",
                "Identify missing data that would have predicted correctly"
            ],
            "priority": "high",  # Prediction failures are important to learn from
            "created_at": datetime.now().isoformat()
        }

        self.questions["pending"].append(question)
        self._save_questions()

        return question["question"]

    def detect_anomaly(
        self,
        pattern_name: str,
        expected_behavior: str,
        observed_behavior: str,
        context: Dict
    ) -> Optional[str]:
        """
        When something unusual happens, get curious.
        Example: "One landlord never retaliates (anomaly)"
        """
        question = {
            "id": f"an_{datetime.now().timestamp()}",
            "type": "anomaly",
            "trigger": f"Unusual pattern in {pattern_name}",
            "question": f"Why is '{observed_behavior}' different from expected '{expected_behavior}'?",
            "context": context,
            "research_paths": [
                "Compare anomaly cases to normal cases",
                "Look for unique factors in anomaly",
                "Check if anomaly reveals better strategy",
                "Determine if anomaly is sustainable pattern"
            ],
            "priority": "medium",
            "created_at": datetime.now().isoformat()
        }

        self.questions["pending"].append(question)
        self._save_questions()

        return question["question"]

    def detect_knowledge_gap(
        self,
        topic: str,
        why_needed: str
    ) -> Optional[str]:
        """
        When app realizes it doesn't know something important.
        Example: "Users ask about repair costs, but I have no data"
        """
        question = {
            "id": f"kg_{datetime.now().timestamp()}",
            "type": "knowledge_gap",
            "trigger": f"Missing information about {topic}",
            "question": f"What is the answer to: {topic}?",
            "context": {
                "topic": topic,
                "why_needed": why_needed
            },
            "research_paths": [
                "Ask users who have this information",
                "Search public records",
                "Analyze similar cases for clues",
                "Cross-reference multiple data sources"
            ],
            "priority": "low",  # Not urgent, but improves usefulness
            "created_at": datetime.now().isoformat()
        }

        self.questions["pending"].append(question)
        self._save_questions()

        return question["question"]

    def detect_user_correction(
        self,
        suggestion: Dict,
        user_action: Dict,
        result: Dict
    ) -> Optional[str]:
        """
        When user ignores suggestion and succeeds, learn why.
        Example: "User filed with health dept (not rent board as suggested) and won faster"
        """
        question = {
            "id": f"uc_{datetime.now().timestamp()}",
            "type": "user_correction",
            "trigger": "User did something different and got better result",
            "question": f"Why did user's approach work better than our suggestion?",
            "context": {
                "our_suggestion": suggestion,
                "user_action": user_action,
                "result": result
            },
            "research_paths": [
                "Analyze why user's choice was better",
                "Check if this works for others too",
                "Update prediction model with new strategy",
                "Determine when to use this alternative path"
            ],
            "priority": "high",  # Users know things we don't
            "created_at": datetime.now().isoformat()
        }

        self.questions["pending"].append(question)
        self._save_questions()

        return question["question"]

    # ========================================================================
    # RESEARCH METHODS: How to find answers
    # ========================================================================

    def research_question(self, question_id: str) -> Dict:
        """
        Conduct research to answer a question.
        Returns: Research findings
        """
        # Find question
        question = None
        for q in self.questions["pending"]:
            if q["id"] == question_id:
                question = q
                break

        if not question:
            return {"error": "Question not found"}

        # Move to researching
        self.questions["pending"].remove(question)
        self.questions["researching"].append(question)
        self._save_questions()

        # Execute research based on type
        research_method = {
            "prediction_failure": self._research_prediction_failure,
            "anomaly": self._research_anomaly,
            "knowledge_gap": self._research_knowledge_gap,
            "user_correction": self._research_user_correction
        }

        handler = research_method.get(question["type"])
        if not handler:
            return {"error": f"No research method for {question['type']}"}

        findings = handler(question)

        # Record research completion
        question["findings"] = findings
        question["researched_at"] = datetime.now().isoformat()
        self.questions["researching"].remove(question)
        self.questions["answered"].append(question)
        self._save_questions()

        # Add to knowledge base
        self._integrate_findings(question, findings)

        return findings

    def _research_prediction_failure(self, question: Dict) -> Dict:
        """Research why a prediction was wrong."""
        prediction = question["context"]["prediction"]
        actual = question["context"]["actual"]

        findings = {
            "root_cause": "Analyzing...",
            "missing_factors": [],
            "correction": {}
        }

        # Check what factors were in prediction
        pred_factors = prediction.get("factors", {})
        actual_factors = actual.get("factors", {})

        # Find missing factors
        for key, value in actual_factors.items():
            if key not in pred_factors:
                findings["missing_factors"].append({
                    "factor": key,
                    "value": value,
                    "impact": "high"  # This factor wasn't in our model
                })

        # Determine root cause
        if findings["missing_factors"]:
            findings["root_cause"] = f"Prediction missing {len(findings['missing_factors'])} critical factors"
        else:
            findings["root_cause"] = "Factor weights may be incorrect"

        # Suggest correction
        findings["correction"] = {
            "action": "Add missing factors to prediction model",
            "new_factors": findings["missing_factors"],
            "expected_improvement": "15-25% better prediction accuracy"
        }

        return findings

    def _research_anomaly(self, question: Dict) -> Dict:
        """Research why something unusual happened."""
        context = question["context"]

        findings = {
            "unique_factors": [],
            "explanation": "",
            "actionable_insight": ""
        }

        # Look for unique characteristics in anomaly
        # (In real implementation, this would query user data)

        findings["explanation"] = "Anomaly shows alternative successful path"
        findings["actionable_insight"] = "Add anomaly strategy as option for users"

        return findings

    def _research_knowledge_gap(self, question: Dict) -> Dict:
        """Research missing information."""
        topic = question["context"]["topic"]

        findings = {
            "topic": topic,
            "sources": [],
            "data_collected": {},
            "confidence": "medium"
        }

        # In real implementation, this would:
        # - Query user database
        # - Search public records
        # - Aggregate data from multiple sources

        findings["sources"] = [
            "user_reports",
            "public_records",
            "court_documents"
        ]

        findings["data_collected"] = {
            "note": "Real implementation would populate with actual data",
            "example": "Average repair cost: $1,800"
        }

        return findings

    def _research_user_correction(self, question: Dict) -> Dict:
        """Research why user's approach worked better."""
        suggestion = question["context"]["our_suggestion"]
        user_action = question["context"]["user_action"]
        result = question["context"]["result"]

        findings = {
            "why_user_was_right": "",
            "when_to_use_user_method": "",
            "update_recommendations": {}
        }

        findings["why_user_was_right"] = "User's method achieved faster resolution"
        findings["when_to_use_user_method"] = "For health hazards, health dept is faster than rent board"
        findings["update_recommendations"] = {
            "old": suggestion,
            "new": user_action,
            "conditions": "Use for health_hazard category"
        }

        return findings

    def _integrate_findings(self, question: Dict, findings: Dict):
        """Add research findings to knowledge base."""
        entry = {
            "question": question["question"],
            "type": question["type"],
            "findings": findings,
            "learned_at": datetime.now().isoformat()
        }

        self.knowledge["research_log"].append(entry)

        # Add to facts if verified
        if question["type"] in ["knowledge_gap", "user_correction"]:
            fact_id = f"fact_{len(self.knowledge['facts']) + 1}"
            self.knowledge["facts"][fact_id] = {
                "statement": question["question"],
                "answer": findings,
                "confidence": findings.get("confidence", "high"),
                "source": question["type"]
            }

        # Add improvement tracking
        self.knowledge["improvements"].append({
            "timestamp": datetime.now().isoformat(),
            "improvement": f"Learned from {question['type']}",
            "question": question["question"],
            "impact": "Prediction accuracy should improve"
        })

        self._save_knowledge()

    # ========================================================================
    # SELF-IMPROVEMENT: App evaluates itself
    # ========================================================================

    def evaluate_performance(self, predictions: List[Dict]) -> Dict:
        """
        App evaluates its own performance and gets curious about failures.
        """
        total = len(predictions)
        correct = sum(1 for p in predictions if p.get("correct", False))
        accuracy = (correct / total * 100) if total > 0 else 0

        evaluation = {
            "total_predictions": total,
            "correct": correct,
            "accuracy": f"{accuracy:.1f}%",
            "curiosity_triggered": []
        }

        # Get curious about failures
        failures = [p for p in predictions if not p.get("correct", False)]

        for failure in failures:
            question = self.detect_prediction_failure(
                prediction=failure.get("prediction", {}),
                actual_outcome=failure.get("actual", {})
            )
            if question:
                evaluation["curiosity_triggered"].append(question)

        return evaluation

    def generate_research_agenda(self) -> List[Dict]:
        """
        App creates its own research agenda based on curiosity.
        Returns: Prioritized list of questions to research
        """
        pending = self.questions["pending"]

        # Sort by priority
        priority_order = {"high": 3, "medium": 2, "low": 1}
        sorted_questions = sorted(
            pending,
            key=lambda q: priority_order.get(q.get("priority", "low"), 0),
            reverse=True
        )

        agenda = {
            "total_questions": len(sorted_questions),
            "high_priority": len([q for q in sorted_questions if q.get("priority") == "high"]),
            "research_queue": sorted_questions[:10]  # Top 10
        }

        return agenda


# Global instance
_curiosity_engine = None

def get_curiosity() -> CuriosityEngine:
    """Get global curiosity engine instance."""
    global _curiosity_engine
    if _curiosity_engine is None:
        _curiosity_engine = CuriosityEngine()
    return _curiosity_engine
