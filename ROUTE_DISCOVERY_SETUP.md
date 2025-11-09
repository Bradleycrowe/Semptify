# Route Discovery Integration Setup

## Quick Start (5 minutes)

### Step 1: Add to Semptify.py

In `Semptify.py`, find the blueprint registration section and add:

```python
# Around line 50-60 where blueprints are registered
from route_discovery_routes import route_discovery_bp, init_route_discovery_api

# After all other blueprints:
init_route_discovery_api(app)
app.register_blueprint(route_discovery_bp)
```

### Step 2: Initialize on First Run

The system auto-initializes on first request to:
- `/api/discovery/scan`
- or any other discovery endpoint

Or trigger manually:
```bash
curl -X POST http://localhost:5000/api/discovery/scan
```

### Step 3: Test It

```bash
# See all discovered routes
curl http://localhost:5000/api/discovery/qualified-routes

# See data source registry
curl http://localhost:5000/api/discovery/registry

# See integration status
curl http://localhost:5000/api/discovery/integration-status
```

## Integration with Learning Module

### Option 1: Auto-Integration (Recommended)

Update `preliminary_learning.py` to use discovered sources:

```python
# At top of preliminary_learning.py
from route_discovery_bridge import LearningModuleDataSourceAdapter, IntegrationBridge

class PreliminaryLearningModule:
    def __init__(self):
        # ... existing code ...

        # NEW: Initialize discovered sources
        try:
            self.bridge = IntegrationBridge()
            self.adapter = LearningModuleDataSourceAdapter(self.bridge)
        except:
            self.bridge = None
            self.adapter = None

    def get_procedures(self, category: str):
        # Try discovered sources first
        if self.adapter:
            result = self.adapter.query_data_sources(
                "preliminary_learning",
                f"procedures in {category}"
            )
            if result.get("discovered_results"):
                return result

        # Fall back to built-in knowledge
        return self.get_procedures_builtin(category)
```

### Option 2: Manual Query Endpoint

Create a new endpoint in `preliminary_learning_routes.py`:

```python
@learning_module_bp.route('/api/learning/discovered-sources', methods=['GET'])
def get_discovered_sources():
    """Get list of discovered data sources."""
    try:
        response = requests.get('http://localhost:5000/api/discovery/registry')
        return jsonify(response.json())
    except:
        return jsonify({"sources": []})
```

### Option 3: Query Via Discovery API

Learning module endpoints can make requests to discovery API:

```python
# In preliminary_learning_routes.py
import requests

@learning_module_bp.route('/api/learning/procedures-enhanced', methods=['GET'])
def get_procedures_enhanced():
    """Get procedures from both built-in and discovered sources."""
    category = request.args.get('category', 'rental')

    # Query discovered sources
    try:
        response = requests.post(
            'http://localhost:5000/api/discovery/query-sources',
            json={
                "query": f"procedures for {category}",
                "learning_category": "procedures"
            }
        )
        discovered = response.json()
    except:
        discovered = {"results": []}

    # Get built-in procedures
    builtin = get_procedures_builtin(category)

    # Merge and return
    return jsonify({
        "built_in": builtin,
        "discovered_sources": discovered.get("results", []),
        "total_sources": len(discovered.get("results", []))
    })
```

## Managing Discovered Sources

### Adding New Routes

1. Create new Flask route (e.g., `/api/learning/housing-agencies`):

```python
@some_routes_bp.route('/api/learning/housing-agencies', methods=['GET'])
def get_housing_agencies():
    return jsonify({
        "agencies": [...]
    })
```

2. Register the route:

```bash
# Scan for new routes
curl -X POST http://localhost:5000/api/discovery/scan

# Register new routes as data sources
curl -X POST http://localhost:5000/api/discovery/register-sources
```

3. Verify it was discovered:

```bash
curl http://localhost:5000/api/discovery/registry
```

### Excluding Routes from Discovery

Routes are excluded if they:
- Use POST/PUT/DELETE methods (operational)
- Are under `/admin/` path (administrative)
- Are static files
- Don't have `/api/` prefix

If you need to exclude a specific `/api/` GET route, update the pattern in `route_discovery.py`:

```python
# In _is_informational_route():
EXCLUDED_ENDPOINTS = [
    "/api/internal/",  # Add your pattern
    "/api/debug/"
]

for pattern in EXCLUDED_ENDPOINTS:
    if pattern in path_lower:
        return False
```

### Custom Route Classification

You can customize classification by modifying patterns:

```python
# In route_discovery.py _is_informational_route():
informational_keywords = [
    "/api/learning",
    "/api/procedures",
    "/api/my-custom-info-endpoint",  # Add custom pattern
    # ...
]
```

## Monitoring & Troubleshooting

### Check Discovery Status

```bash
curl http://localhost:5000/api/discovery/integration-status
```

Output:
```json
{
  "status": "success",
  "discovered_sources_count": 11,
  "integration_mappings": 3,
  "sources": [...]
}
```

### View Routes by Category

```bash
curl http://localhost:5000/api/discovery/routes-by-category/procedures
```

### Test Specific Route

Before adding to registry, test a route:

```python
# In route_discovery.py
discovery = RouteDiscovery(app)
is_working, description, data = discovery.test_route(
    app.test_client(),
    "/api/learning/procedures"
)
print(f"Working: {is_working}, {description}")
```

### View Query Statistics

```bash
curl http://localhost:5000/api/discovery/query-statistics
```

Output shows how many modules are using discovered sources.

## Performance Tips

### 1. Cache Discoveries

Discovery results are cached in:
- `data/route_catalog.json`
- `data/data_source_registry.json`

No re-scanning needed unless new routes added.

### 2. Batch Queries

Instead of querying each source individually:

```python
# Don't do this:
for source in sources:
    result = query_source(source)

# Do this:
results = requests.post('/api/discovery/query-sources', json={
    "query": "...",
    "learning_category": "procedures"
})
```

### 3. Use Category Filters

Narrow searches by category to reduce overhead:

```bash
curl -X POST http://localhost:5000/api/discovery/query-sources \
  -H "Content-Type: application/json" \
  -d '{"query":"rental", "learning_category":"procedures"}'
```

## Common Issues & Solutions

### Issue: "Bridge not initialized"

**Cause**: `init_route_discovery_api()` not called

**Fix**: Add to Semptify.py:
```python
from route_discovery_routes import init_route_discovery_api
init_route_discovery_api(app)
```

### Issue: Routes discovered but not showing in registry

**Cause**: Registration step not run

**Fix**: Call registration endpoint:
```bash
curl -X POST http://localhost:5000/api/discovery/register-sources
```

### Issue: Learning module can't find discovered sources

**Cause**: Bridge not initialized in learning module

**Fix**: Update learning module:
```python
from route_discovery_bridge import IntegrationBridge, LearningModuleDataSourceAdapter

# In __init__:
self.bridge = IntegrationBridge()
self.adapter = LearningModuleDataSourceAdapter(self.bridge)
```

### Issue: Old discovered sources showing after removal

**Cause**: Cache not cleared

**Fix**: Delete cache files:
```bash
rm data/route_catalog.json
rm data/data_source_registry.json
```

Then re-run discovery.

## Advanced: Custom Integration Pattern

For advanced use cases, create custom data sources:

```python
# custom_datasources.py
from route_discovery_bridge import DiscoveredDataSource

class CustomDataSource(DiscoveredDataSource):
    """Custom data source with specialized query logic."""

    def query(self, query_type: str, params=None):
        # Custom query logic
        if query_type == "legal_precedents":
            return self.fetch_legal_precedents(params)
        else:
            return super().query(query_type, params)

    def fetch_legal_precedents(self, params):
        # Your custom logic
        pass
```

Then register it:

```python
bridge.discovered_sources["custom_legal"] = CustomDataSource(
    {"source_id": "custom_legal", ...},
    client=app.test_client()
)
```

## Next: Calendar Hub Integration

Once route discovery is working, integrate with calendar hub:

```python
# In calendar_api.py
from route_discovery_bridge import IntegrationBridge

class CalendarHub:
    def __init__(self):
        # ... existing code ...
        self.bridge = IntegrationBridge()

    def query_datasource(self, source_id):
        """Query discovered data source through calendar."""
        source = self.bridge.discovered_sources.get(source_id)
        if source:
            return source.fetch()
        return None
```

## Documentation Reference

- **Complete Guide**: See `ROUTE_DISCOVERY_SYSTEM.md`
- **Code**: `route_discovery.py`, `route_discovery_bridge.py`, `route_discovery_routes.py`
- **API Docs**: Endpoint reference in `ROUTE_DISCOVERY_SYSTEM.md`
