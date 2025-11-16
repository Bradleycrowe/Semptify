"""
Enhanced Reasoning System with MN-specific knowledge
Validates and improves tenant rights recommendations
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class ReasoningSystem:
    def __init__(self):
        # MN-specific legal resources
        self.mn_resources = {
            'legal_aid': [
                {'name': 'Mid-Minnesota Legal Aid', 'phone': '1-800-292-4150', 'url': 'https://www.lawhelpmn.org'},
                {'name': 'HOME Line (Tenant Hotline)', 'phone': '866-866-3546', 'hours': 'M-F 1pm-4pm'},
                {'name': 'Legal Aid Service of MN', 'phone': '612-746-3751'}
            ],
            'court_costs': {
                'file_answer_eviction': 75,
                'small_claims_filing': 80,
                'appeal_filing': 285,
                'service_of_process': 75
            },
            'winter_protections': {
                'applies': 'October 1 - April 30',
                'cold_weather_rule': 'Heat must be 68°F, utilities cannot be shut off'
            }
        }
        
        # Expanded statute map with descriptions
        self.statute_map = {
            'holdover_tenancy': [
                {'num': '504B.141', 'title': 'Holding over after termination', 'type': 'rights'},
                {'num': '504B.135', 'title': 'Notice to terminate tenancy', 'type': 'procedure'}
            ],
            'security_deposit': [
                {'num': '504B.178', 'title': 'Deposit return requirements (21 days)', 'type': 'rights'}
            ],
            'eviction_defense': [
                {'num': '504B.285', 'title': 'Eviction grounds', 'type': 'defense'},
                {'num': '504B.335', 'title': 'Retaliation prohibition', 'type': 'defense'}
            ],
            'nonpayment': [
                {'num': '504B.291', 'title': 'Nonpayment notice requirements (14 days)', 'type': 'procedure'}
            ],
            'unlawful_lockout': [
                {'num': '504B.375', 'title': 'Utility shutoff prohibition', 'type': 'rights'},
                {'num': '609.605', 'title': 'Criminal lockout penalties', 'type': 'criminal'}
            ],
            'retaliation_defense': [
                {'num': '504B.441', 'title': 'Retaliatory eviction defense (90 days)', 'type': 'defense'}
            ]
        }

    def analyze(self, facts: Dict, stage: str) -> Dict:
        """Run complete 6-step reasoning chain with MN enhancements"""
        reasoning_chain = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'steps': []
        }

        # Step 1: Gather Facts
        step1 = self._gather_facts(facts)
        reasoning_chain['steps'].append(step1)
        
                # Step 2: Identify Issues
        step2 = self._identify_issues(stage, facts)
        reasoning_chain['steps'].append(step2)

        # Step 1.5: Jurisdiction Resolution
        step15 = self._resolve_jurisdiction(facts)
        reasoning_chain['steps'].append(step15)

        # Step 3: Determine Research Needs
        step3 = self._determine_research_needs(step2['issues'])
        reasoning_chain['steps'].append(step3)
        
        # Step 4: Assess Risks (with MN winter considerations)
        step4 = self._assess_risks(facts, step2['issues'])
        reasoning_chain['steps'].append(step4)
        
        # Step 5: Generate Options (with evidence and costs)
        step5 = self._generate_options(step2['issues'], step4, facts)
        reasoning_chain['steps'].append(step5)
        
        # Step 6: Recommend Action (with timeline and resources)
        step6 = self._recommend_action(step5['options'], step4, facts)
        reasoning_chain['steps'].append(step6)

        # Summary with confidence
        summary = {
            'primary_issue': step2['issues'][0] if step2['issues'] else 'unclear',
            'risk_level': step4['overall_risk'],
            'urgency': step4['urgency'],
            'recommended_action': step6['recommendation'],
            'confidence': self._calculate_confidence(step1['completeness'], step4['urgency'])
        }

        return {**reasoning_chain, 'summary': summary}

    def _gather_facts(self, facts: Dict) -> Dict:
        """Step 1: What do we know vs what's missing?"""
        critical_facts = ['lease_status', 'payment_current', 'notices_received', 
                         'landlord_communication', 'timeline']
        
        known = {k: v for k, v in facts.items() if k in critical_facts and v is not None}
        gaps = [f for f in critical_facts if f not in known or known.get(f) is None]
        completeness = len(known) / len(critical_facts)
        
        return {
            'step': 'fact_gathering',
            'known_facts': known,
            'fact_gaps': gaps,
            'completeness': completeness,
            'reasoning': f"We know {len(known)} of {len(critical_facts)} critical facts. Missing: {', '.join(gaps) if gaps else 'none'}"
        }

    def _identify_issues(self, stage: str, facts: Dict) -> Dict:
        """Step 2: What legal issues are present?"""
        issues = []
        
        # Stage-based detection
        if stage == 'ended_lease' and facts.get('still_in_unit'):
            issues.append('holdover_tenancy')
        
        if not facts.get('deposit_returned', True):
            issues.append('security_deposit')
        
        if facts.get('notices_received') in ['eviction_notice', 'eviction_summons']:
            issues.append('eviction_defense')
            
        if not facts.get('payment_current'):
            issues.append('nonpayment')
            
        if facts.get('landlord_communication') in ['threatening', 'lockout_threat']:
            issues.append('unlawful_lockout_risk')
            
        # Retaliation detection
        if facts.get('recent_complaint') and facts.get('notices_received'):
            issues.append('retaliation_defense')
        
        return {
            'step': 'issue_identification',
            'issues': issues,
            'reasoning': f"Based on stage '{stage}' and facts, identified {len(issues)} legal issues: {', '.join(issues)}"
        }

    def _determine_research_needs(self, issues: List[str]) -> Dict:
        """Step 3: Which MN statutes apply?"""
        statutes = []
        for issue in issues:
            if issue in self.statute_map:
                statutes.extend(self.statute_map[issue])
        
        # Deduplicate
        seen = set()
        unique_statutes = []
        for s in statutes:
            if s['num'] not in seen:
                seen.add(s['num'])
                unique_statutes.append(s)
        
        return {
            'step': 'legal_research',
            'statutes_needed': unique_statutes,
            'source': 'revisor.mn.gov/statutes/cite/',
            'reasoning': f"Need to research {len(unique_statutes)} MN statutes: {', '.join(s['num'] for s in unique_statutes)}"
        }

    def _assess_risks(self, facts: Dict, issues: List[str]) -> Dict:
        """Step 4: What are the risks and timeline? (MN-specific)"""
        risks = []
        urgency = 'normal'
        
        # Timeline-based urgency
        if facts.get('court_date'):
            days_until = self._calculate_days_until(facts['court_date'])
            if days_until <= 7:
                urgency = 'critical'
                risks.append(f"Court date in {days_until} days - must respond NOW")
            elif days_until <= 14:
                urgency = 'urgent'
                risks.append(f"Court date in {days_until} days - need to prepare")

        if facts.get('eviction_notice_date'):
            days_since = self._calculate_days_since(facts['eviction_notice_date'])
            if days_since < 7:
                urgency = 'urgent'
                risks.append("Eviction notice received - limited time to respond")

        # Issue-based risks
        if 'holdover_tenancy' in issues and not facts.get('paying_rent'):
            risks.append("Not paying rent during holdover = eviction risk")

        if 'unlawful_lockout_risk' in issues:
            risks.append("Landlord cannot lock you out without court order (MN 504B.375)")
        
        # MN winter protections
        if self._is_winter_months():
            risks.append("⚠ Winter eviction protections may apply (Oct 1 - Apr 30)")
        
        # Section 8 protections
        if facts.get('section_8') or facts.get('housing_voucher'):
            risks.append("Section 8 tenant - additional protections apply")

        # Overall risk level
        risk_level = 'low'
        if urgency in ['urgent', 'critical']:
            risk_level = 'high'
        elif len(risks) > 2:
            risk_level = 'medium'

        return {
            'step': 'risk_assessment',
            'risks': risks,
            'urgency': urgency,
            'overall_risk': risk_level,
            'winter_protections': self._is_winter_months(),
            'reasoning': f"Risk level: {risk_level}, Urgency: {urgency}. {len(risks)} risks identified."
        }

    def _generate_options(self, issues: List[str], risk_data: Dict, facts: Dict) -> Dict:
        """Step 5: What can they do? (with evidence and costs)"""
        options = []
        
        if 'holdover_tenancy' in issues:
            options.append({
                'option': 'Continue as month-to-month tenant',
                'basis': 'MN 504B.141 - automatic conversion',
                'requirements': 'Continue paying rent on time',
                'evidence_needed': [
                    'Rent receipts (last 3 months)',
                    'Copy of original lease',
                    'Written communication with landlord'
                ],
                'action_steps': [
                    'Continue paying rent (same amount, same day)',
                    'Send certified letter confirming intent to stay month-to-month',
                    'Document all payments and communications'
                ],
                'costs': '$5-10 for certified mail',
                'pros': ['Legal right to stay', 'Stable housing', 'No moving costs'],
                'cons': ['Either party can terminate with notice', 'Rent could increase'],
                'timeline': 'Immediate - continue current arrangement'
            })
            
            options.append({
                'option': 'Negotiate new lease',
                'basis': 'Voluntary agreement',
                'requirements': 'Landlord willing, terms agreeable',
                'evidence_needed': [
                    'Good payment history',
                    'Current rent receipts',
                    'References if requested'
                ],
                'action_steps': [
                    'Request meeting with landlord in writing',
                    'Propose lease terms (duration, rent amount)',
                    'Get everything in writing before signing'
                ],
                'costs': 'Possible application/admin fee',
                'pros': ['Longer-term stability', 'Locked-in rent', 'Better planning'],
                'cons': ['May include rent increase', 'Longer commitment'],
                'timeline': '2-4 weeks negotiation'
            })

        if 'security_deposit' in issues:
            options.append({
                'option': 'Demand deposit return',
                'basis': 'MN 504B.178 - landlord must return within 21 days',
                'requirements': 'Move-out date + 21 days passed',
                'evidence_needed': [
                    'Move-in condition report',
                    'Move-out photos',
                    'Cleaning receipts',
                    'Forwarding address proof'
                ],
                'action_steps': [
                    'Send certified letter demanding deposit + itemized statement',
                    'Allow 5 business days for response',
                    'File small claims if no response'
                ],
                'costs': f"${self.mn_resources['court_costs']['small_claims_filing']} small claims filing if needed",
                'pros': ['Get money back', 'Easy to file', 'No lawyer needed'],
                'cons': ['Takes time', 'Court date required', 'Landlord may counterclaim'],
                'timeline': '1-2 months if goes to court'
            })

        if 'eviction_defense' in issues:
            urgency_level = risk_data['urgency']
            options.append({
                'option': 'File court answer and defenses',
                'basis': 'MN 504B.285 - grounds for eviction, 504B.441 - retaliation defense',
                'requirements': f"Answer due before court date (urgency: {urgency_level})",
                'evidence_needed': [
                    'All notices received',
                    'Rent receipts showing payment history',
                    'Communications with landlord',
                    'Photos of unit condition',
                    'Repair requests (if retaliation)'
                ],
                'action_steps': [
                    'Get free legal help IMMEDIATELY (HOME Line: 866-866-3546)',
                    'File written answer with court before hearing',
                    'Bring all evidence to court',
                    'Request jury trial if available'
                ],
                'costs': f"${self.mn_resources['court_costs']['file_answer_eviction']} filing fee (may be waived if low income)",
                'pros': ['Protect your rights', 'Stay in unit during case', 'Possible dismissal'],
                'cons': ['Stressful', 'Time-consuming', 'May need to pay back rent'],
                'timeline': 'Court date typically 7-14 days from summons',
                'urgent': urgency_level in ['critical', 'urgent']
            })

        if not options:
            options.append({
                'option': 'Gather more information',
                'basis': 'Need clarity before action',
                'action_steps': [
                    'Review lease carefully',
                    'Document current situation',
                    'Call HOME Line for free advice: 866-866-3546'
                ],
                'costs': 'Free',
                'timeline': '1-2 days'
            })

        return {
            'step': 'option_generation',
            'options': options,
            'reasoning': f"Generated {len(options)} viable options based on issues and risks"
        }

    def _recommend_action(self, options: List[Dict], risk_data: Dict, facts: Dict) -> Dict:
        """Step 6: What should they do next? (prioritized with resources)"""
        urgency = risk_data['urgency']
        
        if urgency == 'critical':
            return {
                'step': 'recommendation',
                'recommendation': 'URGENT: Respond to court notice immediately',
                'priority': 'critical',
                'next_steps': [
                    'Call HOME Line NOW: 866-866-3546 (M-F 1-4pm)',
                    'File answer with court before deadline',
                    'Gather all evidence (receipts, notices, photos)',
                    'Contact legal aid TODAY: 1-800-292-4150'
                ],
                'resources': self.mn_resources['legal_aid'],
                'deadline': 'Court date - do not miss it!',
                'reasoning': 'Critical timeline requires immediate legal response'
            }
        
        if urgency == 'urgent':
            return {
                'step': 'recommendation',
                'recommendation': 'Act quickly to preserve your rights',
                'priority': 'urgent',
                'next_steps': [
                    'Call HOME Line for advice: 866-866-3546',
                    'Send certified letter responding to notice',
                    'Gather evidence now (don\'t wait)',
                    'Consider legal representation'
                ],
                'resources': self.mn_resources['legal_aid'],
                'timeline': 'Within 3-5 days',
                'reasoning': 'Time-sensitive situation requires prompt action'
            }
        
        # Normal priority - find best option
        if options and 'urgent' in options[0]:
            best_option = options[0]['option']
            next_steps = options[0].get('action_steps', [])
        elif options:
            best_option = options[0]['option']
            next_steps = options[0].get('action_steps', [
                'Continue paying rent to maintain rights',
                'Communicate with landlord in writing',
                'Document your situation'
            ])
        else:
            best_option = 'Need more information'
            next_steps = [
                'Review your lease',
                'Call HOME Line: 866-866-3546',
                'Document everything'
            ]

        return {
            'step': 'recommendation',
            'recommendation': f"Consider: {best_option}",
            'priority': 'normal',
            'next_steps': next_steps,
            'resources': self.mn_resources['legal_aid'],
            'reasoning': f"Based on your situation, {best_option.lower()} appears most viable"
        }

    def _calculate_days_until(self, date_str: str) -> int:
        """Calculate days until a future date"""
        try:
            target = datetime.strptime(date_str, '%Y-%m-%d')
            delta = target - datetime.now()
            return max(0, delta.days)
        except:
            return 999

    def _calculate_days_since(self, date_str: str) -> int:
        """Calculate days since a past date"""
        try:
            past = datetime.strptime(date_str, '%Y-%m-%d')
            delta = datetime.now() - past
            return max(0, delta.days)
        except:
            return 0

    def _is_winter_months(self) -> bool:
        """Check if current date falls in MN winter protection period (Oct 1 - Apr 30)"""
        month = datetime.now().month
        return month >= 10 or month <= 4

    def _calculate_confidence(self, completeness: float, urgency: str) -> float:
        """Calculate confidence based on fact completeness and urgency"""
        base = completeness
        if urgency == 'critical':
            return max(0.6, base)  # Lower confidence in crisis
        elif urgency == 'urgent':
            return max(0.7, base)
        else:
            return min(0.95, base + 0.1)  # Higher confidence when not rushed

    def _resolve_jurisdiction(self, facts: Dict) -> Dict:
        """Step 1.5: Resolve jurisdiction assumption and confirmation."""
        cand = facts.get('jurisdiction_candidate')
        conf = float(facts.get('jurisdiction_confidence') or 0.0)
        confirmed = bool(facts.get('jurisdiction_confirmed'))
        sources = facts.get('jurisdiction_sources') or []
        if confirmed and cand:
            chosen = cand
            reason = f"Using confirmed jurisdiction {cand}"
        elif cand:
            chosen = 'MN'  # Phase 1: default to MN until user confirms
            why = ', '.join([f"{s.get('type')}={s.get('value')}" for s in sources]) or 'unknown signals'
            reason = f"Candidate {cand} (confidence {conf}); defaulting to MN until confirmed (sources: {why})"
        else:
            chosen = 'MN'
            reason = 'No candidate jurisdiction found; defaulting to MN'
        return {
            'step': 'jurisdiction_resolution',
            'jurisdiction': chosen,
            'candidate': cand,
            'confirmed': confirmed,
            'confidence': conf,
            'sources': sources,
            'reasoning': reason
        }
# Test if run directly
if __name__ == '__main__':
    reasoner = ReasoningSystem()
    
    test_facts = {
        'lease_status': 'ended',
        'still_in_unit': True,
        'payment_current': True,
        'paying_rent': True,
        'notices_received': None,
        'landlord_communication': 'accepting rent',
        'deposit_returned': False,
        'timeline': '2 weeks since lease end'
    }
    
    result = reasoner.analyze(test_facts, 'ended_lease')
    
    print('\n=== REASONING TEST ===\n')
    print(f'Stage: {result["stage"]}\n')
    print('Steps:\n')
    
    for step in result['steps']:
        step_name = step['step'].replace('_', ' ').upper()
        reasoning = step.get('reasoning', step.get('recommendation', ''))
        print(f'{step_name}:')
        print(f'  {reasoning}\n')
    
    print('=== SUMMARY ===')
    print(f"Primary Issue: {result['summary']['primary_issue']}")
    print(f"Risk Level: {result['summary']['risk_level']}")
    print(f"Urgency: {result['summary']['urgency']}")
    print(f"Recommendation: {result['summary']['recommended_action']}")
    print(f"Confidence: {int(result['summary']['confidence']*100)}%")




