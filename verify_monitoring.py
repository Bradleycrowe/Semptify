from Semptify import app
from security import get_metrics, get_latency_stats

# Simulate some requests
with app.test_client() as client:
    client.get('/health')
    client.get('/health')
    client.get('/metrics')

# Check metrics
metrics = get_metrics()
latencies = get_latency_stats()

print('Metrics Summary:')
print(f'  Requests Total: {metrics.get("requests_total", 0)}')
print(f'  Uptime: {metrics.get("uptime_seconds", 0)}s')
print()
print('Latency Stats:')
print(f'  P50: {latencies.get("p50_ms", 0):.2f}ms')
print(f'  P95: {latencies.get("p95_ms", 0):.2f}ms')
print(f'  P99: {latencies.get("p99_ms", 0):.2f}ms')
print(f'  Mean: {latencies.get("mean_ms", 0):.2f}ms')
print(f'  Max: {latencies.get("max_ms", 0):.2f}ms')
print(f'  Count: {latencies.get("count", 0)}')
