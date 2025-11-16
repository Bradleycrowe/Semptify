"""
Improvement Engine
Evaluates emerging technologies (storage, runtimes, languages) and proposes safe migration plans.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import random
import json

@dataclass
class TechOption:
    category: str            # e.g. storage, runtime, language
    name: str                # e.g. Cloudflare R2, AWS S3, Rust, PyPy
    maturity: str            # experimental | beta | stable | enterprise
    perf_score: float        # relative (0-100)
    cost_score: float        # lower is cheaper (0-100)
    reliability_score: float # uptime & data durability
    migration_effort: int    # estimated hours
    ecosystem_score: float   # community/tooling richness
    notes: str               # summary

    def composite(self) -> float:
        # Weighted composite scoring
        return round(
            self.perf_score * 0.35 +
            (100 - self.cost_score) * 0.15 +
            self.reliability_score * 0.25 +
            (100 - self.migration_effort) * 0.10 +
            self.ecosystem_score * 0.15,
            2
        )

@dataclass
class MigrationPlan:
    id: str
    created_at: str
    target: TechOption
    rationale: List[str]
    risk_assessment: Dict[str, Any]
    steps: List[Dict[str, Any]]
    simulated_benefits: Dict[str, Any]
    approval_required: bool = True
    approved: bool = False

class ImprovementEngine:
    """Core driver for technology improvement suggestions."""

    def __init__(self):
        self.baseline_metrics: Dict[str, Any] = {}
        self.discovered: List[TechOption] = []
        self.proposals: List[MigrationPlan] = []

    # 1. Collect current metrics -------------------------------------------------
    def collect_metrics(self) -> Dict[str, Any]:
        # In real system: query Prometheus, logs, storage timings.
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'storage_latency_ms': random.randint(30, 120),
            'request_throughput_rps': random.randint(120, 500),
            'error_rate_pct': round(random.uniform(0.2, 2.5), 2),
            'cpu_load_pct': round(random.uniform(18, 67), 2),
            'memory_usage_mb': random.randint(350, 950),
            'language_hotspots': ['python:io', 'python:json', 'pdf_generation']
        }
        self.baseline_metrics = metrics
        return metrics

    # 2. Discover candidate technologies ---------------------------------------
    def discover_options(self) -> List[TechOption]:
        # Normally: external feeds, curated list, vendor APIs.
        catalog = [
            TechOption('storage','Cloudflare R2','stable',85,20,92,8,70,'Low-cost S3-compatible object store'),
            TechOption('storage','AWS S3','enterprise',78,35,99,6,95,'Industry standard object storage'),
            TechOption('language','Rust microservice','stable',90,25,97,24,80,'High performance compiled service'),
            TechOption('language','PyPy','stable',65,15,90,6,60,'Faster Python runtime for dynamic code'),
            TechOption('runtime','Serverless Workers','beta',82,30,94,14,75,'Edge execution reduce latency'),
            TechOption('runtime','Local Ollama optimized','beta',60,10,85,10,55,'Fast local model inference'),
            TechOption('future','Quantum Simulation Layer','experimental',40,60,50,120,25,'Placeholder for post-quantum workflow acceleration')
        ]
        self.discovered = catalog
        return catalog

    # 3. Evaluate options vs baseline -----------------------------------------
    def evaluate_options(self) -> List[Dict[str, Any]]:
        evaluations = []
        for opt in self.discovered:
            score = opt.composite()
            benefit_latency = self._estimate_latency_improvement(opt)
            evaluations.append({
                'name': opt.name,
                'category': opt.category,
                'maturity': opt.maturity,
                'composite_score': score,
                'estimated_latency_improvement_pct': benefit_latency,
                'migration_effort_hours': opt.migration_effort,
                'recommended': score > 75 and benefit_latency > 10 and opt.maturity != 'experimental'
            })
        evaluations.sort(key=lambda e: e['composite_score'], reverse=True)
        return evaluations

    def _estimate_latency_improvement(self, opt: TechOption) -> float:
        base = self.baseline_metrics.get('storage_latency_ms', 100)
        if opt.category == 'storage':
            # Pretend perf_score correlates linearly to latency reduction
            improvement = max(0, (opt.perf_score - 70) * 0.9)
            return round(improvement, 2)
        if opt.category == 'runtime':
            return round((opt.perf_score - 65) * 0.7, 2)
        if opt.category == 'language':
            return round((opt.perf_score - 60) * 0.5, 2)
        return 0.0

    # 4. Build migration plan --------------------------------------------------
    def build_plan(self, target_name: str) -> MigrationPlan | None:
        match = next((o for o in self.discovered if o.name == target_name), None)
        if not match:
            return None
        rationale = [
            f"Composite score {match.composite()} exceeds threshold",
            f"Maturity level: {match.maturity}",
            "Projected latency improvement positive",
        ]
        risks = {
            'data_loss_risk': 'low' if match.reliability_score > 90 else 'medium',
            'vendor_lock_in': 'medium' if 'AWS' in match.name else 'low',
            'migration_complexity': match.migration_effort,
            'rollback_strategy': 'Maintain dual-write until integrity verified'
        }
        steps = [
            {'order':1,'title':'Establish sandbox environment','detail':'Provision isolated test namespace.'},
            {'order':2,'title':'Replicate representative dataset','detail':'Copy anonymized subset for benchmarking.'},
            {'order':3,'title':'Run latency & error benchmarks','detail':'Compare p50/p95 vs baseline.'},
            {'order':4,'title':'Dual-write activation','detail':'Write to old and new storage in parallel.'},
            {'order':5,'title':'Integrity verification','detail':'Cross-check object counts + hashes.'},
            {'order':6,'title':'Cutover & monitor','detail':'Switch read path; keep fallback for 24h.'}
        ]
        simulated = self.simulate_migration(match)
        plan = MigrationPlan(
            id=f"plan_{match.name.lower().replace(' ','_')}_{int(datetime.utcnow().timestamp())}",
            created_at=datetime.utcnow().isoformat(),
            target=match,
            rationale=rationale,
            risk_assessment=risks,
            steps=steps,
            simulated_benefits=simulated,
            approval_required=True,
            approved=False
        )
        self.proposals.append(plan)
        return plan

    # 5. Simulate migration benefits -----------------------------------------
    def simulate_migration(self, target: TechOption) -> Dict[str, Any]:
        baseline_latency = self.baseline_metrics.get('storage_latency_ms', 100)
        projected_latency = round(baseline_latency * (1 - min(0.5, target.perf_score/200)), 2)
        error_rate = self.baseline_metrics.get('error_rate_pct', 1.0)
        projected_error_rate = round(max(0.1, error_rate * (1 - target.reliability_score/400)), 2)
        return {
            'baseline_latency_ms': baseline_latency,
            'projected_latency_ms': projected_latency,
            'latency_delta_ms': baseline_latency - projected_latency,
            'baseline_error_rate_pct': error_rate,
            'projected_error_rate_pct': projected_error_rate,
            'confidence': 'medium' if target.maturity in ['beta','stable'] else 'low'
        }

    # 6. Propose changes (summary) --------------------------------------------
    def propose_changes(self) -> List[Dict[str, Any]]:
        return [
            {
                'plan_id': p.id,
                'target': p.target.name,
                'category': p.target.category,
                'composite': p.target.composite(),
                'latency_gain_ms': p.simulated_benefits['latency_delta_ms'],
                'requires_approval': p.approval_required,
                'approved': p.approved
            } for p in self.proposals
        ]

    # 7. Apply migration (requires approval) ----------------------------------
    def apply_migration(self, plan_id: str, approved: bool) -> Dict[str, Any]:
        plan = next((p for p in self.proposals if p.id == plan_id), None)
        if not plan:
            return {'status':'error','message':'Plan not found'}
        if not approved:
            return {'status':'denied','message':'Approval required to proceed'}
        plan.approved = True
        # Stub: In reality perform steps; here we just mark applied.
        return {
            'status':'applied',
            'target': plan.target.name,
            'steps_executed': [s['title'] for s in plan.steps],
            'monitoring_window_hours': 24
        }

# Singleton accessor
_instance: ImprovementEngine | None = None

def get_improvement_engine() -> ImprovementEngine:
    global _instance
    if _instance is None:
        _instance = ImprovementEngine()
    return _instance
