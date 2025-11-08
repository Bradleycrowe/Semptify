"""
Minnesota / Eagan Configuration for Semptify
Accurate laws for Eagan, MN 55121 (Dakota County)
Updated: November 2025
"""

MINNESOTA_LAWS = {
    "state": "minnesota",
    "city": "eagan_city",
    "county": "dakota_county",
    "zip": "55121",

    "laws": {
        # MINNESOTA STATE LAWS
        "habitability": {
            "statute": "Minnesota Statutes §504B.161",
            "requirement": "Landlord must maintain fit premises (heat, water, structural soundness)",
            "deadline": "reasonable time (typically 14 days)",
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.161"
        },

        "security_deposit": {
            "statute": "Minnesota Statutes §504B.178",
            "no_limit": True,
            "requirement": "No statutory limit, but must be reasonable",
            "return_deadline": "21 days after move-out",
            "itemized_statement": "Required",
            "interest": "1% annual if 12+ units",
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.178"
        },

        "retaliation": {
            "statute": "Minnesota Statutes §504B.285",
            "presumption_period": "90 days",
            "penalty": "Actual damages + up to 3 months rent or $500 (whichever greater)",
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.285"
        },

        "repairs_and_deduct": {
            "statute": "Minnesota Statutes §504B.425",
            "allowed": True,
            "max_amount": "$100 or 1 month rent (whichever less)",
            "requirement": "Must give notice first, wait reasonable time",
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.425"
        },

        "rent_escrow": {
            "statute": "Minnesota Statutes §504B.385",
            "allowed": True,
            "requirement": "Can deposit rent with court if violations exist",
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.385"
        },

        "entry_notice": {
            "statute": "Minnesota Statutes §504B.211",
            "requirement": "Reasonable notice (typically 24 hours)",
            "emergency_exception": True,
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.211"
        },

        "lease_termination": {
            "month_to_month": "End of monthly rental period (not less than 1 month notice)",
            "statute": "Minnesota Statutes §504B.135",
            "source": "https://www.revisor.mn.gov/statutes/cite/504B.135"
        },

        # DAKOTA COUNTY (where Eagan is)
        "health_inspections": {
            "jurisdiction": "Dakota County Public Health",
            "phone": "651-554-6100",
            "website": "https://www.co.dakota.mn.us/HealthFamily/PublicHealth/",
            "complaint_process": "Call or file online complaint"
        },

        # EAGAN CITY
        "rental_licensing": {
            "statute": "Eagan City Code §5-5",
            "requirement": "All rental properties must be licensed with city",
            "inspection": "Required every 3 years",
            "phone": "651-675-5500",
            "website": "https://www.cityofeagan.com/",
            "verification": "Tenants can verify if rental is licensed"
        },

        "property_maintenance": {
            "statute": "Eagan City Code Chapter 8",
            "standard": "International Property Maintenance Code",
            "enforcement": "City code enforcement",
            "complaints": "651-675-5500"
        }
    },

    "typical_timelines": {
        "emergency_repairs": "24 hours (no heat in winter, no water, gas leak)",
        "urgent_repairs": "3-5 days (broken window, door lock)",
        "normal_repairs": "14 days (typical reasonable time)",
        "non_urgent": "30 days (cosmetic, minor issues)"
    },

    "tenant_resources": {
        "home_line": {
            "name": "HOME Line (Minnesota tenant hotline)",
            "phone": "866-866-3546",
            "website": "https://homelinemn.org/",
            "services": "Free tenant rights advice for Minnesota"
        },
        "legal_aid": {
            "name": "Southern Minnesota Regional Legal Services",
            "phone": "952-888-9615",
            "website": "https://www.smrls.org/",
            "income_limits": "Must qualify based on income"
        },
        "housing_court": {
            "name": "Dakota County Housing Court",
            "location": "1560 Highway 55, Hastings, MN 55033",
            "phone": "651-438-4314",
            "website": "https://www.mncourts.gov/Find-Courts/Dakota-County.aspx"
        }
    },

    "common_rent_ranges_2025": {
        "studio": "$900-$1,200",
        "1br": "$1,100-$1,500",
        "2br": "$1,400-$1,900",
        "3br": "$1,800-$2,500",
        "source": "Based on Eagan area listings Nov 2025"
    }
}


# User-controlled progression settings
USER_CONTROL = {
    "auto_advance": False,  # Never auto-advance stages
    "require_confirmation": True,  # Always ask before moving to next step
    "allow_skip": False,  # User must complete each stage
    "show_next_button": True,  # Always show "Ready for Next Step" button
}


# What user sees at each stage
USER_JOURNEY_STAGES = {
    "searching": {
        "title": "🔍 Apartment Search",
        "next_action": "I Found a Place",
        "user_decides": True
    },
    "applying": {
        "title": "📝 Application Submitted",
        "next_action": "I Got Approved",
        "user_decides": True
    },
    "signing": {
        "title": "📄 Lease Review",
        "next_action": "I Signed the Lease",
        "user_decides": True
    },
    "moving_in": {
        "title": "📸 Move-In Inspection",
        "next_action": "I Moved In",
        "user_decides": True
    },
    "living": {
        "title": "🏠 Living There",
        "next_action": "Report a Problem",
        "user_decides": True
    },
    "issue": {
        "title": "🔧 Resolving Issue",
        "next_action": "Issue Resolved",
        "user_decides": True
    },
    "moving_out": {
        "title": "📦 Moving Out",
        "next_action": "I Moved Out",
        "user_decides": True
    }
}
