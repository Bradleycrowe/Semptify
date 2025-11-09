"""
Route Discovery & Dynamic Data Source Integration
Allows Semptify to automatically discover and wire in information routes
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RouteDiscovery:
    """
    Discovers informational routes and integrates them as data sources.
    Scans Flask app for routes that provide information/knowledge.
    """

    def __init__(self, app=None, data_dir: str = "data"):
        self.app = app
        self.data_dir = data_dir
        self.discovered_routes = {}
        self.qualified_routes = []
        self.integration_log = []
        self.catalog_file = os.path.join(data_dir, "route_catalog.json")
        self.load_catalog()

    def load_catalog(self):
        """Load previously discovered routes."""
        if os.path.exists(self.catalog_file):
            try:
                with open(self.catalog_file, 'r') as f:
                    data = json.load(f)
                    self.discovered_routes = data.get("discovered_routes", {})
                    self.qualified_routes = data.get("qualified_routes", [])
            except:
                pass

    def save_catalog(self):
        """Save route catalog for future reference."""
        os.makedirs(self.data_dir, exist_ok=True)
        catalog = {
            "discovered_routes": self.discovered_routes,
            "qualified_routes": self.qualified_routes,
            "last_updated": datetime.now().isoformat(),
            "total_qualified": len(self.qualified_routes)
        }
        with open(self.catalog_file, 'w') as f:
            json.dump(catalog, f, indent=2)
        logger.info(f"Saved route catalog: {len(self.qualified_routes)} qualified routes")

    def scan_app(self):
        """
        Scan Flask app for all routes.
        Classify them as informational, operational, or system.
        """
        if not self.app:
            logger.error("No Flask app provided")
            return

        logger.info("Scanning Flask app for routes...")

        route_types = {
            "informational": [],
            "operational": [],
            "system": []
        }

        for rule in self.app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue

            route_path = str(rule)
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})

            route_info = {
                "path": route_path,
                "endpoint": rule.endpoint,
                "methods": methods,
                "qualified": False,
                "category": None
            }

            # Classify route
            if self._is_informational_route(route_path, rule.endpoint):
                route_type = "informational"
                route_info["qualified"] = True
                route_info["category"] = "informational"
            elif self._is_operational_route(route_path, rule.endpoint):
                route_type = "operational"
                route_info["category"] = "operational"
            else:
                route_type = "system"
                route_info["category"] = "system"

            route_types[route_type].append(route_info)
            self.discovered_routes[route_path] = route_info

        # Log results
        for route_type, routes in route_types.items():
            logger.info(f"  {route_type}: {len(routes)} routes")
            for route in routes[:3]:  # Show first 3
                logger.info(f"    - {route['path']}")

        # Qualify informational routes
        self.qualified_routes = [r for r in self.discovered_routes.values() if r.get("qualified")]
        logger.info(f"\n✓ Found {len(self.qualified_routes)} qualified informational routes")

        self.save_catalog()
        return route_types

    def _is_informational_route(self, path: str, endpoint: str) -> bool:
        """
        Determine if route provides information/knowledge.

        Informational keywords:
        - /api/learning/*
        - /api/procedures/*
        - /api/forms/*
        - /api/timeline/*
        - /api/agencies/*
        - /api/fact-check/*
        - /api/resources/*
        - /api/references/*
        - /api/guides/*
        - /api/requirements/*
        """
        informational_keywords = [
            "/api/learning",
            "/api/procedures",
            "/api/forms",
            "/api/timeline",
            "/api/agencies",
            "/api/fact-check",
            "/api/resources",
            "/api/references",
            "/api/guides",
            "/api/requirements",
            "/api/knowledge",
            "/api/information",
            "/api/data/",
            "/api/check",
            "/api/verify",
            "/api/lookup"
        ]

        path_lower = str(path).lower()

        # Check for informational keywords
        for keyword in informational_keywords:
            if keyword in path_lower:
                return True

        # Check for GET-only endpoints (typically informational)
        if "GET" in str(path) and "POST" not in str(path) and "DELETE" not in str(path):
            if "/api/" in path and any(x in path for x in [
                "get", "list", "find", "search", "query", "info", "data", "show"
            ]):
                return True

        return False

    def _is_operational_route(self, path: str, endpoint: str) -> bool:
        """
        Determine if route performs operations (create, update, delete).

        Operational keywords:
        - POST /api/* (create)
        - PUT /api/* (update)
        - DELETE /api/* (delete)
        - PATCH /api/*
        - /admin/*
        - /upload
        - /submit
        """
        operational_keywords = [
            "/admin",
            "/submit",
            "/upload",
            "/create",
            "/update",
            "/delete",
            "/save",
            "/process"
        ]

        path_lower = str(path).lower()
        methods_str = str(path)

        # Check for POST/PUT/DELETE
        if any(method in methods_str for method in ["POST", "PUT", "DELETE", "PATCH"]):
            if "/api/" in path:
                return True

        # Check for operational keywords
        for keyword in operational_keywords:
            if keyword in path_lower:
                return True

        return False

    def get_qualified_routes(self) -> List[Dict]:
        """Get all qualified informational routes."""
        return self.qualified_routes

    def get_route_by_category(self, category: str) -> List[Dict]:
        """Get routes by information category."""
        # Parse category from route paths
        routes_by_category = {}

        for route_info in self.qualified_routes:
            path = route_info["path"]

            # Extract category from path
            # /api/learning/procedures -> "procedures"
            # /api/learning/forms -> "forms"
            parts = path.split("/")

            if len(parts) > 3:
                cat = parts[3]  # After /api/learning/
            else:
                cat = "other"

            if cat not in routes_by_category:
                routes_by_category[cat] = []

            routes_by_category[cat].append(route_info)

        return routes_by_category.get(category, [])

    def test_route(self, client, route_path: str, method: str = "GET") -> Tuple[bool, str, Optional[Dict]]:
        """
        Test if a route is working and returns valid data.

        Returns: (is_working, description, sample_data)
        """
        try:
            if method == "GET":
                response = client.get(route_path)
            elif method == "POST":
                response = client.post(route_path, json={})
            else:
                return False, f"Unsupported method {method}", None

            if response.status_code == 200:
                try:
                    data = response.get_json()
                    if data:
                        return True, "Working", data
                    else:
                        return True, "Working (empty response)", {}
                except:
                    return True, "Working (non-JSON)", None

            else:
                return False, f"HTTP {response.status_code}", None

        except Exception as e:
            return False, str(e), None

    def validate_route_for_integration(self, route_info: Dict) -> Tuple[bool, str]:
        """
        Validate if route meets integration criteria.

        Criteria:
        - Must be GET endpoint
        - Must return JSON
        - Must have /api/ prefix
        - Must return data structure
        """
        path = route_info.get("path", "")
        methods = route_info.get("methods", "")

        # Must be GET
        if "GET" not in methods:
            return False, "Not a GET endpoint"

        # Must have /api/ prefix
        if "/api/" not in path:
            return False, "Missing /api/ prefix"

        # Must not have path parameters (for now)
        if "<" in path and ">" in path:
            # Routes with parameters need special handling
            # But we'll mark them as qualified
            pass

        return True, "Valid for integration"

    def generate_integration_config(self) -> Dict:
        """
        Generate configuration for integrating qualified routes as data sources.

        Output format:
        {
            "data_sources": [
                {
                    "source_id": "learning_procedures",
                    "name": "Legal Procedures",
                    "endpoint": "/api/learning/procedures",
                    "method": "GET",
                    "category": "informational",
                    "qualified": true
                }
            ]
        }
        """
        data_sources = []

        for route_info in self.qualified_routes:
            source = {
                "source_id": route_info["endpoint"].replace("/", "_").lower(),
                "name": self._generate_friendly_name(route_info["endpoint"]),
                "endpoint": route_info["path"],
                "method": "GET",  # Informational routes are typically GET
                "category": route_info.get("category", "informational"),
                "qualified": route_info.get("qualified", False),
                "added_at": datetime.now().isoformat()
            }
            data_sources.append(source)

        return {
            "data_sources": data_sources,
            "total_sources": len(data_sources),
            "generated_at": datetime.now().isoformat()
        }

    def _generate_friendly_name(self, endpoint: str) -> str:
        """Generate friendly name from endpoint."""
        # /api/learning/procedures -> "Learning Procedures"
        parts = endpoint.split("/")
        if len(parts) > 2:
            name_parts = parts[2:]  # Skip /api
            name = " ".join(name_parts)
            return name.title()
        return endpoint

    def register_routes_as_datasources(self) -> Dict:
        """
        Register qualified routes as data sources.
        Makes them available to learning modules.
        """
        config = self.generate_integration_config()

        integration_log_entry = {
            "timestamp": datetime.now().isoformat(),
            "routes_registered": len(config["data_sources"]),
            "sources": config["data_sources"]
        }

        self.integration_log.append(integration_log_entry)
        logger.info(f"Registered {len(config['data_sources'])} routes as data sources")

        # Save integration log
        log_file = os.path.join(self.data_dir, "route_integration_log.json")
        os.makedirs(self.data_dir, exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump({"integrations": self.integration_log}, f, indent=2)

        return config


class DataSourceRegistry:
    """
    Registry of all integrated data sources.
    Allows learning modules to discover and use routes as information sources.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.registry_file = os.path.join(data_dir, "data_source_registry.json")
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load data source registry."""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"sources": [], "metadata": {}}

    def register_source(self, source_config: Dict) -> bool:
        """
        Register a data source.

        source_config should contain:
        - source_id: unique identifier
        - name: display name
        - endpoint: API endpoint
        - method: HTTP method
        - category: data category
        """
        try:
            # Check if already registered
            existing = [s for s in self.registry["sources"] if s.get("source_id") == source_config.get("source_id")]
            if not existing:
                self.registry["sources"].append(source_config)
                self._save_registry()
                logger.info(f"Registered source: {source_config.get('name')}")
                return True
            else:
                logger.info(f"Source already registered: {source_config.get('name')}")
                return False
        except Exception as e:
            logger.error(f"Error registering source: {e}")
            return False

    def register_bulk(self, sources: List[Dict]) -> int:
        """Register multiple sources at once."""
        count = 0
        for source in sources:
            if self.register_source(source):
                count += 1
        return count

    def get_all_sources(self) -> List[Dict]:
        """Get all registered sources."""
        return self.registry.get("sources", [])

    def get_sources_by_category(self, category: str) -> List[Dict]:
        """Get sources by category."""
        return [s for s in self.registry.get("sources", []) if s.get("category") == category]

    def get_source_by_id(self, source_id: str) -> Optional[Dict]:
        """Get specific source by ID."""
        sources = [s for s in self.registry.get("sources", []) if s.get("source_id") == source_id]
        return sources[0] if sources else None

    def _save_registry(self):
        """Persist registry to disk."""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def get_registry_summary(self) -> Dict:
        """Get summary of registry."""
        sources = self.registry.get("sources", [])

        categories = {}
        for source in sources:
            cat = source.get("category", "other")
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_sources": len(sources),
            "sources_by_category": categories,
            "sources": sources
        }


# Integration Hook for Flask App
def init_route_discovery(app, data_dir: str = "data"):
    """
    Initialize route discovery for Flask app.
    Automatically discovers and registers informational routes.
    """
    discovery = RouteDiscovery(app, data_dir)
    registry = DataSourceRegistry(data_dir)

    # Scan app for routes
    discovery.scan_app()

    # Register qualified routes as data sources
    config = discovery.register_routes_as_datasources()

    # Add sources to registry
    for source in config["data_sources"]:
        registry.register_source(source)

    logger.info(f"✓ Route discovery initialized")
    logger.info(f"  - Scanned: {len(discovery.discovered_routes)} total routes")
    logger.info(f"  - Qualified: {len(discovery.qualified_routes)} informational routes")
    logger.info(f"  - Registered: {len(config['data_sources'])} data sources")

    return discovery, registry
