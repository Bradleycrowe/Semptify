# Semptify: Complete Learning Integration

## Overview
**Semptify** is now a **self-learning tenant sidekick** that gets smarter with every user interaction.

---

## 🧠 Intelligence Stack (All Integrated)

### **1. Learning Engine** (`learning_engine.py`)
- **What**: Learns patterns from user behavior
- **Example**: "85% who send written notice first win their case"
- **Wired into**: Data flow, journey tracking, outcomes

### **2. Curiosity Engine** (`curiosity_engine.py`)
- **What**: Asks questions and researches answers
- **Example**: "Why did prediction fail? → Research → Learn missing factor"
- **Wired into**: Prediction failures, anomalies, knowledge gaps

### **3. Intelligence Engine** (`intelligence_engine.py`)
- **What**: Connects related information (address → owner → violations → history)
- **Example**: "ABC Management → 12 complaints → 60% retaliation → warn user"
- **Wired into**: Entity lookups, risk assessment

### **4. Jurisdiction Engine** (`jurisdiction_engine.py`)
- **What**: Determines which laws apply (federal/state/county/city hierarchy)
- **Example**: "City 72-hour law overrides state 30-day law (more protective)"
- **Wired into**: Legal guidance, procedural correctness

### **5. Tenant Journey** (`tenant_journey.py`) **← NEW!**
- **What**: Tracks complete tenant experience, applies ALL intelligence at each stage
- **Example**: "Searching → Applying → Signing → Living → Issue → Resolution"
- **Wired into**: ALL above systems + user timeline

---

## 🗺️ Tenant Journey Stages

```
1. SEARCHING
   ↓ [Learning: Check landlord reputation, area intel]

2. APPLYING
   ↓ [Intelligence: Lookup agency, compare fees, warn of issues]

3. SCREENING
   ↓ [Waiting period]

4. APPROVED
   ↓ [Success checkpoint]

5. SIGNING
   ↓ [Jurisdiction: Legal limits, Learning: Problematic clauses]

6. MOVING_IN
   ↓ [Learning: What others forget to document]

7. LIVING
   ↓ [Monitoring, documentation]

8. ISSUE (Problem arises)
   ↓ [ALL SYSTEMS ACTIVATE]
   |
   ├─ Jurisdiction: Legal process for this issue
   ├─ Intelligence: Similar cases & outcomes
   ├─ Learning: Successful strategies
   └─ Curiosity: Research if low data

9. RESOLVING
   ↓ [Real-time guidance, pattern matching]

10. MOVING_OUT
    ↓ [Security deposit protection]

11. DISPUTE
    ↓ [Legal pathways]

12. CLOSED
    └─ [Record outcome → Feed back to learning systems]
```

---

## 🔄 Complete Learning Loop

### **How It Works:**

```
USER ACTION
    ↓
JOURNEY TRACKER records it
    ↓
LEARNING ENGINE observes pattern
    ↓
INTELLIGENCE ENGINE connects to related data
    ↓
JURISDICTION ENGINE validates legal correctness
    ↓
GUIDANCE provided to user
    ↓
USER OUTCOME
    ↓
CURIOSITY ENGINE evaluates:
  - Was prediction correct?
  - Any anomalies?
  - Knowledge gaps?
    ↓
RESEARCH & LEARN
    ↓
UPDATE MODELS
    ↓
NEXT USER gets BETTER guidance
```

---

## 📊 Example: Complete Flow

### **User: Sarah**

#### **Stage 1: Searching** (Day 1)
```
Sarah: POST /api/journey/start
{
  "location": {"city": "sacramento_city", "zip": "95814"},
  "context": {"looking_for": "2br", "budget": 1800}
}

App Response:
{
  "journey_id": "journey_sarah_123",
  "guidance": [
    {
      "type": "warning",
      "title": "Area Intelligence",
      "message": "Based on 47 reports in 95814:",
      "insights": [
        "Average rent: $1,650 (your budget is reasonable)",
        "3 properties have high complaint rates",
        "Health hazards reported: mold (8 cases)"
      ]
    }
  ]
}
```

#### **Stage 2: Applying** (Day 3)
```
Sarah: POST /api/journey/journey_sarah_123/advance
{
  "new_stage": "applying",
  "data": {
    "agency": "ABC Property Management",
    "address": "123 Main St",
    "application_fee": 75
  }
}

🧠 App LEARNS:
- Stores: ABC Management charges $75 fee at 123 Main

🔍 Intelligence CHECKS:
- Lookup ABC Management
- Finds: 12 past reports, 8 illegal fee charges, 60% retaliation rate

⚖️ Jurisdiction VALIDATES:
- California max fee (2025): $58.23
- Sarah's fee: $75 = ILLEGAL ($16.77 over)

App Response:
{
  "guidance": [
    {
      "type": "critical",
      "title": "🚨 ILLEGAL APPLICATION FEE",
      "message": "ABC charged $75, legal max is $58.23",
      "action": "Document this. You can recover overage + penalties."
    },
    {
      "type": "warning",
      "title": "ABC Management - Known Issues",
      "learned_from": "12 tenant reports",
      "issues": [
        "8 cases of illegal fees",
        "60% retaliation rate after complaints",
        "Average case resolution: 4.2 months"
      ],
      "recommendation": "DOCUMENT EVERYTHING from now on"
    }
  ]
}
```

#### **Stage 3: Issue** (Month 2)
```
Sarah: POST /api/journey/journey_sarah_123/advance
{
  "new_stage": "issue",
  "data": {
    "issue_type": "mold",
    "landlord": "ABC Property Management",
    "severity": "health_hazard"
  }
}

🎯 ALL SYSTEMS ACTIVATE:

⚖️ JURISDICTION:
- City ordinance: 72 hours for health hazards
- State law: 30 days (city is stricter → city applies)

📊 INTELLIGENCE (similar cases):
- 15 mold cases against ABC Management
- Success rate: 85% (with proper evidence)
- Average resolution: 3.2 months
- Common pitfall: 70% lost due to improper service of notice

📚 LEARNING (successful strategies):
- Users who filed dual complaints (health + rent board): 90% success
- Users with media coverage: 75% protection from retaliation
- Hand delivery + witness: 87% court acceptance vs 72% certified mail

🤔 CURIOSITY (if prediction fails later):
- Will ask: "Why did ABC ignore 72-hour deadline in Sarah's case?"
- Research: Compare to past ABC behavior
- Learn: Update ABC's compliance pattern

App Response:
{
  "guidance": [
    {
      "type": "legal",
      "title": "Legal Process",
      "applicable_law": {
        "statute": "City Ordinance §8.100.070",
        "requirement": "Repair within 72 hours (health hazard)",
        "jurisdiction": "Sacramento City (overrides state 30-day)"
      },
      "steps": [
        "1. Document (10+ photos, timestamps)",
        "2. Send written notice (hand delivery + witness)",
        "3. Wait 72 hours",
        "4. File dual complaints (Health Dept + Rent Board)"
      ]
    },
    {
      "type": "intelligence",
      "title": "Intelligence from 15 Similar Cases",
      "success_rate": "85% (with proper evidence)",
      "strategies": [
        "Dual filing (health + rent) = 90% success",
        "Media coverage = 75% retaliation protection",
        "Hand delivery = 87% court acceptance"
      ],
      "warnings": [
        "ABC Management history: 60% retaliation rate",
        "Expect retaliation within 30 days (8 of 12 cases)",
        "Common pitfall: Improper service (70% of losses)"
      ]
    },
    {
      "type": "recommendation",
      "title": "Your Action Plan",
      "actions": [
        "TODAY: Photos (10+), video, timeline",
        "DAY 1: Hand-deliver notice (bring witness)",
        "DAY 3: If no response, file with Health Dept",
        "DAY 3: File with Rent Board (dual filing)",
        "DAY 3: Send copy to KCRA/Fox 40 (media protection)",
        "ONGOING: Document all communication"
      ]
    }
  ]
}
```

#### **Stage 4: Outcome** (Month 4)
```
Sarah: POST /api/journey/journey_sarah_123/outcome
{
  "outcome_type": "resolved",
  "outcome_data": {
    "resolution": "Repair completed after health dept inspection",
    "time_taken_days": 18,
    "landlord_response": "complied after inspection",
    "retaliation": false,
    "satisfaction": "high",
    "used_media": true,
    "used_dual_filing": true
  }
}

🧠 APP LEARNS:
- Media coverage worked (no retaliation)
- Dual filing + health dept = fast resolution (18 days vs 3.2 month avg)
- ABC Management DOES comply when health dept involved

📈 PREDICTIONS IMPROVE:
- Update: "ABC Management + Health Dept involvement = 90% compliance"
- Update: "Media coverage reduces retaliation from 60% to 10%"
- Update: "Average resolution with this strategy: 18 days (vs 3.2 months)"

🎯 NEXT USER BENEFITS:
- Gets Sarah's successful strategy automatically
- Warned that media is KEY protection
- Told to expect 18-day resolution (not 3 months)
```

---

## 🚀 API Endpoints

### **Journey Management**
- `POST /api/journey/start` - Start tracking
- `POST /api/journey/<id>/advance` - Move to next stage
- `GET /api/journey/<id>/guidance` - Get intelligent guidance
- `POST /api/journey/<id>/outcome` - Record outcome (triggers learning)
- `GET /api/journey/<id>` - Get full journey details

### **Learning**
- `POST /api/learning/observe` - Record action
- `GET /api/learning/patterns` - Get learned patterns
- `GET /api/learning/suggestions` - Get AI suggestions

### **Intelligence**
- `POST /api/intelligence/lookup` - Lookup entity (landlord, agency, address)
- `GET /api/intelligence/similar` - Find similar situations

---

## 🔑 Key Features

### **1. Situational Awareness**
User enters ONE piece of info (address, agency name, etc.)
→ App finds EVERYTHING related and warns of problems

### **2. Predictive Intelligence**
Based on similar cases: "Users with your situation had 85% success doing X"

### **3. Procedural Correctness**
Ensures legal compliance, correct order, no skipped steps

### **4. Perspective Analysis**
Shows situation from tenant, landlord, judge viewpoints

### **5. Cost Analysis**
Calculates: filing fees, time, recovery, net outcome

### **6. Guard Rails**
Prevents mistakes: "STOP - you're missing critical evidence"

### **7. Curiosity-Driven Learning**
App asks "why?" when wrong, researches, improves continuously

---

## 💡 The Magic

**Every user makes the app smarter for the NEXT user.**

Sarah's successful mold case → Next tenant with ABC Management gets:
- Shorter resolution time estimate (18 days vs 3 months)
- Media protection strategy (proven effective)
- Dual filing recommendation (90% success rate)
- No wasted time on ineffective approaches

---

## Files Created

### **Core Systems**
- `tenant_journey.py` - Journey tracker with all intelligence
- `journey_routes.py` - API endpoints
- `learning_engine.py` - Pattern learning
- `curiosity_engine.py` - Self-learning through questions
- `intelligence_engine.py` - Entity intelligence & connections
- `jurisdiction_engine.py` - Legal hierarchy & procedural correctness
- `perspective_engine.py` - Multi-angle analysis

### **Integration**
- `Semptify.py` - Updated to register journey blueprint
- All systems auto-initialize on first use

### **Documentation**
- `CURIOSITY_LEARNING_SYSTEM.md` - How curiosity works
- This file - Complete integration guide

---

## Next Steps

1. **Test the journey flow**
2. **Add more stage guidance** (currently has: searching, applying, signing, moving_in, issue)
3. **Connect to existing modules** (vault, calendar, ledger)
4. **Train on real data** as users use the system
5. **Monitor learning** - track accuracy improvements over time

---

## Result

**Semptify learns about every tenant's journey:**
- Where they struggle
- What works
- What doesn't
- Why outcomes differ
- How to improve

**And becomes a smarter sidekick for every new tenant.** 🎯✨
