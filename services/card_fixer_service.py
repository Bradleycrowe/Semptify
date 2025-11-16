"""
Card Auto-Fix Service - Repairs broken card links and deactivates invalid cards
"""
import sqlite3
from typing import List, Dict, Any
from user_database import DB_PATH


def deactivate_broken_cards(broken_cards: List[Dict[str, Any]]) -> int:
    """Mark broken cards as inactive in database."""
    if not broken_cards:
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    count = 0
    
    for card in broken_cards:
        if card.get('active', 1) == 1:  # Only deactivate if currently active
            cur.execute(
                "UPDATE cards SET active = 0, updated_at = datetime('now') WHERE slug = ?",
                (card['slug'],)
            )
            count += cur.rowcount
    
    conn.commit()
    conn.close()
    return count


def update_card_route(slug: str, old_route: str, new_route: str) -> bool:
    """Update a card's route to corrected path."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE cards SET route = ?, updated_at = datetime('now') WHERE slug = ? AND route = ?",
        (new_route, slug, old_route)
    )
    
    success = cur.rowcount > 0
    conn.commit()
    conn.close()
    return success


def suggest_route_corrections(broken_route: str, valid_routes: List[str]) -> List[str]:
    """Suggest possible corrections for broken routes using fuzzy matching."""
    suggestions = []
    
    # Simple pattern matching - can be enhanced with fuzzy matching library
    broken_parts = broken_route.strip('/').split('/')
    
    for valid in valid_routes:
        valid_parts = valid.strip('/').split('/')
        
        # Check if main segment matches
        if broken_parts and valid_parts:
            if broken_parts[0] in valid or broken_parts[-1] in valid:
                suggestions.append(valid)
    
    return suggestions[:3]  # Top 3 suggestions


def auto_fix_cards(app) -> Dict[str, Any]:
    """Attempt automatic fixes for common card issues."""
    from engines.health_check_engine import validate_card_routes, get_all_flask_routes
    
    card_check = validate_card_routes(app)
    broken = card_check.get('broken_details', [])
    
    if not broken:
        return {'status': 'ok', 'fixes_applied': 0, 'message': 'No broken cards found'}
    
    valid_routes = [r['path'] for r in get_all_flask_routes(app)]
    fixes_applied = []
    deactivated = []
    
    # Common route mappings (hard-coded corrections)
    route_fixes = {
        '/calendar-timeline': '/timeline',
        '/ledger': '/api/ledger-calendar/ledger',
        '/demand-letter': None,  # Not implemented yet
        '/courtroom': None,
        '/laws': '/rights'
    }
    
    for card in broken:
        old_route = card['route']
        
        # Try known fixes first
        if old_route in route_fixes:
            new_route = route_fixes[old_route]
            if new_route and new_route in valid_routes:
                if update_card_route(card['slug'], old_route, new_route):
                    fixes_applied.append({
                        'slug': card['slug'],
                        'old': old_route,
                        'new': new_route
                    })
                    continue
        
        # If no fix available, keep card active
        pass  # Cards stay active even with broken routes

    # Never deactivate cards - admin will fix routes manually
    
    return {
        'status': 'completed',
        'fixes_applied': len(fixes_applied),
        'deactivated': len(deactivated),
        'details': {
            'fixed': fixes_applied,
            'deactivated': deactivated
        }
    }
