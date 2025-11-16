HOW SEMPTIFY ADDRESSES YOUR REQUIREMENTS
=========================================
Last updated: 2025-11-15 19:09

REQUIREMENT 1: Official Sources Only (.gov)
-------------------------------------------
Module: official_sources.py
- ALLOWED_OFFICIAL_DOMAINS: revisor.mn.gov, mncourts.gov, *.mn.gov, *.gov
- is_official_source(url): Validates every citation against .gov patterns
- OFFICIAL_ONLY flag: Environment-controlled, defaults to True
- Used by: realtime_research_engine.py for all citations

Result: Every legal claim cites revisor.mn.gov (MN official statutes)


REQUIREMENT 2: Conflict Resolution (Federal vs State)
-----------------------------------------------------
Module: legal_conflict_resolver.py
- Implements Supremacy Clause hierarchy:
  1. U.S. Constitution
  2. Federal statutes
  3. Federal regulations
  4. State constitutions & statutes
  5. Local ordinances
  6. Private contracts
  
- Preemption types: Express, Field, Conflict, Obstacle
- Default for landlord-tenant: FLOOR model
  (Federal sets minimum, states can add protections)
  
- analyze_preemption() returns structured decision logic
- Used by: realtime_research_engine.py in every response

Result: When MN and federal laws conflict, system explains which applies and why


REQUIREMENT 3: Real-Time Research
----------------------------------
Module: realtime_research_engine.py
- Fetches current MN statutes during "researching your options" phase
- research_holdover_rights(state='MN'):
  * Checks 504B.141, 504B.135, 504B.285, 504B.291, 504B.301, 504B.311
  * Validates URLs with is_official_source()
  * Extracts short quotes from statute pages
  * Runs preemption analysis
  * Returns citations + presentations (grouped state/federal)
  
- Timestamps: Every citation includes checked_date
- Used by: journey_routes.py /api/journey/respond

Result: Live lookup of current laws, not cached/stale data


REQUIREMENT 4: Context-Aware (Intent, Purpose, Outlook)
--------------------------------------------------------
Module: housing_journey_engine.py
- 7 stages: looking, applying, signed_lease, in_lease, ending_lease, ended_lease, eviction
- Stage-specific questions capture:
  * Factual context (dates, notices, payments)
  * Intent (what they want to happen)
  * Emotional state (worried, confident)
  * Relationship dynamics (landlord communication)
  
- Keyword detection triggers capabilities:
  holdover → holdover_rights
  eviction → eviction_defense
  deposit → security_deposit_recovery
  
- Used by: journey_routes.py to personalize research

Result: System grows capabilities based on user's actual situation


REQUIREMENT 5: UI Presentation (State says X, Federal says Y)
-------------------------------------------------------------
Module: templates/housing_journey.html
- "What the law says" section with:
  * State law says: [quote from MN statute]
  * Federal law says: [quote from federal statute]
  * Disclaimer: "This is not legal advice. Consult an attorney."
  
- "Official Sources" panel with:
  * Verified: Official Government Source
  * Last checked timestamp
  * Links to revisor.mn.gov
  
- "Thank you for your patience, we are researching your options..."
  (shown during real-time lookup)

Result: Clear, cited, non-advice presentation


REQUIREMENT 6: Seed Growth System
----------------------------------
Module: seed_core.py
- analyze_need(user_input, facts) detects keywords
- generate_engine_code(capability) creates Python modules
- Example: holdover_tenant → generates MN-specific rights analyzer
  
- Used by: journey_routes.py calls seed_manager.process_user_input()
- Storage: simulated_buckets/<session_id>/semptify-seed/engines/

Result: System writes its own code based on detected needs


GAPS IDENTIFIED
---------------
1. Quote extraction from revisor.mn.gov not yet tested
2. UI 'What the law says' section needs testing
3. Federal statute lookup not yet implemented (only state)
4. Local ordinances (city/county) not yet integrated
5. No recent court case lookup (only statutes)


NEXT STEPS TO COMPLETE
-----------------------
1. Test /api/journey/respond returns presentations
2. Verify UI renders 'State law says' with quotes
3. Add federal statute lookup (if needed for user's case)
4. Test full flow: stage selection → questions → research → citations
5. Verify disclaimer always shows when legal content present
