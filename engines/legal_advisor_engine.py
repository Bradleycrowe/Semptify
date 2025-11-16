"""Auto-generated search engine"""

def legal_advisor_logic(query):
    """Search logic."""
    search_term = query.get('search', '')
    location = query.get('location', '')
    results = [{"id": 1, "title": f"Result for {search_term}", "location": location}] if search_term else []
    return {"status": "success", "results": results, "count": len(results)}
