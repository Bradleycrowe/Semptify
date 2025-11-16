"""
Legal conflict resolver for federal vs state vs local rules.
Implements a clear, explainable policy using the Supremacy Clause and preemption doctrines.
This is a guidance layer (not legal advice) and defaults are tuned for landlord-tenant.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class PreemptionAnalysis:
    domain: str
    model: str  # 'floor', 'ceiling', 'program_specific', 'unknown'
    rules: List[str]
    hierarchy: List[str]
    note: str

SUPREMACY_HIERARCHY = [
    'U.S. Constitution',
    'Federal statutes (validly enacted)',
    'Federal regulations (within authority)',
    'State constitutions & statutes',
    'State regulations',
    'Local ordinances',
    'Private contracts (leases)'
]

DEFAULT_RULES = [
    'Express preemption: If federal law explicitly preempts state law, federal controls.',
    'Field preemption: If Congress occupies the field, federal controls.',
    'Conflict (impossibility) preemption: If it is impossible to comply with both, federal controls.',
    'Obstacle preemption: If state law stands as an obstacle to federal purposes, federal controls.',
    'Savings clauses: If federal law preserves state law, state rules can coexist.',
]

# Post-2024 note: judicial deference to agencies has been curtailed; ensure the regulation is within statutory authority.

DOMAIN_DEFAULTS = {
    # Landlord-tenant is primarily state-law; federal often sets minimum protections
    'landlord_tenant': PreemptionAnalysis(
        domain='landlord_tenant',
        model='floor',
        rules=DEFAULT_RULES + [
            'In landlord-tenant matters, federal rules usually set a floor (minimum protections) rather than a ceiling.',
            'More-protective state/local laws typically stand unless expressly preempted or in conflict with federal programs.',
            'Program-specific housing (e.g., HUD/Section 8, VAWA) may include conditions that control in case of conflict.'
        ],
        hierarchy=SUPREMACY_HIERARCHY,
        note='Default heuristic for residential housing matters.'
    )
}


def analyze_preemption(state: str, domain: str, citations: List[Dict], federal_program: Optional[str] = None) -> Dict:
    analysis = DOMAIN_DEFAULTS.get(domain, PreemptionAnalysis(
        domain=domain,
        model='unknown',
        rules=DEFAULT_RULES,
        hierarchy=SUPREMACY_HIERARCHY,
        note='No domain-specific heuristic configured.'
    ))

    result = {
        'domain': analysis.domain,
        'model': analysis.model,
        'hierarchy': analysis.hierarchy,
        'rules': analysis.rules,
        'federal_program': federal_program,
        'applied_logic': []
    }

    # Heuristic application summary we can surface in UI/API
    if federal_program:
        result['applied_logic'].append('Program-specific rules may control where applicable.')
    if analysis.model == 'floor':
        result['applied_logic'].append('Prefer more-protective state/local rules unless there is express or conflict preemption.')
    elif analysis.model == 'ceiling':
        result['applied_logic'].append('Prefer federal baseline where state rules exceed federal ceilings.')

    return result
