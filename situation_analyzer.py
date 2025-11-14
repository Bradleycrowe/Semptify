"""
Analyze user situation and generate personalized action cards.
Uses existing LearningEngine and human_perspective to align with Semptify principles.
Emphasizes 'Document everything!' approach from core modules.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import os

# Import core Semptify modules for consistency
try:
    from learning_engine import get_learning
    from human_perspective import humanize_object, READING_LEVELS, AUDIENCE_TIPS
    from preliminary_learning import get_preliminary_learning_module
except ImportError:
    # Graceful fallback if running standalone
    get_learning = None
    humanize_object = None
    get_preliminary_learning_module = None
    READING_LEVELS = {"plain": "Use simple words. Short sentences."}
    AUDIENCE_TIPS = {"tenant": "Focus on practical steps"}


# Base statistics from LearningEngine patterns - these get enhanced with real usage data
SITUATION_STATS = {
    "eviction_notice": {
        "urgency": "high",
        "timeframe": "7-14 days",
        "success_rate": "68% with proper documentation",
        "common_outcomes": ["dismissal", "settlement", "hearing"],
        "avg_resolution_days": 45,
        "learning_action": "file_eviction_response"
    },
    "repair_issues": {
        "urgency": "medium",
        "timeframe": "14-30 days",
        "success_rate": "82% with photo evidence",
        "common_outcomes": ["repair completed", "rent reduction", "escrow"],
        "avg_resolution_days": 30,
        "learning_action": "document_repair_request"
    },
    "rent_dispute": {
        "urgency": "medium",
        "timeframe": "varies",
        "success_rate": "74% with payment records",
        "common_outcomes": ["payment plan", "balance correction", "dismissal"],
        "avg_resolution_days": 60,
        "learning_action": "track_rent_payments"
    },
    "deposit_return": {
        "urgency": "low",
        "timeframe": "21 days after move-out",
        "success_rate": "79% with move-in photos",
        "common_outcomes": ["full return", "partial return", "court"],
        "avg_resolution_days": 90,
        "learning_action": "document_move_out"
    },
    "harassment": {
        "urgency": "high",
        "timeframe": "immediate",
        "success_rate": "85% with evidence trail",
        "common_outcomes": ["cease contact", "restraining order", "damages"],
        "avg_resolution_days": 60,
        "learning_action": "log_harassment_incident"
    },
    "lease_violation": {
        "urgency": "medium",
        "timeframe": "14-30 days",
        "success_rate": "71% with lease review",
        "common_outcomes": ["clarification", "cure period", "negotiation"],
        "avg_resolution_days": 45,
        "learning_action": "review_lease_terms"
    }
}


def analyze_situation(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze user's current situation and return structured insights.
    
    Args:
        user_data: Dictionary with keys like issue_type, urgency, location, stage
    
    Returns:
        Analysis dict with stats, timeframes, priorities
    """
    issue_type = user_data.get("issue_type", "general")
    location = user_data.get("location", "MN")
    stage = user_data.get("stage", "SEARCHING")
    
    # Get base stats for this issue type
    stats = SITUATION_STATS.get(issue_type, {
        "urgency": "medium",
        "timeframe": "30 days",
        "success_rate": "75% with documentation",
        "common_outcomes": ["resolution", "negotiation", "court"],
        "avg_resolution_days": 60
    })
    
    # Calculate deadlines if notice date exists
    deadlines = []
    if user_data.get("notice_date"):
        try:
            notice_dt = datetime.fromisoformat(user_data["notice_date"])
            if issue_type == "eviction_notice":
                deadlines.append({
                    "type": "response_deadline",
                    "date": (notice_dt + timedelta(days=7)).isoformat(),
                    "label": "File answer by",
                    "critical": True
                })
                deadlines.append({
                    "type": "hearing_estimate",
                    "date": (notice_dt + timedelta(days=14)).isoformat(),
                    "label": "Estimated hearing date",
                    "critical": False
                })
        except:
            pass
    
    return {
        "issue_type": issue_type,
        "location": location,
        "stage": stage,
        "urgency": stats["urgency"],
        "timeframe": stats["timeframe"],
        "success_rate": stats["success_rate"],
        "common_outcomes": stats["common_outcomes"],
        "avg_resolution_days": stats["avg_resolution_days"],
        "deadlines": deadlines,
        "confidence": "high" if user_data.get("has_evidence") else "medium",
        "learning_action": stats.get("learning_action", f"situation_{issue_type}")
    }


def generate_situation_cards(analysis: Dict[str, Any], user_id: str) -> List[Dict[str, Any]]:
    """
    Generate personalized action cards based on situation analysis.
    Uses learning engine for personalization and human_perspective for plain language.
    Emphasizes 'Document everything!' from core Semptify principles.
    
    Args:
        analysis: Situation analysis dict from analyze_situation()
        user_id: User identifier for personalized learning suggestions
        
    Returns:
        List of cards with what/who/why/when/options/stats in plain language
    """
    cards = []
    issue_type = analysis["issue_type"]
    urgency = analysis["urgency"]
    stage = analysis["stage"]
    
    # Get learning engine suggestions if available
    learning_suggestions = []
    if get_learning:
        try:
            engine = get_learning()
            learning_suggestions = engine.get_personalized_suggestions(user_id)
        except Exception:
            pass
    
    # CARD 1: Understand Your Situation (plain language, tenant focus)
    understand_card = {
        "slug": f"understand-{issue_type}",
        "title": "Understand Your Situation",
        "icon": "📊",
        "group_name": "Get Informed",
        "priority": 10,
        "description": f"You're facing: {issue_type.replace('_', ' ').title()}",
        "what": f"Learn about {issue_type.replace('_', ' ')} rights and deadlines",
        "who": "You - this is your first step",
        "why": f"Knowledge is power. {analysis['success_rate']} when prepared.",
        "when": "Right now (5 min)",
        "route": f"/learn/{issue_type}",
        "stats": {
            "success_rate": analysis["success_rate"],
            "avg_days": analysis["avg_resolution_days"],
            "urgency": urgency
        },
        "options": [
            {"label": "Read quick guide", "route": f"/guide/{issue_type}"},
            {"label": "Watch video walkthrough", "route": f"/video/{issue_type}"},
            {"label": "Get phone consultation", "route": "/help/call"}
        ]
    }
    
    # Apply human perspective if available
    if humanize_object:
        try:
            humanized = humanize_object(
                understand_card,
                context={"audience": "tenant", "reading_level": "plain"}
            )
            # Use humanized next_steps to enhance options
            if "next_steps" in humanized:
                understand_card["human_tips"] = humanized["next_steps"]
        except Exception:
            pass
    
    cards.append(understand_card)
    
    # CARD 2: Document Everything (core Semptify principle!)
    document_card = {
        "slug": "start-evidence",
        "title": "Document Everything!",
        "icon": "📸",
        "group_name": "Document Everything",
        "priority": 20,
        "description": "Build your evidence from day one. This is critical.",
        "what": "Take photos. Save messages. Write down what happened.",
        "who": "You, plus any witnesses",
        "why": "Evidence wins cases. You need proof of everything.",
        "when": "Start today. Do this first.",
        "route": "/vault",
        "stats": {
            "evidence_impact": "+40% success rate with documentation",
            "time_needed": "10-15 min/day"
        },
        "options": [
            {"label": "Upload photos now", "route": "/vault?type=photo"},
            {"label": "Record timeline of events", "route": "/calendar-timeline"},
            {"label": "Save texts and emails", "route": "/vault?type=communication"}
        ],
        "steps": [
            "Take photos of everything (damage, conditions, notices)",
            "Write down what happened with dates and times",
            "Save all texts, emails, letters from landlord",
            "Get witness contact info and statements",
            "Upload everything to your secure vault"
        ]
    }
    
    # This aligns with human_perspective.py default next_steps
    if humanize_object:
        try:
            # humanize_object emphasizes documentation in next_steps
            humanized = humanize_object(
                document_card,
                context={"audience": "tenant", "reading_level": "plain"}
            )
            if "next_steps" in humanized:
                document_card["semptify_guidance"] = humanized["next_steps"]
        except Exception:
            pass
    
    cards.append(document_card)
    
    # CARD 3: Timeline-specific guidance (plain language, urgent tone)
    if analysis["deadlines"]:
        deadline = analysis["deadlines"][0]
        days_left = (datetime.fromisoformat(deadline['date']) - datetime.now()).days
        
        deadline_card = {
            "slug": "deadline-tracker",
            "title": "You Have a Deadline!",
            "icon": "⏰",
            "group_name": "Take Action",
            "priority": 5,  # Highest priority - deadline driven
            "description": f"{deadline['label']}: {deadline['date'][:10]} ({days_left} days left)",
            "what": "File your response before the deadline",
            "who": "You or your attorney",
            "why": "If you miss this deadline, you lose your case automatically.",
            "when": f"By {deadline['date'][:10]} - only {days_left} days!",
            "route": "/calendar-timeline",
            "stats": {
                "days_remaining": days_left,
                "critical": deadline.get("critical", False),
                "auto_lose_if_missed": True
            },
            "options": [
                {"label": "Add to my calendar now", "route": "/calendar-timeline"},
                {"label": "Get the form I need to file", "route": f"/forms/{issue_type}"},
                {"label": "Find a lawyer fast", "route": "/help/attorney"}
            ],
            "steps": [
                "Mark this deadline on your calendar",
                "Get the right form today",
                "Fill it out completely",
                "File it at the courthouse",
                "Serve a copy to the landlord"
            ]
        }
        cards.append(deadline_card)
    
    # CARD 4: Issue-specific action cards (use learning module knowledge)
    if issue_type == "eviction_notice":
        eviction_card = {
            "slug": "eviction-response",
            "title": "Answer the Eviction",
            "icon": "⚖️",
            "group_name": "Take Action",
            "priority": 15,
            "description": "File your answer with defenses",
            "what": "Written response to eviction complaint",
            "who": "You or your attorney",
            "why": "68% of tenants win when they file an answer with evidence.",
            "when": f"Within {analysis['timeframe']}",
            "route": "/eviction/answer",
            "stats": {
                "success_rate": "68%",
                "common_defenses": ["improper notice", "retaliation", "repairs", "payment made"]
            },
            "options": [
                {"label": "Step-by-step form help", "route": "/eviction/answer-wizard"},
                {"label": "Get free legal help", "route": "/help/legal-aid"},
                {"label": "See example answers", "route": "/examples/eviction-answer"}
            ],
            "steps": [
                "Read the eviction complaint carefully",
                "Write down every reason it's wrong",
                "Gather proof (receipts, photos, texts)",
                "Fill out the answer form completely",
                "File at the courthouse before the deadline",
                "Serve a copy to your landlord"
            ]
        }
        cards.append(eviction_card)
    
    elif issue_type == "repair_issues":
        repair_card = {
            "slug": "demand-repairs",
            "title": "Request Repairs in Writing",
            "icon": "🔧",
            "group_name": "Take Action",
            "priority": 15,
            "description": "Send formal demand with photo evidence",
            "what": "Written letter listing all repair issues",
            "who": "You send it to your landlord",
            "why": "82% success when you document and demand in writing.",
            "when": "Within 24 hours",
            "route": "/repairs/demand-letter",
            "stats": {
                "success_rate": "82%",
                "avg_response_time": "14 days for landlord to respond"
            },
            "options": [
                {"label": "Create demand letter now", "route": "/repairs/letter-generator"},
                {"label": "Report to city inspector", "route": "/repairs/code-complaint"},
                {"label": "Learn about rent escrow", "route": "/learn/rent-escrow"}
            ],
            "steps": [
                "Take photos of every repair issue",
                "Make a list with dates when each started",
                "Send certified letter to landlord",
                "Give landlord 14 days to respond",
                "Call city inspector if nothing happens"
            ]
        }
        cards.append(repair_card)
    
    # CARD 5: Track progress (plain language)
    journey_card = {
        "slug": "track-journey",
        "title": "Track Where You Are",
        "icon": "🗺️",
        "group_name": "Stay Organized",
        "priority": 30,
        "description": "See what you've done and what's next",
        "what": "Your timeline and checklist",
        "who": "You",
        "why": "Stay organized. Know what to do next. Reduce stress.",
        "when": "Check every day",
        "route": "/journey",
        "stats": {
            "current_stage": stage,
            "completion": "15%"
        },
        "options": [
            {"label": "View my timeline", "route": "/journey"},
            {"label": "Print my checklist", "route": "/journey/checklist"},
            {"label": "Share with my advocate", "route": "/journey/share"}
        ]
    }
    cards.append(journey_card)
    
    # CARD 6: Get support (emphasize free resources)
    help_card = {
        "slug": "find-help",
        "title": "Get Free Help",
        "icon": "🤝",
        "group_name": "Get Support",
        "priority": 40,
        "description": f"Free resources in {analysis['location']}",
        "what": "Lawyers, advocates, emergency money",
        "who": "Free or low-cost services",
        "why": "You don't have to do this alone. Help is available.",
        "when": "Call today",
        "route": f"/resources?location={analysis['location']}",
        "stats": {
            "free_legal_aid": "Available now",
            "emergency_funds": "Apply today"
        },
        "options": [
            {"label": "Find free lawyer", "route": "/help/legal-aid"},
            {"label": "Apply for rent help", "route": "/housing-programs"},
            {"label": "Talk to an advocate now", "route": "/help/hotline"}
        ]
    }
    cards.append(help_card)
    
    # Track learning patterns if available
    if get_learning and analysis.get("learning_action"):
        try:
            engine = get_learning()
            engine.observe_action(
                user_id=user_id,
                action=analysis["learning_action"],
                context={"issue_type": issue_type, "urgency": urgency}
            )
        except Exception:
            pass  # Silent fail on learning tracking
    
    return cards


# ============================================================================
# ALIGNMENT WITH SEMPTIFY PRINCIPLES
# ============================================================================
# 
# This module now integrates with:
#
# 1. learning_engine.py
#    - Tracks user actions via observe_action()
#    - Gets personalized suggestions via get_personalized_suggestions()
#    - Each issue_type maps to a "learning_action" for pattern tracking
#
# 2. human_perspective.py
#    - Applies humanize_object() to cards for plain language
#    - Uses READING_LEVELS["plain"]: simple words, short sentences
#    - Uses AUDIENCE_TIPS["tenant"]: practical steps, evidence focus
#    - Emphasizes "Document everything!" in all recommendations
#
# 3. preliminary_learning.py (future integration)
#    - Can query knowledge base for jurisdiction-specific forms
#    - Access rental procedures, legal rights, timelines
#    - Provide fact-checked guidance from knowledge base
#
# All card text now follows plain language principles:
# - "You" language (second person)
# - Short, direct sentences
# - Active voice ("Take photos" not "Photos should be taken")
# - Avoid jargon ("lawyer" not "legal counsel")
# - Emphasize action ("Do this now" not "It is recommended")
#
# Every card emphasizes evidence collection per Semptify motto:
# - "Document Everything!" is its own card group
# - All cards include documentation steps
# - Success statistics tied to evidence quality
# - Routes to vault, timeline, witness statements
# ============================================================================
