"""
Librarian Engine - Populates and maintains law library with local laws, ordinances, and codes.
Helps users and guests find relevant legal information with facts cards and information modules.
The Librarian also provides daily fun facts on various topics.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import hashlib
import random


# Fun facts database - The Librarian's personality
FUN_FACTS = [
    "Did you know? The Fair Housing Act was signed into law just one week after Dr. Martin Luther King Jr.'s assassination in 1968.",
    "Fun fact: The word 'tenant' comes from the Latin 'tenere' meaning 'to hold.' You hold the right to occupy your home!",
    "Here's something interesting: In ancient Rome, landlords were called 'domini' (lords) and tenants were 'coloni' (cultivators).",
    "Did you know? The first rent control law in the U.S. was passed in New York City in 1943 during World War II.",
    "Fun fact: The average American moves 11.7 times in their lifetime. That's a lot of leases!",
    "Interesting tidbit: The term 'landlord' dates back to feudal times when lords literally owned the land.",
    "Did you know? Security deposits became common in the 1970s. Before that, handshake agreements were more typical.",
    "Fun fact: The longest residential lease ever recorded was for 10 million years in Ireland (though it was a legal quirk!).",
    "Here's a cool fact: In Japan, it's customary to give your landlord a 'gift' of 1-2 months rent when moving in, which you never get back!",
    "Did you know? The word 'eviction' comes from the Latin 'evincere' meaning 'to overcome completely.'",
    "Fun fact: In Sweden, tenant rights are so strong that it can take years to evict someone, even for non-payment.",
    "Interesting: The tallest residential building in the world is Central Park Tower in NYC at 1,550 feet - that's a lot of tenants!",
    "Did you know? Housing courts didn't exist in most U.S. cities until the 1970s. Before that, disputes were handled in general civil courts.",
    "Fun fact: The U.S. has about 44 million rental households - that's roughly 1 in 3 Americans!",
    "Here's something neat: Medieval European cities had 'rent days' when everyone paid rent at the same time, often with public celebrations.",
    "Did you know? The federal minimum wage was created in 1938, but the federal minimum rent has never existed.",
    "Fun fact: In ancient Babylon (1754 BC), Hammurabi's Code included laws about rental properties and tenant rights!",
    "Interesting: The term 'apartment' comes from the Italian 'appartamento,' meaning 'a separated place.'",
    "Did you know? Section 8 was created in 1974 and now assists over 5 million families across the United States.",
    "Fun fact: The average U.S. rent has increased 145% since 2000, while wages increased only 68% in the same period.",
    "Here's a quirky law: In Minnesota, it's technically illegal for landlords to shut off heat between October 1 and April 30, even if tenant doesn't pay.",
    "Did you know? The concept of 'habitability' wasn't legally required in most states until the 1970s warranty of habitability movement.",
    "Fun fact: Cats are better tenants than dogs, statistically speaking - they cause 50% less property damage on average!",
    "Interesting: The most expensive rent in the world is in Hong Kong, averaging over $3,500 per month for a tiny 400 sq ft apartment.",
    "Did you know? The first apartment building in America was built in New York City in 1869. Before that, people rented floors in houses.",
    "Fun fact: In medieval England, rent was often paid in chickens, grain, or other goods rather than money!",
    "Here's something: The term 'studio apartment' originated in the 1920s when artists used them as combined living/work spaces.",
    "Did you know? The longest someone has lived in the same apartment is 82 years - Ruth Gottesman in NYC from 1936 to 2018!",
    "Fun fact: Landlords in ancient Rome provided public baths for tenants. Modern landlords rarely provide such luxuries!",
    "Interesting: The word 'lease' comes from the Latin 'laxare' meaning 'to loosen or let go.' You're 'let go' into the property!",
]


# Legal resource categories
LEGAL_CATEGORIES = {
    'tenant_rights': 'Tenant Rights & Protections',
    'landlord_duties': 'Landlord Responsibilities',
    'eviction_process': 'Eviction Process & Defense',
    'rent_control': 'Rent Control & Increases',
    'security_deposit': 'Security Deposits',
    'repairs_habitability': 'Repairs & Habitability',
    'discrimination': 'Fair Housing & Discrimination',
    'lease_terms': 'Lease Agreements & Terms',
    'court_procedures': 'Court Procedures & Filing',
    'local_ordinances': 'Local Ordinances & Codes',
    'federal_hud': 'HUD Regulations & Programs',
    'section_8': 'Section 8 Housing Choice Vouchers',
    'tenant_funding': 'Tenant Financial Assistance',
    'landlord_funding': 'Landlord Funding & Tax Credits',
    'emergency_rental': 'Emergency Rental Assistance',
    'fair_housing_act': 'Fair Housing Act (Federal)'
}


# Example legal resources (seed data)
SEED_LEGAL_RESOURCES = [
    {
        'title': 'Minnesota Tenant Rights Overview',
        'category': 'tenant_rights',
        'jurisdiction': 'Minnesota',
        'level': 'state',
        'summary': 'Comprehensive overview of tenant rights under Minnesota Statutes Chapter 504B',
        'key_facts': [
            'Landlords must provide 24-hour notice before entry (except emergencies)',
            'Security deposits must be returned within 21 days',
            'Tenants have right to withhold rent for uninhabitable conditions',
            'Retaliation for exercising rights is illegal'
        ],
        'citations': ['MN Stat § 504B.211', 'MN Stat § 504B.178', 'MN Stat § 504B.285'],
        'effective_date': '2024-01-01',
        'last_updated': datetime.now().isoformat()
    },
    {
        'title': 'Eviction Process in Minnesota',
        'category': 'eviction_process',
        'jurisdiction': 'Minnesota',
        'level': 'state',
        'summary': 'Step-by-step explanation of the eviction process in Minnesota courts',
        'key_facts': [
            'Landlord must serve proper notice (14 days for non-payment)',
            'Tenant has 7 days to answer eviction summons',
            'Court hearing typically within 7-14 days of filing',
            'Redemption period available in some cases'
        ],
        'citations': ['MN Stat § 504B.321', 'MN Stat § 504B.335'],
        'effective_date': '2024-01-01',
        'last_updated': datetime.now().isoformat()
    },
    {
        'title': 'Security Deposit Laws',
        'category': 'security_deposit',
        'jurisdiction': 'Minnesota',
        'level': 'state',
        'summary': 'Rules governing security deposits, interest, and returns',
        'key_facts': [
            'Landlord must provide itemized list of deductions',
            'Interest must be paid on deposits held over 1 year',
            'Failure to return deposit within 21 days = bad faith',
            'Tenant may recover 2x deposit plus attorney fees if landlord in bad faith'
        ],
        'citations': ['MN Stat § 504B.178'],
        'effective_date': '2024-01-01',
        'last_updated': datetime.now().isoformat()
    },
    {
        'title': 'Habitability Requirements',
        'category': 'repairs_habitability',
        'jurisdiction': 'Minnesota',
        'level': 'state',
        'summary': 'Minimum habitability standards landlords must maintain',
        'key_facts': [
            'Heat must be maintained at 68°F (October-May)',
            'Hot water temperature 110-130°F',
            'Working smoke and carbon monoxide detectors required',
            'Landlord must make repairs within 14 days of notice'
        ],
        'citations': ['MN Stat § 504B.161', 'Minneapolis Code § 244.2050'],
        'effective_date': '2024-01-01',
        'last_updated': datetime.now().isoformat()
    },
    {
        'title': 'Fair Housing Protections',
        'category': 'discrimination',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Protected classes under Fair Housing Act',
        'key_facts': [
            'Cannot discriminate based on race, color, religion, national origin',
            'Sex (including sexual harassment) is protected',
            'Familial status and disability are protected',
            'Minnesota adds sexual orientation, gender identity, and public assistance'
        ],
        'citations': ['42 U.S.C. § 3604', 'MN Stat § 363A.09'],
        'effective_date': '1968-04-11',
        'last_updated': datetime.now().isoformat()
    },
    {
        'title': 'HUD Housing Quality Standards',
        'category': 'federal_hud',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Federal minimum housing quality standards for HUD-assisted properties',
        'key_facts': [
            'All HUD housing must meet basic health and safety standards',
            'Annual inspections required for Section 8 properties',
            'Tenants can request special inspections for violations',
            'Landlords must make repairs within 24 hours (emergency) or 30 days (non-emergency)'
        ],
        'citations': ['24 CFR § 982.401', 'HUD Handbook 4350.3'],
        'effective_date': '2000-01-01',
        'last_updated': datetime.now().isoformat()
    },
    {
        'title': 'Section 8 Housing Choice Voucher Program',
        'category': 'section_8',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Overview of Section 8 voucher program for low-income tenants',
        'key_facts': [
            'Voucher pays portion of rent based on income (typically 30%)',
            'Tenant must find landlord who accepts Section 8',
            'Unit must pass HUD inspection before move-in',
            'Annual income recertification required',
            'Portability allows moving between jurisdictions'
        ],
        'citations': ['42 U.S.C. § 1437f', '24 CFR § 982'],
        'effective_date': '1974-08-22',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://www.hud.gov/topics/housing_choice_voucher_program_section_8'
    },
    {
        'title': 'Emergency Rental Assistance Program (ERAP)',
        'category': 'emergency_rental',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Federal funding for tenants struggling to pay rent due to COVID-19 or economic hardship',
        'key_facts': [
            'Covers past due rent, current rent, and future rent (up to 3 months)',
            'Also covers utilities and internet service',
            'No repayment required (not a loan)',
            'Tenant must demonstrate financial hardship',
            'Income must be at or below 80% area median income'
        ],
        'citations': ['American Rescue Plan Act of 2021', 'ERA1 and ERA2 Programs'],
        'effective_date': '2021-03-11',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/emergency-rental-assistance-program'
    },
    {
        'title': 'Low-Income Housing Tax Credit (LIHTC) for Landlords',
        'category': 'landlord_funding',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Federal tax credits for landlords who provide affordable housing',
        'key_facts': [
            'Largest source of affordable housing funding in U.S.',
            'Provides dollar-for-dollar reduction in federal tax liability',
            'Units must remain affordable for 15-30 years',
            'Rent limits tied to area median income',
            'Landlord must accept tenants at or below 60% AMI'
        ],
        'citations': ['26 U.S.C. § 42', 'IRS Revenue Procedure 2022-14'],
        'effective_date': '1986-01-01',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://www.irs.gov/credits-deductions/businesses/low-income-housing-tax-credit'
    },
    {
        'title': 'Minnesota Emergency Rental Assistance (RentHelpMN)',
        'category': 'tenant_funding',
        'jurisdiction': 'Minnesota',
        'level': 'state',
        'summary': 'State program providing emergency rental assistance to Minnesota tenants',
        'key_facts': [
            'Pays up to 18 months of past due and future rent',
            'Income must be at or below 80% area median income',
            'Must show pandemic-related hardship',
            'Application submitted by tenant or landlord',
            'Payment made directly to landlord'
        ],
        'citations': ['MN Dept of Employment and Economic Development'],
        'effective_date': '2021-03-01',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://www.renthelpmn.org'
    },
    {
        'title': 'Fair Housing Act - National Law',
        'category': 'fair_housing_act',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Federal law prohibiting housing discrimination',
        'key_facts': [
            'Prohibits discrimination in sale, rental, and financing of housing',
            'Protected classes: race, color, religion, national origin, sex, disability, familial status',
            'Applies to landlords, property managers, lenders, and real estate agents',
            'Tenants can file complaint with HUD within 1 year',
            'Violations can result in fines up to $100,000+'
        ],
        'citations': ['42 U.S.C. § 3601-3619', '24 CFR Part 100'],
        'effective_date': '1968-04-11',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_act_overview'
    },
    {
        'title': 'HUD Rental Assistance Programs Overview',
        'category': 'federal_hud',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Comprehensive overview of HUD rental assistance programs',
        'key_facts': [
            'Public Housing - government-owned properties for low-income families',
            'Section 8 Vouchers - tenant-based rental assistance',
            'Project-Based Section 8 - assistance tied to specific buildings',
            'Section 811 - housing for people with disabilities',
            'Section 202 - housing for elderly (62+)'
        ],
        'citations': ['24 CFR Parts 5, 880, 882, 960, 982'],
        'effective_date': '1937-09-01',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://www.hud.gov/topics/rental_assistance'
    },
    {
        'title': 'Landlord Participation in Section 8 - Requirements & Benefits',
        'category': 'landlord_funding',
        'jurisdiction': 'Federal',
        'level': 'federal',
        'summary': 'Guide for landlords on accepting Section 8 vouchers',
        'key_facts': [
            'Guaranteed monthly rent payment from housing authority',
            'Tenant responsible for their portion (usually 30% of income)',
            'Unit must pass HUD Housing Quality Standards inspection',
            'Annual inspections required',
            'Landlord can reject tenant for legitimate reasons (credit, rental history)',
            'Cannot reject solely because tenant has voucher (in many states)'
        ],
        'citations': ['24 CFR § 982.308', 'Local source of income protection laws'],
        'effective_date': '1974-08-22',
        'last_updated': datetime.now().isoformat(),
        'source_url': 'https://www.hud.gov/topics/housing_choice_voucher_program_section_8'
    }
]


def init_librarian(data_dir: str = 'data'):
    """Initialize librarian engine and seed library with default resources."""
    library_dir = os.path.join(data_dir, 'library')
    os.makedirs(library_dir, exist_ok=True)
    
    # Create index file
    index_path = os.path.join(library_dir, 'index.json')
    if not os.path.exists(index_path):
        index = {
            'categories': LEGAL_CATEGORIES,
            'resources': [],
            'last_updated': datetime.now().isoformat()
        }
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2)
    
    # Seed default resources
    for resource in SEED_LEGAL_RESOURCES:
        add_legal_resource(resource, data_dir)


def add_legal_resource(resource: Dict[str, Any], data_dir: str = 'data') -> str:
    """
    Add or update a legal resource in the library.
    
    Args:
        resource: Dict with title, category, jurisdiction, level, summary, key_facts, citations
        data_dir: Base data directory
    
    Returns:
        Resource ID
    """
    library_dir = os.path.join(data_dir, 'library')
    os.makedirs(library_dir, exist_ok=True)
    
    # Generate resource ID
    resource_id = hashlib.sha256(
        f"{resource['title']}{resource['jurisdiction']}{resource['category']}".encode()
    ).hexdigest()[:12]
    
    full_resource = {
        'resource_id': resource_id,
        'title': resource['title'],
        'category': resource['category'],
        'jurisdiction': resource['jurisdiction'],
        'level': resource.get('level', 'local'),  # federal, state, county, city, local
        'summary': resource['summary'],
        'key_facts': resource['key_facts'],
        'citations': resource.get('citations', []),
        'effective_date': resource.get('effective_date', ''),
        'source_url': resource.get('source_url', ''),
        'added_at': datetime.now().isoformat(),
        'last_updated': resource.get('last_updated', datetime.now().isoformat()),
        'tags': resource.get('tags', [])
    }
    
    # Save resource file
    resource_path = os.path.join(library_dir, f"{resource_id}.json")
    with open(resource_path, 'w') as f:
        json.dump(full_resource, f, indent=2)
    
    # Update index
    index_path = os.path.join(library_dir, 'index.json')
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    # Check if resource already in index
    existing = next((r for r in index['resources'] if r['resource_id'] == resource_id), None)
    if existing:
        existing.update({
            'title': resource['title'],
            'category': resource['category'],
            'jurisdiction': resource['jurisdiction'],
            'last_updated': datetime.now().isoformat()
        })
    else:
        index['resources'].append({
            'resource_id': resource_id,
            'title': resource['title'],
            'category': resource['category'],
            'jurisdiction': resource['jurisdiction'],
            'level': full_resource['level'],
            'last_updated': datetime.now().isoformat()
        })
    
    index['last_updated'] = datetime.now().isoformat()
    
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
    
    return resource_id


def search_library(query: str, category: Optional[str] = None, 
                  jurisdiction: Optional[str] = None, 
                  data_dir: str = 'data') -> List[Dict[str, Any]]:
    """
    Search library for relevant resources.
    
    Args:
        query: Search query
        category: Filter by category
        jurisdiction: Filter by jurisdiction
        data_dir: Base data directory
    
    Returns:
        List of matching resources
    """
    library_dir = os.path.join(data_dir, 'library')
    if not os.path.exists(library_dir):
        return []
    
    results = []
    query_lower = query.lower()
    
    for filename in os.listdir(library_dir):
        if filename.endswith('.json') and filename != 'index.json':
            with open(os.path.join(library_dir, filename), 'r') as f:
                resource = json.load(f)
            
            # Apply filters
            if category and resource.get('category') != category:
                continue
            if jurisdiction and resource.get('jurisdiction').lower() != jurisdiction.lower():
                continue
            
            # Search in title, summary, key_facts
            if (query_lower in resource.get('title', '').lower() or
                query_lower in resource.get('summary', '').lower() or
                any(query_lower in fact.lower() for fact in resource.get('key_facts', []))):
                results.append(resource)
    
    return results


def get_resource_by_id(resource_id: str, data_dir: str = 'data') -> Optional[Dict[str, Any]]:
    """Retrieve a specific resource by ID."""
    library_dir = os.path.join(data_dir, 'library')
    resource_path = os.path.join(library_dir, f"{resource_id}.json")
    
    if not os.path.exists(resource_path):
        return None
    
    with open(resource_path, 'r') as f:
        return json.load(f)


def get_resources_by_category(category: str, data_dir: str = 'data') -> List[Dict[str, Any]]:
    """Get all resources in a specific category."""
    return search_library('', category=category, data_dir=data_dir)


def get_resources_by_jurisdiction(jurisdiction: str, data_dir: str = 'data') -> List[Dict[str, Any]]:
    """Get all resources for a specific jurisdiction."""
    library_dir = os.path.join(data_dir, 'library')
    if not os.path.exists(library_dir):
        return []
    
    results = []
    jurisdiction_lower = jurisdiction.lower()
    
    for filename in os.listdir(library_dir):
        if filename.endswith('.json') and filename != 'index.json':
            with open(os.path.join(library_dir, filename), 'r') as f:
                resource = json.load(f)
            
            if resource.get('jurisdiction', '').lower() == jurisdiction_lower:
                results.append(resource)
    
    return results


def generate_info_card(resource_id: str, data_dir: str = 'data') -> Optional[Dict[str, Any]]:
    """
    Generate a user-friendly information card from a legal resource.
    
    Returns:
        Dict with title, summary, key_points, what_it_means, next_steps
    """
    resource = get_resource_by_id(resource_id, data_dir)
    if not resource:
        return None
    
    # Convert key facts to plain language
    key_points = []
    for fact in resource.get('key_facts', []):
        key_points.append(fact)
    
    # Generate "what it means for you" section
    category = resource.get('category', '')
    what_it_means = f"This {LEGAL_CATEGORIES.get(category, 'information')} applies to your situation."
    
    if category == 'tenant_rights':
        what_it_means = "You have these protections under the law. Your landlord must follow these rules."
    elif category == 'eviction_process':
        what_it_means = "If you receive an eviction notice, you have specific rights and deadlines to respond."
    elif category == 'security_deposit':
        what_it_means = "Your security deposit is protected. Your landlord must follow these rules when returning it."
    elif category == 'repairs_habitability':
        what_it_means = "Your home must meet these minimum standards. Your landlord is required to make repairs."
    elif category == 'section_8':
        what_it_means = "If you have a Section 8 voucher, you have rights and responsibilities. Your landlord must meet HUD standards."
    elif category == 'tenant_funding':
        what_it_means = "You may qualify for financial assistance to help with rent, utilities, or moving costs. Apply as soon as possible."
    elif category == 'landlord_funding':
        what_it_means = "Landlords can access tax credits and funding programs. This may help you negotiate with your landlord or find affordable housing."
    elif category == 'emergency_rental':
        what_it_means = "If you're struggling to pay rent, emergency assistance is available. No repayment required - it's not a loan."
    elif category == 'federal_hud':
        what_it_means = "HUD sets minimum standards for housing quality. If you live in HUD-assisted housing, these rules protect you."
    elif category == 'fair_housing_act':
        what_it_means = "Federal law protects you from discrimination. If you believe you've been discriminated against, you can file a complaint."
    
    # Generate next steps
    next_steps = [
        "Save this information to your vault",
        "Document any violations with photos and dates",
        "Keep copies of all communications with your landlord"
    ]
    
    if category == 'eviction_process':
        next_steps = [
            "Read the eviction notice carefully and note deadlines",
            "Respond within 7 days if you receive a summons",
            "Gather evidence (lease, rent receipts, communications)",
            "Consider contacting a tenant rights organization or attorney"
        ]
    elif category == 'section_8':
        next_steps = [
            "Contact your local Public Housing Authority (PHA)",
            "Complete application and provide income verification",
            "Request landlord participation information",
            "Ensure unit passes HUD inspection before signing lease"
        ]
    elif category == 'tenant_funding':
        next_steps = [
            "Apply online or contact your local assistance program",
            "Gather documents: ID, lease, income proof, hardship documentation",
            "Work with your landlord - they may need to submit documents too",
            "Follow up on application status regularly"
        ]
    elif category == 'emergency_rental':
        next_steps = [
            "Apply immediately - funds are limited and first-come-first-served",
            "Provide landlord contact information",
            "Submit proof of income and hardship",
            "Check application status every few days"
        ]
    elif category == 'landlord_funding':
        next_steps = [
            "If you're a tenant: Ask your landlord if they participate in these programs",
            "If your landlord uses tax credits, your unit may have rent limits",
            "For Section 8: Confirm landlord accepts vouchers before applying",
            "Document all program participation for your records"
        ]
    elif category == 'fair_housing_act':
        next_steps = [
            "Document the discriminatory action (date, time, what was said/done)",
            "File complaint with HUD within 1 year at hud.gov/fairhousing",
            "Save all emails, texts, and notices as evidence",
            "Consider contacting a fair housing organization for help"
        ]
    
    return {
        'resource_id': resource_id,
        'title': resource['title'],
        'category': LEGAL_CATEGORIES.get(category, category),
        'jurisdiction': resource['jurisdiction'],
        'summary': resource['summary'],
        'key_points': key_points,
        'what_it_means': what_it_means,
        'next_steps': next_steps,
        'citations': resource.get('citations', []),
        'last_updated': resource.get('last_updated', '')
    }


def get_relevant_resources_for_situation(situation: Dict[str, Any], 
                                        data_dir: str = 'data') -> List[Dict[str, Any]]:
    """
    Get relevant legal resources based on user's situation.
    
    Args:
        situation: Dict with issue_type, urgency, jurisdiction, details
        data_dir: Base data directory
    
    Returns:
        List of relevant info cards
    """
    issue_type = situation.get('issue_type', '')
    jurisdiction = situation.get('jurisdiction', 'Minnesota')
    
    # Map issue types to categories
    category_map = {
        'eviction': 'eviction_process',
        'repairs': 'repairs_habitability',
        'deposit': 'security_deposit',
        'rent_increase': 'rent_control',
        'discrimination': 'discrimination',
        'lease': 'lease_terms',
        'section_8': 'section_8',
        'financial_help': 'tenant_funding',
        'emergency_rent': 'emergency_rental',
        'hud': 'federal_hud'
    }
    
    category = category_map.get(issue_type)
    
    if category:
        resources = get_resources_by_category(category, data_dir)
    else:
        resources = get_resources_by_jurisdiction(jurisdiction, data_dir)
    
    # Generate info cards
    cards = []
    for resource in resources[:5]:  # Limit to top 5
        card = generate_info_card(resource['resource_id'], data_dir)
        if card:
            cards.append(card)
    
    return cards


def update_library_from_source(source_url: str, jurisdiction: str, 
                               data_dir: str = 'data') -> Dict[str, Any]:
    """
    Update library from external source (placeholder for future API integration).
    
    Args:
        source_url: URL to legal resource API
        jurisdiction: Jurisdiction to update
        data_dir: Base data directory
    
    Returns:
        Dict with update status
    """
    # TODO: Implement actual API integration
    # For now, return placeholder
    return {
        'status': 'placeholder',
        'message': 'External source integration coming soon',
        'jurisdiction': jurisdiction,
        'source_url': source_url,
        'timestamp': datetime.now().isoformat()
    }


def get_daily_fun_fact() -> Dict[str, Any]:
    """
    The Librarian shares a daily fun fact.
    Uses date as seed so same fact appears for everyone on the same day.
    
    Returns:
        Dict with fact, date, and librarian_message
    """
    # Use today's date as seed for consistent daily fact
    today = datetime.now().date()
    seed = int(today.strftime('%Y%m%d'))
    random.seed(seed)
    
    fact = random.choice(FUN_FACTS)
    
    # Librarian personality messages
    greetings = [
        "Good day! Your friendly neighborhood Librarian here.",
        "Hello there! The Librarian has something interesting for you.",
        "Greetings! The Library is always full of surprises.",
        "Welcome! Let me share something fascinating.",
        "Good to see you! I've been reading and found this gem:",
    ]
    
    random.seed(seed + 1)  # Different seed for greeting
    greeting = random.choice(greetings)
    
    return {
        'date': today.isoformat(),
        'greeting': greeting,
        'fact': fact,
        'librarian_says': f"{greeting} {fact}"
    }


def get_librarian_greeting() -> str:
    """Get a personalized greeting from the Librarian."""
    hour = datetime.now().hour
    
    if hour < 12:
        time_greeting = "Good morning"
    elif hour < 17:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"
    
    personalities = [
        f"{time_greeting}! The Librarian is here to help you navigate the law.",
        f"{time_greeting}! Welcome to the Library. Knowledge is power!",
        f"{time_greeting}! Let's find the information you need.",
        f"{time_greeting}! The Library's resources are at your disposal.",
    ]
    
    return random.choice(personalities)


# Demo/test
if __name__ == "__main__":
    print("Librarian Engine - Demo\n")
    
    # Initialize library
    init_librarian()
    print("✅ Library initialized with seed resources\n")
    
    # Search for eviction resources
    print("Searching for 'eviction'...")
    results = search_library('eviction')
    print(f"Found {len(results)} resources\n")
    
    for resource in results:
        print(f"📚 {resource['title']}")
        print(f"   Category: {resource['category']}")
        print(f"   Jurisdiction: {resource['jurisdiction']}")
        print()
    
    # Generate info card
    if results:
        print("Generating info card for first result...")
        card = generate_info_card(results[0]['resource_id'])
        print(f"\n📋 {card['title']}")
        print(f"Summary: {card['summary']}")
        print(f"\nKey Points:")
        for point in card['key_points']:
            print(f"  • {point}")
        print(f"\nWhat it means: {card['what_it_means']}")
        print(f"\nNext Steps:")
        for step in card['next_steps']:
            print(f"  {step}")
    
    # Get resources for a situation
    print("\n\nGetting resources for eviction situation...")
    situation = {
        'issue_type': 'eviction',
        'jurisdiction': 'Minnesota',
        'urgency': 'high'
    }
    cards = get_relevant_resources_for_situation(situation)
    print(f"Found {len(cards)} relevant resources")
