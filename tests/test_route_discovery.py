"""
Tests for Route Discovery System
Validates automatic route discovery and data source integration
"""

import pytest
import json
import os
import tempfile
from datetime import datetime
from flask import Flask, jsonify

# Import route discovery modules
from route_discovery import RouteDiscovery, DataSourceRegistry, init_route_discovery
from route_discovery_bridge import IntegrationBridge, DiscoveredDataSource, LearningModuleDataSourceAdapter
from route_discovery_routes import init_route_discovery_api, route_discovery_bp


class TestRouteDiscovery:
    """Test route discovery functionality."""

    @pytest.fixture
    def app(self):
        """Create test Flask app."""
        app = Flask(__name__)
        app.config['TESTING'] = True

        # Register test routes
        @app.route('/api/learning/procedures', methods=['GET'])
        def procedures():
            return jsonify({"procedures": []})

        @app.route('/api/learning/forms', methods=['GET'])
        def forms():
            return jsonify({"forms": []})

        @app.route('/api/learning/fact-check', methods=['POST'])
        def fact_check():
            return jsonify({"result": True})

        @app.route('/admin/release', methods=['POST'])
        def release():
            return jsonify({"status": "ok"})

        @app.route('/health', methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        return app

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_route_discovery_initialization(self, app, temp_dir):
        """Test RouteDiscovery initialization."""
        discovery = RouteDiscovery(app, temp_dir)

        assert discovery.app is not None
        assert discovery.data_dir == temp_dir
        assert isinstance(discovery.discovered_routes, dict)
        assert isinstance(discovery.qualified_routes, list)

    def test_route_scanning(self, app, temp_dir):
        """Test scanning app for routes."""
        discovery = RouteDiscovery(app, temp_dir)
        results = discovery.scan_app()

        assert "informational" in results
        assert "operational" in results
        assert "system" in results

        # Should find at least 3 informational routes
        assert len(results["informational"]) >= 3

        # Should find at least 1 operational route
        assert len(results["operational"]) >= 1

        # Should find at least 1 system route
        assert len(results["system"]) >= 1

    def test_route_classification(self, app, temp_dir):
        """Test route classification logic."""
        discovery = RouteDiscovery(app, temp_dir)

        # Test informational route
        assert discovery._is_informational_route("/api/learning/procedures", "procedures") == True
        assert discovery._is_informational_route("/api/learning/forms", "forms") == True
        assert discovery._is_informational_route("/api/procedures", "procedures") == True

        # Test operational route
        assert discovery._is_operational_route("/admin/release", "release") == True
        assert discovery._is_operational_route("/api/upload", "upload") == True

        # Test system route
        assert discovery._is_informational_route("/health", "health") == False
        assert discovery._is_informational_route("/static/file.js", "static") == False

    def test_qualified_routes(self, app, temp_dir):
        """Test getting qualified routes."""
        discovery = RouteDiscovery(app, temp_dir)
        discovery.scan_app()

        qualified = discovery.get_qualified_routes()
        assert len(qualified) > 0

        # All qualified routes should be informational
        for route in qualified:
            assert route["qualified"] == True
            assert route["category"] == "informational"
            assert "/api/" in route["path"]

    def test_catalog_persistence(self, app, temp_dir):
        """Test saving and loading catalog."""
        discovery = RouteDiscovery(app, temp_dir)
        discovery.scan_app()
        discovery.save_catalog()

        # Verify catalog file exists
        catalog_file = os.path.join(temp_dir, "route_catalog.json")
        assert os.path.exists(catalog_file)

        # Load and verify
        with open(catalog_file, 'r') as f:
            catalog = json.load(f)

        assert "discovered_routes" in catalog
        assert "qualified_routes" in catalog
        assert "last_updated" in catalog
        assert catalog["total_qualified"] > 0


class TestDataSourceRegistry:
    """Test data source registry."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_registry_initialization(self, temp_dir):
        """Test registry initialization."""
        registry = DataSourceRegistry(temp_dir)

        assert registry.data_dir == temp_dir
        assert isinstance(registry.registry, dict)

    def test_register_source(self, temp_dir):
        """Test registering a source."""
        registry = DataSourceRegistry(temp_dir)

        source = {
            "source_id": "test_source",
            "name": "Test Source",
            "endpoint": "/api/test",
            "method": "GET",
            "category": "informational"
        }

        result = registry.register_source(source)
        assert result == True

        # Verify it was added
        sources = registry.get_all_sources()
        assert len(sources) == 1
        assert sources[0]["source_id"] == "test_source"

    def test_duplicate_registration(self, temp_dir):
        """Test that duplicate sources aren't registered twice."""
        registry = DataSourceRegistry(temp_dir)

        source = {
            "source_id": "test_source",
            "name": "Test Source",
            "endpoint": "/api/test",
            "method": "GET",
            "category": "informational"
        }

        result1 = registry.register_source(source)
        result2 = registry.register_source(source)

        assert result1 == True
        assert result2 == False  # Should not register duplicate

        sources = registry.get_all_sources()
        assert len(sources) == 1

    def test_bulk_registration(self, temp_dir):
        """Test registering multiple sources at once."""
        registry = DataSourceRegistry(temp_dir)

        sources = [
            {"source_id": f"source_{i}", "name": f"Source {i}", "endpoint": f"/api/test{i}", "method": "GET", "category": "informational"}
            for i in range(5)
        ]

        count = registry.register_bulk(sources)
        assert count == 5

        all_sources = registry.get_all_sources()
        assert len(all_sources) == 5

    def test_get_sources_by_category(self, temp_dir):
        """Test filtering sources by category."""
        registry = DataSourceRegistry(temp_dir)

        sources = [
            {"source_id": "proc_1", "name": "Procedures", "endpoint": "/api/procedures", "method": "GET", "category": "procedures"},
            {"source_id": "form_1", "name": "Forms", "endpoint": "/api/forms", "method": "GET", "category": "forms"},
            {"source_id": "proc_2", "name": "More Procedures", "endpoint": "/api/more-procedures", "method": "GET", "category": "procedures"},
        ]

        registry.register_bulk(sources)

        procedures = registry.get_sources_by_category("procedures")
        assert len(procedures) == 2

        forms = registry.get_sources_by_category("forms")
        assert len(forms) == 1


class TestIntegrationBridge:
    """Test integration bridge."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_bridge_initialization(self, temp_dir):
        """Test bridge initialization."""
        bridge = IntegrationBridge(temp_dir)

        assert bridge.data_dir == temp_dir
        assert isinstance(bridge.discovered_sources, dict)
        assert isinstance(bridge.integration_map, dict)

    def test_add_discovered_source(self, temp_dir):
        """Test adding discovered source to bridge."""
        bridge = IntegrationBridge(temp_dir)

        source_config = {
            "source_id": "test_source",
            "name": "Test Source",
            "endpoint": "/api/test",
            "method": "GET",
            "category": "informational"
        }

        result = bridge.add_discovered_source(source_config)
        assert result == True

        assert "test_source" in bridge.discovered_sources
        assert bridge.discovered_sources["test_source"].name == "Test Source"

    def test_get_sources_by_learning_category(self, temp_dir):
        """Test filtering by learning category."""
        bridge = IntegrationBridge(temp_dir)

        sources = [
            {"source_id": "proc_1", "name": "Procedures", "endpoint": "/api/learning/procedures", "method": "GET", "category": "informational"},
            {"source_id": "form_1", "name": "Forms", "endpoint": "/api/learning/forms", "method": "GET", "category": "informational"},
            {"source_id": "fact_1", "name": "Fact Check", "endpoint": "/api/learning/fact-check", "method": "GET", "category": "informational"},
        ]

        for source in sources:
            bridge.add_discovered_source(source)

        procedures = bridge.get_sources_by_learning_category("procedures")
        assert len(procedures) > 0

        forms = bridge.get_sources_by_learning_category("forms")
        assert len(forms) > 0

    def test_map_learning_category(self, temp_dir):
        """Test mapping learning category to sources."""
        bridge = IntegrationBridge(temp_dir)

        sources = [
            {"source_id": "proc_1", "name": "Procedures", "endpoint": "/api/learning/procedures/rental", "method": "GET", "category": "informational"},
            {"source_id": "proc_2", "name": "More Procedures", "endpoint": "/api/procedures/rental", "method": "GET", "category": "informational"},
        ]

        for source in sources:
            bridge.add_discovered_source(source)

        mapping = bridge.map_learning_category_to_sources(
            "rental_procedures",
            ["/api/learning/procedures/rental", "/api/procedures/rental"]
        )

        assert mapping["learning_category"] == "rental_procedures"
        assert len(mapping["source_ids"]) > 0
        assert "rental_procedures" in bridge.integration_map


class TestLearningModuleAdapter:
    """Test learning module adapter."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_adapter_initialization(self, temp_dir):
        """Test adapter initialization."""
        bridge = IntegrationBridge(temp_dir)
        adapter = LearningModuleDataSourceAdapter(bridge)

        assert adapter.bridge is not None
        assert isinstance(adapter.query_history, list)

    def test_get_data_sources_for_module(self, temp_dir):
        """Test getting sources for module."""
        bridge = IntegrationBridge(temp_dir)
        adapter = LearningModuleDataSourceAdapter(bridge)

        source_config = {
            "source_id": "learning_procedures",
            "name": "Procedures",
            "endpoint": "/api/learning/procedures",
            "method": "GET",
            "category": "informational"
        }
        bridge.add_discovered_source(source_config)

        sources = adapter.get_data_sources_for_module("preliminary_learning")

        assert sources["module"] == "preliminary_learning"
        assert "discovered_sources" in sources

    def test_query_statistics(self, temp_dir):
        """Test query statistics tracking."""
        bridge = IntegrationBridge(temp_dir)
        adapter = LearningModuleDataSourceAdapter(bridge)

        # Initially empty
        stats = adapter.get_query_statistics()
        assert stats.get("queries", 0) == 0

        # After a query
        adapter.query_history.append({
            "timestamp": datetime.now().isoformat(),
            "module": "test_module",
            "query": "test query",
            "results_found": 5
        })

        stats = adapter.get_query_statistics()
        assert stats["total_queries"] == 1


class TestRouteDiscoveryIntegration:
    """Integration tests."""

    @pytest.fixture
    def app_with_discovery(self):
        """Create app with route discovery initialized."""
        app = Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/api/learning/procedures', methods=['GET'])
        def procedures():
            return jsonify({"procedures": []})

        @app.route('/api/learning/forms', methods=['GET'])
        def forms():
            return jsonify({"forms": []})

        with tempfile.TemporaryDirectory() as tmpdir:
            discovery, registry = init_route_discovery(app, tmpdir)
            yield app, discovery, registry, tmpdir

    def test_full_discovery_flow(self, app_with_discovery):
        """Test complete discovery flow."""
        app, discovery, registry, tmpdir = app_with_discovery

        # Verify discovery
        assert len(discovery.qualified_routes) > 0

        # Verify registry
        sources = registry.get_all_sources()
        assert len(sources) > 0

        # Verify sources are registered
        for source in sources:
            assert "source_id" in source
            assert "endpoint" in source
            assert "category" in source

    def test_integration_with_bridge(self, app_with_discovery):
        """Test bridge integration with discovered sources."""
        app, discovery, registry, tmpdir = app_with_discovery

        bridge = IntegrationBridge(tmpdir)

        # Add discovered sources to bridge
        for source_config in registry.get_all_sources():
            bridge.add_discovered_source(source_config)

        # Verify bridge has sources
        assert len(bridge.discovered_sources) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
