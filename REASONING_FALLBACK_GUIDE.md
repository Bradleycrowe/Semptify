"""
REASONING FALLBACK INTEGRATION GUIDE
====================================

The universal reasoning fallback can be added to ANY failure point in the system.

## Quick Integration Pattern

```python
from services.reasoning_fallback import get_reasoning_fallback

# When your normal fix fails:
try:
    # Normal fix attempt
    result = fix_the_problem()
except Exception as e:
    # Fallback to reasoning
    fallback = get_reasoning_fallback()
    
    facts = {
        'error': str(e),
        'context': 'what_you_were_trying',
        'available_data': your_data_here
    }
    
    # Get AI suggestions
    solution = fallback.solve('problem_type', facts, context="Human description")
    
    # Or auto-apply best suggestion
    def try_fix(suggestion):
        # Your fix logic here
        return apply_fix(suggestion['value'])
    
    result = fallback.auto_apply('problem_type', facts, try_fix)
```

## Real-World Examples

### 1. Import Failures
```python
try:
    from some_module import something
except ImportError as e:
    fallback = get_reasoning_fallback()
    result = fallback.solve('import_failed', {
        'module': 'some_module',
        'error': str(e),
        'sys_path': sys.path,
        'installed_packages': [list from pip]
    })
    # Suggestions might include: install command, alternative imports, etc.
```

### 2. Test Failures
```python
if test_failed:
    fallback = get_reasoning_fallback()
    result = fallback.solve('test_failed', {
        'test_name': test.name,
        'error': test.error,
        'expected': test.expected,
        'actual': test.actual,
        'code_snippet': test.source
    })
    # Suggestions: code fixes, test updates, dependency issues
```

### 3. API Errors
```python
if response.status_code != 200:
    fallback = get_reasoning_fallback()
    result = fallback.solve('api_error', {
        'endpoint': url,
        'status': response.status_code,
        'response': response.text,
        'request_data': request_payload
    })
    # Suggestions: retry with different params, auth fixes, endpoint alternatives
```

### 4. Database Errors
```python
except sqlite3.OperationalError as e:
    fallback = get_reasoning_fallback()
    result = fallback.solve('db_error', {
        'query': sql_query,
        'error': str(e),
        'table': table_name,
        'schema': table_schema
    })
    # Suggestions: migration needed, column rename, index creation
```

### 5. File Not Found
```python
if not os.path.exists(path):
    fallback = get_reasoning_fallback()
    result = fallback.solve('file_missing', {
        'path': path,
        'cwd': os.getcwd(),
        'searched_locations': [list of paths tried],
        'file_type': 'config/data/template'
    })
    # Suggestions: create file, use default, check different location
```

## Integration Checklist

1. **Import the fallback**: `from services.reasoning_fallback import get_reasoning_fallback`
2. **Wrap failure points**: Add try/except or if/else around your fix attempts
3. **Build facts dict**: Include all relevant context (error, data, state)
4. **Choose problem_type**: Descriptive name (route_broken, import_failed, etc.)
5. **Call solve() or auto_apply()**: Get suggestions or auto-fix
6. **Log results**: Always print reasoning confidence and suggestions tried

## Best Practices

- **Rich facts**: More context = better suggestions
- **Specific problem_type**: Helps reasoning system understand domain
- **Graceful degradation**: If reasoning fails, system continues (never crashes)
- **Log everything**: Reasoning attempts show up in logs for debugging
- **Confidence threshold**: Only auto-apply high-confidence suggestions (>0.7)

## Current Integrations

✓ Card route fixing (services/card_fixer_service.py)
✓ Health check engine (engines/health_check_engine.py) 
□ Test runner (add to pytest hooks)
□ Import errors (add to __init__.py files)
□ API errors (add to external API calls)
□ File operations (add to file I/O wrappers)

## Adding to New Areas

To add reasoning fallback to a new area:
1. Find the failure/error handling code
2. Import get_reasoning_fallback()
3. Build facts dict with error context
4. Call fallback.solve() or fallback.auto_apply()
5. Log the reasoning result
6. Update this doc with the integration location
"""
