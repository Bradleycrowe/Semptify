"""
Route Discovery Integration Bridge
Connects discovered routes to learning modules and data flow engine
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscoveredDataSource:
    """
    Wrapper for a discovered route that acts as a data source.
    Provides interface for learning modules to query discovered routes.
    """

    def __init__(self, route_info: Dict, client=None):
        self.route_info = route_info
        self.client = client
        self.endpoint = route_info.get("endpoint", "")
        self.method = route_info.get("method", "GET")
        self.source_id = route_info.get("source_id", "")
        self.name = route_info.get("name", "")
        self.category = route_info.get("category", "")
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour

    def fetch(self, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Fetch data from discovered route.

        Returns:
            Dict: Response data or None if error
        """
        if not self.client:
            logger.error(f"No client available for {self.name}")
            return None

        try:
            if self.method == "GET":
                response = self.client.get(self.endpoint, query_string=params or {})
            elif self.method == "POST":
                response = self.client.post(self.endpoint, json=params or {})
            else:
                return None

            if response.status_code == 200:
                data = response.get_json()
                self.cache[str(params)] = data
                return data
            else:
                logger.warning(f"HTTP {response.status_code} from {self.endpoint}")
                return None

        except Exception as e:
            logger.error(f"Error fetching from {self.name}: {e}")
            return None

    def query(self, query_type: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Query the discovered data source.

        query_type can be:
        - "procedures": Get procedures
        - "forms": Get forms
        - "timeline": Get timeline
        - "resources": Get resources
        - "facts": Get fact-check data
        """
        # Route the query based on endpoint
        if "procedures" in self.endpoint and query_type == "procedures":
            return self.fetch(params)
        elif "forms" in self.endpoint and query_type == "forms":
            return self.fetch(params)
        elif "timeline" in self.endpoint and query_type == "timeline":
            return self.fetch(params)
        elif "facts" in self.endpoint or "fact-check" in self.endpoint:
            return self.fetch(params)
        else:
            return self.fetch(params)

    def get_metadata(self) -> Dict:
        """Get metadata about this data source."""
        return {
            "source_id": self.source_id,
            "name": self.name,
            "endpoint": self.endpoint,
            "method": self.method,
            "category": self.category,
            "type": "discovered_route"
        }


class IntegrationBridge:
    """
    Bridge between route discovery and learning modules.
    Manages integration of discovered routes as learning data sources.
    """

    def __init__(self, data_dir: str = "data", client=None):
        self.data_dir = data_dir
        self.client = client
        self.discovered_sources: Dict[str, DiscoveredDataSource] = {}
        self.integration_map = {}  # Map learning categories to data sources
        self.load_discovered_sources()

    def load_discovered_sources(self):
        """Load previously discovered sources from registry."""
        registry_file = os.path.join(self.data_dir, "data_source_registry.json")

        if os.path.exists(registry_file):
            try:
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
                    for source_config in registry.get("sources", []):
                        source = DiscoveredDataSource(source_config, self.client)
                        self.discovered_sources[source_config.get("source_id")] = source
                        logger.info(f"Loaded discovered source: {source.name}")
            except Exception as e:
                logger.error(f"Error loading discovered sources: {e}")

    def add_discovered_source(self, source_config: Dict) -> bool:
        """Add a newly discovered source."""
        try:
            source = DiscoveredDataSource(source_config, self.client)
            self.discovered_sources[source_config.get("source_id")] = source
            logger.info(f"Added discovered source: {source.name}")
            return True
        except Exception as e:
            logger.error(f"Error adding discovered source: {e}")
            return False

    def get_sources_by_learning_category(self, learning_category: str) -> List[DiscoveredDataSource]:
        """
        Get discovered sources relevant to a learning category.

        learning_category examples:
        - "procedures": /api/learning/procedures/*
        - "forms": /api/learning/forms/*
        - "timeline": /api/learning/timeline/*
        - "fact-check": /api/learning/fact-check/*
        """
        sources = []

        for source_id, source in self.discovered_sources.items():
            # Match learning category to source endpoint
            if learning_category in source.endpoint.lower():
                sources.append(source)

        return sources

    def query_all_sources(self, query: str, learning_category: Optional[str] = None) -> Dict:
        """
        Query all discovered sources for information.

        Returns aggregated results from all matching sources.
        """
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources_queried": 0,
            "results": []
        }

        # Determine which sources to query
        if learning_category:
            sources = self.get_sources_by_learning_category(learning_category)
        else:
            sources = list(self.discovered_sources.values())

        # Query each source
        for source in sources:
            try:
                data = source.fetch({"query": query})
                if data:
                    results["results"].append({
                        "source": source.get_metadata(),
                        "data": data
                    })
                    results["sources_queried"] += 1
            except Exception as e:
                logger.warning(f"Error querying {source.name}: {e}")

        return results

    def map_learning_category_to_sources(self, learning_category: str, endpoint_patterns: List[str]) -> Dict:
        """
        Create mapping from learning category to data sources.

        Example:
            map_learning_category_to_sources(
                "rental_procedures",
                ["/api/learning/procedures/rental", "/api/procedures"]
            )
        """
        mapped_sources = []

        for source_id, source in self.discovered_sources.items():
            for pattern in endpoint_patterns:
                if pattern.lower() in source.endpoint.lower():
                    mapped_sources.append(source_id)

        self.integration_map[learning_category] = {
            "learning_category": learning_category,
            "endpoint_patterns": endpoint_patterns,
            "source_ids": mapped_sources,
            "mapped_at": datetime.now().isoformat()
        }

        logger.info(f"Mapped {learning_category} to {len(mapped_sources)} sources")
        return self.integration_map[learning_category]

    def get_learning_module_datasources(self, module_name: str) -> List[Dict]:
        """
        Get all data sources that should be used by a learning module.

        Used by learning module to find all available data sources.
        """
        sources = []

        for source_id, source in self.discovered_sources.items():
            # Match module name to source
            if module_name.lower() in source.endpoint.lower() or \
               source.category == module_name.lower():
                sources.append(source.get_metadata())

        return sources

    def get_integration_status(self) -> Dict:
        """Get status of integration."""
        return {
            "timestamp": datetime.now().isoformat(),
            "discovered_sources_count": len(self.discovered_sources),
            "integration_mappings": len(self.integration_map),
            "sources": [s.get_metadata() for s in self.discovered_sources.values()],
            "mappings": self.integration_map
        }

    def save_integration_status(self):
        """Save integration status to file."""
        status_file = os.path.join(self.data_dir, "integration_status.json")
        os.makedirs(self.data_dir, exist_ok=True)

        with open(status_file, 'w') as f:
            json.dump(self.get_integration_status(), f, indent=2)

        logger.info(f"Saved integration status to {status_file}")


class LearningModuleDataSourceAdapter:
    """
    Adapter that provides learning modules with discovered data sources.
    Learning modules can query discovered routes just like built-in sources.
    """

    def __init__(self, bridge: IntegrationBridge):
        self.bridge = bridge
        self.query_history = []

    def get_data_sources_for_module(self, module_name: str) -> Dict:
        """
        Get data sources available to a learning module.

        Returns dict with:
        - built_in_sources: Hardcoded in module
        - discovered_sources: From route discovery
        - combined_sources: All sources merged
        """
        discovered = self.bridge.get_learning_module_datasources(module_name)

        return {
            "module": module_name,
            "discovered_sources": discovered,
            "source_count": len(discovered),
            "timestamp": datetime.now().isoformat()
        }

    def query_data_sources(self, module_name: str, query: str, category: Optional[str] = None) -> Dict:
        """
        Query data sources for a module.
        Prioritizes discovered sources but can fall back to built-in.
        """
        result = {
            "module": module_name,
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "discovered_results": [],
            "built_in_results": [],
            "total_results": 0
        }

        # Query discovered sources
        discovered_results = self.bridge.query_all_sources(query, category)
        result["discovered_results"] = discovered_results.get("results", [])

        # Log query
        self.query_history.append({
            "timestamp": datetime.now().isoformat(),
            "module": module_name,
            "query": query,
            "results_found": len(result["discovered_results"])
        })

        result["total_results"] = len(result["discovered_results"])
        return result

    def get_query_statistics(self) -> Dict:
        """Get statistics about queries to discovered sources."""
        if not self.query_history:
            return {"queries": 0}

        modules = set(q.get("module") for q in self.query_history)

        return {
            "total_queries": len(self.query_history),
            "modules_using_discovered_sources": len(modules),
            "queries_by_module": {
                m: len([q for q in self.query_history if q.get("module") == m])
                for m in modules
            },
            "recent_queries": self.query_history[-10:]
        }
