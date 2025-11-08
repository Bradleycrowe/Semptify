# Curiosity-Driven Learning System

## Overview
The app learns through **curiosity** - it asks questions, researches answers, and improves itself continuously.

---

## How It Works

### 1. **Curiosity Triggers** (What makes the app curious)

#### **Prediction Failure**
- App predicts outcome
- Reality is different
- **Curiosity**: "Why was I wrong?"
- Researches missing factors
- Updates model

#### **Anomaly Detection**
- Normal pattern: 60% retaliation
- Unusual case: 5% retaliation
- **Curiosity**: "Why is this different?"
- Researches unique factors
- Discovers new strategy

#### **Knowledge Gap**
- User asks question
- App has no data
- **Curiosity**: "What's the answer?"
- Researches multiple sources
- Builds knowledge base

#### **User Correction**
- App suggests path A
- User does path B (and succeeds)
- **Curiosity**: "Why did their way work better?"
- Researches user's approach
- Updates recommendations

---

## Research Methods

### **Sources**
- User outcome data
- Public records
- Court documents
- Pattern analysis
- Cross-validation (5 sources)

### **Process**
1. Generate question
2. Identify research paths
3. Collect data
4. Validate findings
5. Integrate into knowledge base
6. Update predictions

---

## Self-Improvement Loop

```
OBSERVE → GET CURIOUS → RESEARCH → LEARN → IMPROVE → REPEAT
```

### **Example: Learning About Retaliation**

**Week 1**: App knows nothing
- Sees 10 retaliation cases
- **Curiosity**: "What factors predict retaliation?"

**Week 2**: Basic pattern found
- Learns: "ABC Management retaliates 60% of time"
- **Curiosity**: "Why do 40% NOT get retaliated against?"

**Week 3**: Protective factors discovered
- Finds: 4 users had media coverage
- **Curiosity**: "Does media protect from retaliation?"

**Week 4**: Theory tested
- Validates: Media coverage = 75% protection
- **New recommendation**: "Notify local news for protection"

**Month 2**: Continuous refinement
- Tracks success rate of new recommendation
- **Curiosity**: "Which news outlets are most effective?"
- Refines: "KCRA = 90% protection, others = 60%"

---

## Knowledge Base Growth

### **Facts** (Verified knowledge)
- Average repair cost: $1,800
- Legal filing deadlines by jurisdiction
- Successful strategies by case type

### **Patterns** (Observed behaviors)
- Landlords with contractor licenses respond faster
- Retaliation happens within 30 days
- Dual complaints (health + rent board) = better outcomes

### **Theories** (Being tested)
- "Theory: Filing on 1st of month reduces retaliation"
- Status: Testing with 15 cases
- Confidence: 65% (needs more data)

---

## Integration with Other Systems

### **Jurisdiction Engine**
- Curiosity: "Why do city laws override state?"
- Research: Legal hierarchy
- Learn: Most protective law wins

### **Perspective Engine**
- Curiosity: "What makes a landlord cooperative?"
- Research: Compare good vs bad landlords
- Learn: Contractor license = predictor

### **Intelligence Engine**
- Curiosity: "Why did prediction fail?"
- Research: Missing context
- Learn: Add new factors to model

---

## User Benefits

### **Before Curiosity**
- App gives generic advice
- Predictions based on limited data
- One-size-fits-all suggestions

### **With Curiosity**
- App learns from every case
- Predictions improve continuously
- Personalized strategies from similar successes
- Warns of pitfalls from similar failures

---

## Example: Real Learning Scenario

**User Case**: Mold complaint

**App's Journey**:

1. **Initial Knowledge**: "File complaint, wait 30 days"

2. **Prediction Failure**: User lost case
   - **Curiosity**: "Why did they lose?"
   - **Research**: Found improper service method
   - **Learning**: Service method matters more than thought

3. **Anomaly Found**: One user got repair in 2 days
   - **Curiosity**: "How did they get such fast action?"
   - **Research**: They filed with health dept, not rent board
   - **Learning**: Health hazards = health dept is faster

4. **User Correction**: User added media
   - **Curiosity**: "Did media help?"
   - **Research**: Compare with-media vs without
   - **Learning**: Media reduces retaliation by 75%

5. **Knowledge Gap**: "How much does remediation cost?"
   - **Curiosity**: "What's typical cost?"
   - **Research**: Aggregate from court awards
   - **Learning**: $800-$3,500, average $1,800

6. **New Recommendation** (evolved through curiosity):
   ```
   OLD: "File complaint and wait"

   NEW: "For mold:
   1. Document (10+ photos)
   2. File with Health Dept (faster than rent board)
   3. Notify KCRA or Fox 40 (75% retaliation protection)
   4. Expect $1,800 cost (use in claim)
   5. Service by hand with witness (87% court acceptance)"
   ```

---

## Continuous Learning

### **Daily**
- Evaluate predictions
- Detect anomalies
- Generate new questions

### **Weekly**
- Research high-priority questions
- Validate patterns
- Update recommendations

### **Monthly**
- Performance review
- Theory testing
- Knowledge base expansion

---

## Privacy & Ethics

### **What Gets Learned**
- ✅ Patterns (anonymous aggregates)
- ✅ Successful strategies
- ✅ Legal outcomes
- ✅ Cost averages

### **What Stays Private**
- ❌ Individual identities
- ❌ Personal details
- ❌ Location beyond city level
- ❌ Sensitive communications

---

## Files

- **curiosity_engine.py**: Core learning system
- **demo_curiosity.py**: Working examples
- **data/research_questions.json**: Pending questions
- **data/learned_knowledge.json**: Knowledge base

---

## Key Principle

> **"The app that asks questions becomes smarter than the app that just processes data."**

Curiosity drives:
- Self-improvement
- Adaptation
- Innovation
- Better user outcomes

---

## Next Steps

1. Wire curiosity into data_flow_engine
2. Trigger curiosity on prediction failures
3. Research questions automatically
4. Update user recommendations
5. Track improvement over time

**Result**: App that gets smarter every day through curiosity.
