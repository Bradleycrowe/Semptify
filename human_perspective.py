"""
Human Perspective Module

Purpose: transform technical or raw objects (text or JSON) into clear, human-centered explanations
for specific audiences and reading levels. Emphasizes Semptify's motto: Document everything!
"""
from typing import Any, Dict

READING_LEVELS = {
    "plain":  "Use simple words. Short sentences. No jargon.",
    "simple": "Everyday language. Explain any legal terms in one line.",
    "standard": "Clear and complete. Use definitions when needed.",
    "professional": "Use proper legal/technical terms with brief clarifications.",
}

AUDIENCE_TIPS = {
    "tenant": "Focus on practical steps. What to do next. What to save as evidence.",
    "advocate": "Highlight rights, deadlines, evidence standards, and escalation paths.",
    "judge": "Organize facts, timeline, exhibits, and relevant statutes clearly.",
    "landlord": "State obligations, notice requirements, and remediation timelines.",
}

def _summarize_text(text: str) -> str:
    text = text.strip()
    if len(text) <= 200:
        return text
    return text[:197] + "..."


def humanize_object(obj: Any, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return a human-centered view with title, summary, next-steps, and tips.

    Args:
        obj: text or JSON-like structure
        context: {format_pref, audience, reading_level}
    """
    context = context or {}
    audience = context.get("audience", "tenant")
    level = context.get("reading_level", "plain")

    base = {
        "title": "Humanized View",
        "audience": audience,
        "reading_level": level,
        "style": READING_LEVELS.get(level, READING_LEVELS["plain"]),
        "audience_tip": AUDIENCE_TIPS.get(audience, AUDIENCE_TIPS["tenant"]),
    }

    if isinstance(obj, str):
        base.update({
            "summary": _summarize_text(obj),
            "kind": "text",
        })
    else:
        # Treat as JSON-like
        import json
        try:
            preview = json.dumps(obj, indent=2)[:600]
        except Exception:
            preview = str(obj)
        base.update({
            "summary": preview,
            "kind": "json",
        })

    # Opinionated next steps for tenants: document everything
    next_steps = [
        "Write down what happened in order (who/what/when/where).",
        "Upload pictures, screenshots, and documents to your vault.",
        "Add events to your timeline with exact dates and times.",
        "Create a witness statement if others saw/heard it.",
        "Save copies of all messages and notices (texts, emails, letters).",
    ]

    base["next_steps"] = next_steps

    return base
