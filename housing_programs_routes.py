"""
Flask routes for Housing Programs & Resources system

Endpoints:
- GET /housing-programs - Main search interface
- POST /api/programs/search - Search programs by location and criteria
- GET /api/programs/category/<category> - Get programs by category
- GET /api/programs/guide/<program_id> - Get detailed application guide
- POST /api/programs/track-outcome - Track application outcome
- GET /api/programs/intensity-recommendations - Get intensity-based recommendations
- GET /api/programs/eligibility-check - Check eligibility for programs
- GET /programs-for-landlords - Landlord resources page
"""

from flask import Blueprint, render_template, request, jsonify
import logging
from engines.housing_programs_engine import HousingProgramsEngine, ProgramCategory, UrgencyLevel

# Create blueprint
housing_programs_bp = Blueprint('housing_programs', __name__)

# Initialize engine
engine = HousingProgramsEngine()

logger = logging.getLogger(__name__)


@housing_programs_bp.route('/housing-programs')
def programs():  # Renamed to match template url_for('housing_programs_bp.programs')
    """Main housing programs search interface"""
    return render_template('housing_programs.html')


@housing_programs_bp.route('/api/programs/search', methods=['POST'])
def search_programs():
    """
    Search for housing programs based on location and criteria.
    
    Request body:
    {
        "location": {
            "city": "Minneapolis",
            "county": "Hennepin",
            "state": "MN",
            "zip": "55401"
        },
        "categories": ["rent_assistance", "utility_assistance"],  // Optional
        "urgency": "urgent",  // routine, soon, urgent, emergency
        "household_size": 3,  // Optional
        "annual_income": 28000,  // Optional
        "special_needs": ["veteran", "disability"],  // Optional
        "for_landlord": false  // Optional
    }
    
    Returns:
    {
        "federal_programs": [...],
        "state_programs": [...],
        "county_programs": [...],
        "city_programs": [...],
        "nonprofit_resources": [...],
        "recommended_first_steps": [...],
        "emergency_contacts": [...],
        "eligibility_guidance": {...}
    }
    """
    try:
        data = request.get_json()
        
        # Validate location
        location = data.get('location', {})
        if not location.get('state'):
            return jsonify({
                "error": "Location must include at least a state"
            }), 400
        
        # Get search parameters
        categories = data.get('categories')
        urgency = data.get('urgency', 'routine')
        household_size = data.get('household_size')
        annual_income = data.get('annual_income')
        special_needs = data.get('special_needs')
        for_landlord = data.get('for_landlord', False)
        
        # Discover programs
        result = engine.discover_programs(
            location=location,
            categories=categories,
            urgency=urgency,
            household_size=household_size,
            annual_income=annual_income,
            special_needs=special_needs,
            for_landlord=for_landlord
        )
        
        logger.info(f"Programs search: {location.get('city', 'unknown')}, {len(result['federal_programs'])} federal programs found")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error searching programs: {str(e)}")
        return jsonify({
            "error": "Failed to search programs",
            "detail": str(e)
        }), 500


@housing_programs_bp.route('/api/programs/category/<category>')
def get_programs_by_category(category):
    """
    Get all programs in a specific category.
    
    Query params:
    - state: State abbreviation (required)
    - for_landlord: true/false (optional)
    
    Returns list of programs in that category.
    """
    try:
        state = request.args.get('state')
        if not state:
            return jsonify({
                "error": "State parameter is required"
            }), 400
        
        for_landlord = request.args.get('for_landlord', 'false').lower() == 'true'
        
        location = {"state": state}
        
        result = engine.discover_programs(
            location=location,
            categories=[category],
            for_landlord=for_landlord
        )
        
        # Flatten all programs
        all_programs = (
            result.get('federal_programs', []) +
            result.get('state_programs', []) +
            result.get('county_programs', []) +
            result.get('city_programs', []) +
            result.get('nonprofit_resources', [])
        )
        
        return jsonify({
            "category": category,
            "state": state,
            "programs": all_programs,
            "total": len(all_programs)
        })
        
    except Exception as e:
        logger.error(f"Error getting programs by category: {str(e)}")
        return jsonify({
            "error": "Failed to get programs",
            "detail": str(e)
        }), 500


@housing_programs_bp.route('/api/programs/guide/<program_id>')
def get_application_guide(program_id):
    """
    Get detailed application guide for a specific program.
    
    Query params:
    - city, county, state, zip: Location information
    - household_size, annual_income: Optional household info
    
    Returns step-by-step application guide.
    """
    try:
        location = {
            "city": request.args.get('city'),
            "county": request.args.get('county'),
            "state": request.args.get('state'),
            "zip": request.args.get('zip')
        }
        
        household_info = {}
        if request.args.get('household_size'):
            household_info['size'] = int(request.args.get('household_size'))
        if request.args.get('annual_income'):
            household_info['income'] = float(request.args.get('annual_income'))
        
        guide = engine.generate_application_guide(
            program_id=program_id,
            location=location,
            household_info=household_info if household_info else None
        )
        
        return jsonify(guide)
        
    except Exception as e:
        logger.error(f"Error generating application guide: {str(e)}")
        return jsonify({
            "error": "Failed to generate guide",
            "detail": str(e)
        }), 500


@housing_programs_bp.route('/api/programs/track-outcome', methods=['POST'])
def track_outcome():
    """
    Track outcome of a program application.
    
    Request body:
    {
        "program_id": "HUD_Section8",
        "outcome": "approved",  // approved, denied, pending
        "timeline_days": 90,  // Optional
        "notes": "Got approved after 3 months"  // Optional
    }
    """
    try:
        data = request.get_json()
        
        program_id = data.get('program_id')
        outcome = data.get('outcome')
        
        if not program_id or not outcome:
            return jsonify({
                "error": "program_id and outcome are required"
            }), 400
        
        if outcome not in ['approved', 'denied', 'pending']:
            return jsonify({
                "error": "outcome must be approved, denied, or pending"
            }), 400
        
        engine.track_application_outcome(
            program_id=program_id,
            outcome=outcome,
            timeline_days=data.get('timeline_days'),
            notes=data.get('notes')
        )
        
        return jsonify({
            "success": True,
            "message": "Outcome tracked successfully"
        })
        
    except Exception as e:
        logger.error(f"Error tracking outcome: {str(e)}")
        return jsonify({
            "error": "Failed to track outcome",
            "detail": str(e)
        }), 500


@housing_programs_bp.route('/api/programs/intensity-recommendations', methods=['POST'])
def get_intensity_recommendations():
    """
    Get program recommendations based on adaptive intensity level.
    
    Request body:
    {
        "intensity_level": "ESCALATED",  // POSITIVE, COLLABORATIVE, ASSERTIVE, ESCALATED, MAXIMUM
        "situation": {
            "issue": "no_heat",
            "days": 15,
            "location": {...}
        }
    }
    
    Returns intensity-appropriate program recommendations.
    """
    try:
        data = request.get_json()
        
        intensity_level = data.get('intensity_level')
        situation = data.get('situation', {})
        
        if not intensity_level:
            return jsonify({
                "error": "intensity_level is required"
            }), 400
        
        recommendations = engine.get_intensity_based_recommendations(
            intensity_level=intensity_level,
            situation=situation
        )
        
        return jsonify(recommendations)
        
    except Exception as e:
        logger.error(f"Error getting intensity recommendations: {str(e)}")
        return jsonify({
            "error": "Failed to get recommendations",
            "detail": str(e)
        }), 500


@housing_programs_bp.route('/api/programs/eligibility-check', methods=['POST'])
def check_eligibility():
    """
    Check eligibility for programs based on household info.
    
    Request body:
    {
        "household_size": 3,
        "annual_income": 28000,
        "state": "MN"
    }
    
    Returns eligibility guidance showing which programs you likely qualify for.
    """
    try:
        data = request.get_json()
        
        household_size = data.get('household_size')
        annual_income = data.get('annual_income')
        state = data.get('state')
        
        if not all([household_size, annual_income, state]):
            return jsonify({
                "error": "household_size, annual_income, and state are required"
            }), 400
        
        eligibility = engine._calculate_eligibility(
            household_size=int(household_size),
            annual_income=float(annual_income),
            state=state
        )
        
        return jsonify(eligibility)
        
    except Exception as e:
        logger.error(f"Error checking eligibility: {str(e)}")
        return jsonify({
            "error": "Failed to check eligibility",
            "detail": str(e)
        }), 500


@housing_programs_bp.route('/programs-for-landlords')
def landlord_programs_page():
    """Landlord resources and programs page"""
    return render_template('landlord_programs.html')


@housing_programs_bp.route('/api/programs/all-categories')
def get_all_categories():
    """Get list of all program categories with descriptions"""
    categories = [
        {
            "id": "rent_assistance",
            "name": "Rent Assistance",
            "description": "Help paying rent - Section 8, emergency funds, etc.",
            "icon": "💰"
        },
        {
            "id": "utility_assistance",
            "name": "Utility Assistance",
            "description": "Help with heating, cooling, electricity, water bills",
            "icon": "⚡"
        },
        {
            "id": "emergency_funds",
            "name": "Emergency Funds",
            "description": "Quick assistance to prevent eviction or shutoff",
            "icon": "🚨"
        },
        {
            "id": "legal_aid",
            "name": "Legal Aid",
            "description": "Free legal help for housing issues and evictions",
            "icon": "⚖️"
        },
        {
            "id": "housing_counseling",
            "name": "Housing Counseling",
            "description": "Expert guidance on housing rights and resources",
            "icon": "🏠"
        },
        {
            "id": "weatherization",
            "name": "Weatherization",
            "description": "Free home energy efficiency improvements",
            "icon": "🌡️"
        },
        {
            "id": "disability_accessibility",
            "name": "Disability & Accessibility",
            "description": "Housing help for people with disabilities",
            "icon": "♿"
        },
        {
            "id": "veteran_services",
            "name": "Veteran Services",
            "description": "Housing programs for veterans and families",
            "icon": "🎖️"
        },
        {
            "id": "senior_services",
            "name": "Senior Services",
            "description": "Housing assistance for elderly residents",
            "icon": "👴"
        },
        {
            "id": "homeless_prevention",
            "name": "Homeless Prevention",
            "description": "Emergency help to keep you housed",
            "icon": "🏚️"
        },
        {
            "id": "food_assistance",
            "name": "Food Assistance",
            "description": "Food banks, SNAP, meal programs",
            "icon": "🍎"
        },
        {
            "id": "healthcare",
            "name": "Healthcare",
            "description": "Medical assistance and health insurance programs",
            "icon": "🏥"
        },
        {
            "id": "landlord_rehab",
            "name": "Landlord Rehab Programs",
            "description": "Loans and grants for property improvements",
            "icon": "🔧",
            "for_landlords": True
        },
        {
            "id": "landlord_tax_credits",
            "name": "Landlord Tax Credits",
            "description": "Tax incentives for renting to low-income tenants",
            "icon": "💵",
            "for_landlords": True
        },
        {
            "id": "mediation",
            "name": "Mediation Services",
            "description": "Neutral third party to resolve disputes",
            "icon": "🤝"
        }
    ]
    
    return jsonify({
        "categories": categories,
        "total": len(categories)
    })


@housing_programs_bp.route('/api/programs/quick-help')
def get_quick_help():
    """
    Get immediate help contacts for emergency situations.
    
    Query param:
    - state: State abbreviation
    
    Returns emergency contacts and first steps.
    """
    try:
        state = request.args.get('state', 'US')
        
        quick_help = {
            "emergency_contacts": [
                {
                    "name": "United Way 211",
                    "phone": "211",
                    "description": "Call or text 211 to connect to ALL local resources",
                    "available": "24/7",
                    "why": "Best starting point - connects you to everything available in your area"
                },
                {
                    "name": "National Suicide Prevention Lifeline",
                    "phone": "988",
                    "description": "If you're in crisis and need immediate support",
                    "available": "24/7"
                },
                {
                    "name": "National Domestic Violence Hotline",
                    "phone": "1-800-799-7233",
                    "description": "If housing emergency involves domestic violence",
                    "available": "24/7"
                }
            ],
            "immediate_steps": [
                {
                    "step": 1,
                    "action": "Call 211 RIGHT NOW",
                    "why": "They can connect you to emergency assistance in your area immediately"
                },
                {
                    "step": 2,
                    "action": "If you have an eviction notice or shutoff notice, take a photo and keep it handy",
                    "why": "You'll need this for emergency assistance applications"
                },
                {
                    "step": 3,
                    "action": "Gather any income proof (pay stubs, benefits letters)",
                    "why": "Most programs need this - having it ready speeds up help"
                },
                {
                    "step": 4,
                    "action": "Contact local legal aid",
                    "why": "Even if you think it's too late, you may have legal defenses"
                }
            ],
            "next_steps": [
                "Use the search tool on this page to find ALL programs you qualify for",
                "Apply to MULTIPLE programs - don't put all eggs in one basket",
                "Keep copies of everything you submit",
                "Follow up regularly - squeaky wheel gets the grease"
            ]
        }
        
        return jsonify(quick_help)
        
    except Exception as e:
        logger.error(f"Error getting quick help: {str(e)}")
        return jsonify({
            "error": "Failed to get quick help",
            "detail": str(e)
        }), 500


# Error handlers
@housing_programs_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource not found"
    }), 404


@housing_programs_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500
