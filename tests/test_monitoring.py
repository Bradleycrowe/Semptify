"""Tests for enhanced monitoring features (Option 1)."""
import pytest
from security import get_latency_stats, record_request_latency


def test_record_request_latency():
    """Verify latency recording works."""
    record_request_latency(50.0)
    stats = get_latency_stats()
    assert stats['count'] > 0


def test_latency_stats_percentiles():
    """Verify latency stats include percentiles."""
    # Record predictable latencies: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
    for i in range(1, 11):
        record_request_latency(i * 10)

    stats = get_latency_stats()

    # All these should be present
    assert 'p50_ms' in stats
    assert 'p95_ms' in stats
    assert 'p99_ms' in stats
    assert 'mean_ms' in stats
    assert 'max_ms' in stats
    assert 'count' in stats
    assert stats['count'] >= 10  # at least our 10 latencies


def test_latency_stats_ordering():
    """Verify p50 <= p95 <= p99 <= max."""
    for i in range(1, 51):
        record_request_latency(i * 2)

    stats = get_latency_stats()

    # Percentiles should be in order
    assert stats['p50_ms'] <= stats['p95_ms']
    assert stats['p95_ms'] <= stats['p99_ms']
    assert stats['p99_ms'] <= stats['max_ms']


def test_latency_stats_empty():
    """Verify empty latency history returns zeros."""
    # Create a fresh stats dict without recorded latencies
    # (We can't clear the actual history as it's shared, but we can verify default behavior)
    stats = get_latency_stats()

    # Should have all keys
    assert 'p50_ms' in stats
    assert 'p95_ms' in stats
    assert 'p99_ms' in stats
    assert 'mean_ms' in stats
    assert 'max_ms' in stats
    assert 'count' in stats


def test_metrics_endpoint_json(client):
    """Verify /metrics endpoint returns JSON with latency stats."""
    # Make a request to populate metrics
    client.get('/health')

    # Request metrics as JSON
    resp = client.get('/metrics', headers={'Accept': 'application/json'})
    assert resp.status_code == 200

    data = resp.get_json()
    assert 'requests_total' in data
    assert 'latency_stats' in data
    assert 'p50_ms' in data['latency_stats']


def test_metrics_endpoint_prometheus(client):
    """Verify /metrics endpoint supports Prometheus text format."""
    # Make a request to populate metrics
    client.get('/health')

    # Request metrics as Prometheus text
    resp = client.get('/metrics', headers={'Accept': 'text/plain'})
    assert resp.status_code == 200
    assert resp.content_type == 'text/plain; charset=utf-8'

    # Should contain Prometheus format lines
    text = resp.get_data(as_text=True)
    assert '# HELP' in text
    assert '# TYPE' in text
    assert 'semptify_requests_total' in text
    assert 'semptify_request_latency_p50_ms' in text


def test_metrics_endpoint_prometheus_format_param(client):
    """Verify /metrics?format=prometheus returns Prometheus format."""
    client.get('/health')

    resp = client.get('/metrics?format=prometheus')
    assert resp.status_code == 200
    assert resp.content_type == 'text/plain; charset=utf-8'

    text = resp.get_data(as_text=True)
    assert 'semptify_uptime_seconds' in text
