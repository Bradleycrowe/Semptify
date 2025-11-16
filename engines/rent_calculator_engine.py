"""Auto-generated calculator engine"""

def rent_calculator_logic(data):
    """Calculate legal rent increases for Minnesota."""
    current_rent = float(data.get('current_rent', 0))
    new_rent = float(data.get('new_rent', 0))
    lease_date = data.get('lease_date', '')
    location = data.get('location', 'Minnesota')
    
    # Calculate increase
    increase_amount = new_rent - current_rent
    increase_percent = (increase_amount / current_rent * 100) if current_rent > 0 else 0
    
    # TODO: Implement actual MN rent control statutes
    # TODO: Check local ordinances (Minneapolis, St. Paul have rent stabilization)
    # TODO: Factor in notice requirements
    
    # Placeholder logic
    is_legal = True
    reasons = []
    statutes = []
    
    if increase_percent > 10:
        reasons.append(f"Increase of {increase_percent:.1f}% exceeds typical market range")
        statutes.append("MN Stat § 504B.135 (60-day notice required for increases over 10%)")
    
    if increase_percent > 3:
        statutes.append("Minneapolis Rent Stabilization Ordinance may apply")
        reasons.append("Check local rent stabilization ordinance")
    
    return {
        "status": "success",
        "current_rent": current_rent,
        "new_rent": new_rent,
        "increase_amount": round(increase_amount, 2),
        "increase_percent": round(increase_percent, 2),
        "is_legal": is_legal,
        "reasons": reasons,
        "applicable_statutes": statutes,
        "message": "Rent calculation completed (using placeholder MN rules)"
    }
