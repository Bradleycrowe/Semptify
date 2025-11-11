"""Quick test of simple reasoning engine"""

from reasoning_engine_simple import get_reasoning
import json

# Test different scenarios
reasoning = get_reasoning()

print("=" * 60)
print("TEST 1: New user with eviction issue")
print("=" * 60)
result1 = reasoning.get_cell_content(
    "user123",
    {"issue_type": "eviction"}
)
print("\nCELL A (Situation):")
print(json.dumps(result1["cell_a"], indent=2))
print("\nCELL B (Actions):")
print(json.dumps(result1["cell_b"], indent=2))

print("\n" + "=" * 60)
print("TEST 2: Rent dispute")
print("=" * 60)
result2 = reasoning.get_cell_content(
    "user456",
    {"issue_type": "rent"}
)
print("\nCELL A (Situation):")
print(json.dumps(result2["cell_a"], indent=2))
print("\nCELL B (Actions):")
print(json.dumps(result2["cell_b"], indent=2))

print("\n✅ Reasoning engine works! Ready for Render.")
