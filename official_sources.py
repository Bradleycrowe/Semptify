"""
Official source verification policy.

RULE: .gov sources are AUTHORITATIVE for legal facts.
      Non-gov sources can provide context, opinion, analysis - but NOT legal claims.
      
When verifying legal facts (statutes, case law, regulations): MUST use .gov
When providing context (news, advocacy, explanations): Can use reputable non-gov
"""
from __future__ import annotations
import os
import re
from typing import List

ALLOWED_OFFICIAL_DOMAINS: List[str] = [
    r"^https?://([A-Za-z0-9-]+\.)*revisor\.mn\.gov/",
    r"^https?://([A-Za-z0-9-]+\.)*mncourts\.gov/",
    r"^https?://([A-Za-z0-9-]+\.)*state\.mn\.us/",
    r"^https?://([A-Za-z0-9-]+\.)*mn\.gov/",
    r"^https?://([A-Za-z0-9-]+\.)*\.gov/",
]

# For legal fact verification: must be True
# For opinion/context gathering: can be False
REQUIRE_OFFICIAL_FOR_LEGAL_FACTS: bool = os.getenv('REQUIRE_OFFICIAL_FOR_LEGAL_FACTS', '1') not in ('0', 'false', 'False')

def is_official_source(url: str) -> bool:
    """Check if URL is from official government source."""
    return any(re.match(p, url) for p in ALLOWED_OFFICIAL_DOMAINS)

def classify_source(url: str) -> str:
    """
    Classify source type:
    - 'official': .gov domain, authoritative for legal facts
    - 'reputable': Known news/advocacy (can provide context)
    - 'unknown': Unverified
    """
    if is_official_source(url):
        return 'official'
    
    # Reputable non-gov sources for context (not legal claims)
    reputable_patterns = [
        r'.*nytimes\.com',
        r'.*apnews\.com',
        r'.*reuters\.com',
        r'.*npr\.org',
        r'.*pbs\.org',
    ]
    if any(re.match(p, url) for p in reputable_patterns):
        return 'reputable'
    
    return 'unknown'
