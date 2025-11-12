"""
Contextual Help System - Tooltips and Inline Guidance

Wires human_perspective into UI elements to provide on-demand explanations
for terms, actions, deadlines, and complex concepts.
"""
from typing import Dict, Optional
from human_perspective import humanize_object

# Common legal/housing terms with contexts
TERM_CONTEXTS = {
    "eviction": {
        "term": "Eviction",
        "raw": "Legal process landlord uses to remove tenant from property",
        "audience": "tenant",
        "level": "plain"
    },
    "habitability": {
        "term": "Habitability",
        "raw": "Landlord must keep property safe and livable: working heat, water, no mold/pests",
        "audience": "tenant",
        "level": "plain"
    },
    "escrow": {
        "term": "Rent Escrow",
        "raw": "Pay rent to court instead of landlord while repair dispute is resolved",
        "audience": "tenant",
        "level": "simple"
    },
    "retaliation": {
        "term": "Retaliation",
        "raw": "Illegal for landlord to punish tenant for complaining about repairs or asserting rights",
        "audience": "tenant",
        "level": "plain"
    },
    "security_deposit": {
        "term": "Security Deposit",
        "raw": "Money landlord holds; must return with itemized deductions within legal timeframe (varies by state)",
        "audience": "tenant",
        "level": "simple"
    },
    "notice_to_quit": {
        "term": "Notice to Quit",
        "raw": "Official notice landlord gives before filing eviction; check if proper form and timeframe",
        "audience": "tenant",
        "level": "plain"
    },
    "constructive_eviction": {
        "term": "Constructive Eviction",
        "raw": "When conditions are so bad tenant is forced to leave; may not owe remaining rent",
        "audience": "tenant",
        "level": "simple"
    },
    "fair_housing": {
        "term": "Fair Housing",
        "raw": "Federal law prohibits discrimination based on race, color, religion, sex, disability, familial status, national origin",
        "audience": "tenant",
        "level": "standard"
    },
}

def get_tooltip(term: str, audience: str = "tenant") -> Optional[Dict]:
    """
    Get tooltip content for a term.
    
    Returns:
        {
            "term": "...",
            "explanation": "...",
            "next_steps": [...]
        }
    """
    context = TERM_CONTEXTS.get(term.lower())
    if not context:
        return None
    
    human_view = humanize_object(
        context["raw"],
        {"audience": audience, "reading_level": context.get("level", "plain")}
    )
    
    return {
        "term": context["term"],
        "explanation": human_view.get("summary", context["raw"]),
        "next_steps": human_view.get("next_steps", [])[:2],  # Just 2 for tooltips
        "audience_tip": human_view.get("audience_tip", "")
    }


def format_deadline(deadline_str: str, context: str = "") -> Dict:
    """
    Format a deadline in human terms with urgency and action steps.
    
    Args:
        deadline_str: ISO date like "2025-11-25"
        context: What the deadline is for (e.g., "eviction_answer")
    """
    from datetime import datetime, timedelta
    
    try:
        deadline = datetime.fromisoformat(deadline_str)
        now = datetime.now()
        days_left = (deadline - now).days
        
        if days_left < 0:
            urgency = "⚠️ PAST DUE"
            urgency_level = "critical"
        elif days_left == 0:
            urgency = "🔥 DUE TODAY"
            urgency_level = "critical"
        elif days_left <= 3:
            urgency = "🚨 URGENT"
            urgency_level = "high"
        elif days_left <= 7:
            urgency = "⏰ COMING UP"
            urgency_level = "medium"
        else:
            urgency = "📅 UPCOMING"
            urgency_level = "normal"
        
        human_date = deadline.strftime("%A, %B %d, %Y")
        
        # Context-specific actions
        actions = {
            "eviction_answer": [
                "File your written answer with the court NOW",
                "Bring copies to court on the hearing date",
                "Get free legal help if you haven't yet"
            ],
            "rent_payment": [
                "Pay rent or document why you're withholding",
                "Keep proof of payment (receipt, screenshot)",
                "If you can't pay, call legal aid immediately"
            ],
            "repair_response": [
                "Check if landlord fixed the issue",
                "Take dated photos if still not fixed",
                "Send follow-up letter via certified mail"
            ],
        }
        
        return {
            "deadline": human_date,
            "days_left": days_left,
            "urgency": urgency,
            "urgency_level": urgency_level,
            "actions": actions.get(context, ["Check what you need to do by this date", "Document everything", "Get help if needed"])
        }
    except Exception:
        return {
            "deadline": deadline_str,
            "days_left": None,
            "urgency": "📅",
            "urgency_level": "normal",
            "actions": ["Mark your calendar", "Check requirements"]
        }


def explain_form_field(field_name: str, form_type: str = "witness_statement") -> Dict:
    """
    Explain what a form field is asking for in plain language.
    
    Args:
        field_name: e.g., "incident_date", "witness_contact"
        form_type: e.g., "witness_statement", "complaint", "service_animal"
    """
    explanations = {
        "witness_statement": {
            "incident_date": "When did this happen? Be as specific as possible (date and time).",
            "location": "Where exactly did it happen? (Apartment 2B, hallway, parking lot, etc.)",
            "witness_name": "Who saw or heard this? Include yourself if you were there.",
            "description": "What happened? Write it like you're telling a friend—step by step, in order.",
            "evidence": "What can prove this? (Photos, videos, texts, emails, other witnesses)"
        },
        "complaint": {
            "complaint_type": "What are you filing about? (Repairs, harassment, discrimination, etc.)",
            "parties": "Who's involved? (You, landlord, property manager, etc.)",
            "relief_sought": "What do you want to happen? (Fix repairs, stop harassment, return deposit, etc.)",
            "facts": "What happened? Start from the beginning and write in order."
        },
        "service_animal": {
            "animal_type": "What kind of animal? (Dog, cat, miniature horse, etc.)",
            "disability": "You don't have to name the condition—just say you have a disability.",
            "tasks": "What does the animal do for you? (Alerts to anxiety, guides you, retrieves items, etc.)"
        }
    }
    
    form_fields = explanations.get(form_type, {})
    explanation = form_fields.get(field_name, "Fill this out with accurate information.")
    
    human_view = humanize_object(
        {"field": field_name, "form": form_type, "help": explanation},
        {"audience": "tenant", "reading_level": "plain"}
    )
    
    return {
        "field": field_name,
        "explanation": explanation,
        "tips": human_view.get("next_steps", [])[:2]
    }


# Helper for inline tooltips in templates
def get_inline_help(key: str, context: Dict = None) -> str:
    """
    Quick inline helper text for templates.
    Usage: {{ get_inline_help('eviction') }}
    """
    tooltip = get_tooltip(key)
    if tooltip:
        return f"ℹ️ {tooltip['explanation']}"
    return ""


if __name__ == "__main__":
    print("🧪 Testing Contextual Help System\n")
    
    # Test tooltip
    print("=== Tooltip Test ===")
    tip = get_tooltip("eviction")
    print(f"Term: {tip['term']}")
    print(f"Explanation: {tip['explanation']}")
    print(f"Next steps: {tip['next_steps']}\n")
    
    # Test deadline formatting
    print("=== Deadline Test ===")
    deadline = format_deadline("2025-11-15", "eviction_answer")
    print(f"Deadline: {deadline['deadline']}")
    print(f"Days left: {deadline['days_left']}")
    print(f"Urgency: {deadline['urgency']}")
    print(f"Actions: {deadline['actions']}\n")
    
    # Test form field explanation
    print("=== Form Field Test ===")
    field = explain_form_field("incident_date", "witness_statement")
    print(f"Field: {field['field']}")
    print(f"Explanation: {field['explanation']}")
    print(f"Tips: {field['tips']}")
