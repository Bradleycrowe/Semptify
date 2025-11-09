"""
Route Discovery & Dynamic Data Source Flask Endpoints
Exposes route discovery and integration capabilities via API
"""

from flask import Blueprint, jsonify, request, current_app
from typing import Dict, Optional
import logging
from datetime import datetime

# Import discovery modules
try:
    from route_discovery import RouteDiscovery, DataSourceRegistry, init_route_discovery
    from route_discovery_bridge import IntegrationBridge, LearningModuleDataSourceAdapter
except ImportError:
    RouteDiscovery = None
    DataSourceRegistry = None
    IntegrationBridge = None
    LearningModuleDataSourceAdapter = None

logger = logging.getLogger(__name__)

route_discovery_bp = Blueprint('route_discovery', __name__, url_prefix='/api/discovery')

# Global instances (initialized on app startup)
_discovery_instance = None
_registry_instance = None
_bridge_instance = None
_adapter_instance = None


def init_route_discovery_api(app, data_dir: str = "data"):
    """Initialize route discovery API."""
    global _discovery_instance, _registry_instance, _bridge_instance, _adapter_instance

    if RouteDiscovery is None:
        logger.error("Route discovery module not available")
        return

    try:
        # Initialize discovery and registry
        _discovery_instance, _registry_instance = init_route_discovery(app, data_dir)

        # Initialize bridge
        _bridge_instance = IntegrationBridge(data_dir, app.test_client())

        # Add discovered sources to bridge
        for source_config in _registry_instance.get_all_sources():
            _bridge_instance.add_discovered_source(source_config)

        # Initialize adapter
        _adapter_instance = LearningModuleDataSourceAdapter(_bridge_instance)

        logger.info("✓ Route discovery API initialized")
        logger.info(f"  - Discovery: {len(_discovery_instance.discovered_routes)} routes scanned")
        logger.info(f"  - Registry: {len(_registry_instance.get_all_sources())} sources registered")
        logger.info(f"  - Bridge: {len(_bridge_instance.discovered_sources)} sources loaded")

    except Exception as e:
        logger.error(f"Error initializing route discovery API: {e}")


# ============================================================================
# Discovery Endpoints
# ============================================================================

@route_discovery_bp.route('/scan', methods=['POST'])
def scan_routes():
    """
    Scan Flask app for all routes.
    Classify as informational, operational, or system.

    Returns:
        JSON with classification results
    """
    if not _discovery_instance:
        return jsonify({"error": "Discovery not initialized"}), 503

    try:
        results = _discovery_instance.scan_app()

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "scanned_routes": len(_discovery_instance.discovered_routes),
            "qualified_informational": len(_discovery_instance.qualified_routes),
            "classification": {
                "informational": len(results.get("informational", [])),
                "operational": len(results.get("operational", [])),
                "system": len(results.get("system", []))
            },
            "routes": {
                "informational": [r["path"] for r in results.get("informational", [])],
                "operational": [r["path"] for r in results.get("operational", [])],
                "system": [r["path"] for r in results.get("system", [])][:10]  # Limit system routes
            }
        }), 200

    except Exception as e:
        logger.error(f"Error scanning routes: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/qualified-routes', methods=['GET'])
def get_qualified_routes():
    """
    Get all qualified informational routes.

    Returns:
        JSON list of qualified routes
    """
    if not _discovery_instance:
        return jsonify({"error": "Discovery not initialized"}), 503

    try:
        routes = _discovery_instance.get_qualified_routes()

        return jsonify({
            "status": "success",
            "count": len(routes),
            "routes": routes
        }), 200

    except Exception as e:
        logger.error(f"Error getting qualified routes: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/routes-by-category/<category>', methods=['GET'])
def get_routes_by_category(category: str):
    """
    Get qualified routes by category.

    Categories:
        - procedures
        - forms
        - timeline
        - agencies
        - resources
        - etc.

    Returns:
        JSON list of routes matching category
    """
    if not _discovery_instance:
        return jsonify({"error": "Discovery not initialized"}), 503

    try:
        category_dict = _discovery_instance.get_route_by_category(category)

        return jsonify({
            "status": "success",
            "category": category,
            "count": len(category_dict.get(category, [])),
            "routes": category_dict.get(category, [])
        }), 200

    except Exception as e:
        logger.error(f"Error getting routes by category: {e}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# Data Source Registry Endpoints
# ============================================================================

@route_discovery_bp.route('/register-sources', methods=['POST'])
def register_sources():
    """
    Register discovered routes as data sources.
    Called after route scanning to add qualified routes to registry.

    Returns:
        JSON with registration results
    """
    if not _discovery_instance or not _registry_instance:
        return jsonify({"error": "Discovery not initialized"}), 503

    try:
        # Generate integration config from discovered routes
        config = _discovery_instance.register_routes_as_datasources()

        # Register all sources
        count = _registry_instance.register_bulk(config.get("data_sources", []))

        # Add to bridge
        for source_config in config.get("data_sources", []):
            _bridge_instance.add_discovered_source(source_config)

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "sources_registered": count,
            "data_sources": config.get("data_sources", [])
        }), 200

    except Exception as e:
        logger.error(f"Error registering sources: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/registry', methods=['GET'])
def get_registry():
    """
    Get complete data source registry.

    Returns:
        JSON with all registered data sources and metadata
    """
    if not _registry_instance:
        return jsonify({"error": "Registry not initialized"}), 503

    try:
        summary = _registry_instance.get_registry_summary()

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "total_sources": summary.get("total_sources"),
            "by_category": summary.get("sources_by_category"),
            "sources": summary.get("sources")
        }), 200

    except Exception as e:
        logger.error(f"Error getting registry: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/registry/by-category/<category>', methods=['GET'])
def get_registry_by_category(category: str):
    """
    Get data sources by category from registry.

    Returns:
        JSON list of sources in category
    """
    if not _registry_instance:
        return jsonify({"error": "Registry not initialized"}), 503

    try:
        sources = _registry_instance.get_sources_by_category(category)

        return jsonify({
            "status": "success",
            "category": category,
            "count": len(sources),
            "sources": sources
        }), 200

    except Exception as e:
        logger.error(f"Error getting registry by category: {e}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# Integration Bridge Endpoints
# ============================================================================

@route_discovery_bp.route('/sources-for-learning/<module_name>', methods=['GET'])
def get_sources_for_learning_module(module_name: str):
    """
    Get all discovered data sources available for a learning module.

    Learning modules can use this to discover what data sources are available.

    Args:
        module_name: Name of learning module (e.g., 'procedures', 'forms')

    Returns:
        JSON list of data sources relevant to module
    """
    if not _bridge_instance:
        return jsonify({"error": "Bridge not initialized"}), 503

    try:
        sources = _bridge_instance.get_learning_module_datasources(module_name)

        return jsonify({
            "status": "success",
            "module": module_name,
            "timestamp": datetime.now().isoformat(),
            "sources_count": len(sources),
            "sources": sources
        }), 200

    except Exception as e:
        logger.error(f"Error getting sources for module: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/query-sources', methods=['POST'])
def query_all_sources():
    """
    Query all discovered data sources.

    Request body:
        {
            "query": "information to search for",
            "learning_category": "optional category filter"
        }

    Returns:
        JSON with aggregated results from all sources
    """
    if not _bridge_instance:
        return jsonify({"error": "Bridge not initialized"}), 503

    try:
        data = request.get_json() or {}
        query = data.get("query", "")
        category = data.get("learning_category")

        if not query:
            return jsonify({"error": "query parameter required"}), 400

        results = _bridge_instance.query_all_sources(query, category)

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            **results
        }), 200

    except Exception as e:
        logger.error(f"Error querying sources: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/map-category', methods=['POST'])
def map_learning_category():
    """
    Create mapping from learning category to data sources.

    Request body:
        {
            "learning_category": "rental_procedures",
            "endpoint_patterns": ["/api/learning/procedures/rental"]
        }

    Returns:
        JSON with mapping configuration
    """
    if not _bridge_instance:
        return jsonify({"error": "Bridge not initialized"}), 503

    try:
        data = request.get_json() or {}
        category = data.get("learning_category")
        patterns = data.get("endpoint_patterns", [])

        if not category or not patterns:
            return jsonify({"error": "learning_category and endpoint_patterns required"}), 400

        mapping = _bridge_instance.map_learning_category_to_sources(category, patterns)

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "mapping": mapping
        }), 200

    except Exception as e:
        logger.error(f"Error mapping category: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/integration-status', methods=['GET'])
def get_integration_status():
    """
    Get complete integration status.

    Returns:
        JSON with:
        - Number of discovered sources
        - Integration mappings
        - Query statistics
    """
    if not _bridge_instance or not _adapter_instance:
        return jsonify({"error": "Bridge not initialized"}), 503

    try:
        status = _bridge_instance.get_integration_status()
        stats = _adapter_instance.get_query_statistics()

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "integration": status,
            "query_statistics": stats
        }), 200

    except Exception as e:
        logger.error(f"Error getting integration status: {e}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# Learning Module Integration Endpoints
# ============================================================================

@route_discovery_bp.route('/learning-module-sources/<module_name>', methods=['GET'])
def get_learning_module_sources(module_name: str):
    """
    Get data sources available to a learning module (via adapter).

    This endpoint is used by learning modules to discover what data sources
    they should use when querying for information.

    Args:
        module_name: Name of learning module

    Returns:
        JSON with discovered and built-in data sources for module
    """
    if not _adapter_instance:
        return jsonify({"error": "Adapter not initialized"}), 503

    try:
        sources = _adapter_instance.get_data_sources_for_module(module_name)

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            **sources
        }), 200

    except Exception as e:
        logger.error(f"Error getting learning module sources: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/learning-module-query', methods=['POST'])
def query_via_learning_module():
    """
    Query data sources via learning module adapter.

    This endpoint shows how learning modules should query discovered sources
    in addition to their built-in knowledge base.

    Request body:
        {
            "module": "preliminary_learning",
            "query": "information to search for",
            "category": "optional category"
        }

    Returns:
        JSON with results from both discovered and built-in sources
    """
    if not _adapter_instance:
        return jsonify({"error": "Adapter not initialized"}), 503

    try:
        data = request.get_json() or {}
        module = data.get("module", "")
        query = data.get("query", "")
        category = data.get("category")

        if not module or not query:
            return jsonify({"error": "module and query parameters required"}), 400

        result = _adapter_instance.query_data_sources(module, query, category)

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            **result
        }), 200

    except Exception as e:
        logger.error(f"Error querying via learning module: {e}")
        return jsonify({"error": str(e)}), 500


@route_discovery_bp.route('/query-statistics', methods=['GET'])
def get_query_statistics():
    """
    Get statistics about queries to discovered data sources.

    Returns:
        JSON with:
        - Total queries made
        - Modules using discovered sources
        - Recent queries
    """
    if not _adapter_instance:
        return jsonify({"error": "Adapter not initialized"}), 503

    try:
        stats = _adapter_instance.get_query_statistics()

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        }), 200

    except Exception as e:
        logger.error(f"Error getting query statistics: {e}")
        return jsonify({"error": str(e)}), 500
