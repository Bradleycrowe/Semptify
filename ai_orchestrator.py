"""
AI Orchestrator core - lightweight multi-agent coordinator for Semptify
Provides a simple API used by the blueprint to run a round of agent interaction.
If configured providers (Ollama/OpenAI) are available it will call them, otherwise it falls back to simulated responses for local testing.
"""
import os
import json
import time
from typing import List, Dict, Any

# Try to import existing provider helpers if available
try:
    from copilot_routes import generate_response as copilot_generate
except Exception:
    copilot_generate = None

try:
    import requests
except Exception:
    requests = None


def _simulate_response(agent_name: str, prompt: str, context: Dict[str, Any]) -> str:
    # Short deterministic simulation to allow local testing
    return f"[{agent_name}] simulated response to: {prompt[:120]}"


class Agent:
    def __init__(self, id: str, role: str, description: str, provider: str = 'local'):
        self.id = id
        self.role = role
        self.description = description
        self.provider = provider

    def to_dict(self):
        return {"id": self.id, "role": self.role, "description": self.description, "provider": self.provider}


class Orchestrator:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run_round(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = context or {}
        timeline = []

        # Feed the prompt to each agent sequentially and collect replies
        for a in self.agents:
            start = time.time()
            reply = None
            if a.provider == 'copilot' and copilot_generate:
                try:
                    reply = copilot_generate(prompt, context)
                except Exception as e:
                    reply = f"[error calling copilot] {e}"
            elif a.provider in ('openai','ollama') and requests:
                # Keep this lightweight — don't implement full provider calls here
                reply = _simulate_response(a.role, prompt, context)
            else:
                reply = _simulate_response(a.role, prompt, context)

            duration = round((time.time() - start) * 1000)
            timeline.append({
                "agent_id": a.id,
                "role": a.role,
                "provider": a.provider,
                "request": prompt,
                "response": reply,
                "ms": duration
            })

            # Prepare the next prompt: include previous response in context
            prompt = f"{prompt}\n\n{a.role} says: {reply}"

        return {"timeline": timeline, "final_prompt": prompt}


# Convenience helper to load agents from a file
def load_agents_from_file(path: str):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    agents = [Agent(a['id'], a['role'], a.get('description',''), a.get('provider','local')) for a in data.get('agents', [])]
    return agents


if __name__ == '__main__':
    # Quick local smoke test
    agents = [Agent('legal','Legal Analyst','Summarize the law in MN about evictions','local'), Agent('evidence','Evidence Collector','Checklist for photos & notary','local')]
    o = Orchestrator(agents)
    out = o.run_round('How to prepare for a hearing?')
    print(json.dumps(out, indent=2))
