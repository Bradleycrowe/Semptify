# Semptify FastAPI Redesign Plan

## Phase 0: Define the Foundation

### 1. The Original Problem
What situation or frustration drove you to create Semptify?
- [ ] Personal experience as a tenant?
- [ ] Seeing others struggle with landlord disputes?
- [ ] Lack of affordable legal help?
- [ ] Other: _______________

### 2. Who Is Semptify For?
- [ ] Tenants facing eviction
- [ ] Anyone renting who wants to protect themselves
- [ ] Low-income renters specifically
- [ ] Geographic focus: _______________

### 3. The Core Promise
In one sentence, what does Semptify do for the user?
> _____________________________________________

### 4. What Success Looks Like
When a user finishes using Semptify, what have they achieved?
- [ ] A court-ready evidence packet
- [ ] Knowledge of their rights
- [ ] Filed complaint with proper authorities
- [ ] Other: _______________

---

## Current Flask Semptify: Lessons Learned

### ✅ Keep (Good Patterns)
| Pattern | Why It Works |
|---------|--------------|
| Intensity Engine UX | Adaptive UI based on user urgency |
| Vault document certification | SHA-256 hashing, JSON certificates |
| Modular blueprints | Separation of concerns |
| Security layers | Token auth, rate limiting, CSRF |
| Timeline/Calendar integration | Core user value |

### ⚠️ Fix (Problematic Patterns)
| Problem | Root Cause | FastAPI Solution |
|---------|------------|------------------|
| 6 base templates | No design system | Single base + components |
| 339 Python files | Feature sprawl, no structure | Organized `/app` folder structure |
| 96 route files | No clear module boundaries | Domain-driven routers |
| Inline CSS everywhere | No style architecture | Tailwind or CSS modules |
| Mixed auth approaches | Evolved organically | Single auth dependency |
| Sync blocking on AI calls | Flask limitations | Native async |

---

## Proposed FastAPI Architecture

```
Semptify-FastAPI/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── core/
│   │   ├── config.py           # Settings (pydantic)
│   │   ├── security.py         # Auth, tokens, rate limits
│   │   └── database.py         # Async SQLite/Postgres
│   ├── routers/
│   │   ├── auth.py             # /register, /login, /token
│   │   ├── vault.py            # /vault/* document storage
│   │   ├── timeline.py         # /timeline/* events
│   │   ├── calendar.py         # /calendar/* scheduling
│   │   ├── copilot.py          # /api/copilot AI features
│   │   ├── complaints.py       # /complaints/* filing
│   │   └── admin.py            # /admin/* management
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── event.py
│   ├── services/               # Business logic (engines)
│   │   ├── intensity_engine.py
│   │   ├── document_service.py
│   │   └── ai_service.py
│   └── templates/              # Jinja2 (FastAPI supports it)
│       ├── base.html           # ONE base template
│       ├── components/         # Reusable pieces
│       └── pages/              # Full pages
├── static/
├── tests/
├── requirements.txt
└── README.md
```

---

## Migration Strategy

### Phase 1: Core Foundation
- [ ] Create project scaffold
- [ ] Implement `core/config.py` with Pydantic settings
- [ ] Implement `core/security.py` (tokens, rate limiting)
- [ ] Implement `core/database.py` (async SQLite)

### Phase 2: Auth & Users
- [ ] Anonymous token registration (like current)
- [ ] User token validation
- [ ] Admin token system

### Phase 3: Document Vault
- [ ] File upload with SHA-256 certification
- [ ] JSON certificate generation
- [ ] Download/retrieval

### Phase 4: Timeline & Calendar
- [ ] Event storage and retrieval
- [ ] Calendar integration
- [ ] Deadline tracking

### Phase 5: AI Copilot
- [ ] Async AI provider calls
- [ ] Multiple provider support (OpenAI, Azure, Ollama)

### Phase 6: Complaints & Court Packets
- [ ] Multi-step wizard
- [ ] PDF generation
- [ ] Evidence compilation

### Phase 7: Admin & Observability
- [ ] Admin dashboard
- [ ] Metrics endpoint
- [ ] Health checks

---

## Design Decisions to Make

1. **Database**: SQLite (simple) vs PostgreSQL (scalable)?
2. **Frontend**: Keep Jinja2 templates or go API-only + separate frontend?
3. **CSS Framework**: Bootstrap (current) vs Tailwind vs something else?
4. **Hosting**: Render (current) vs other options?

---

## Next Steps

1. Answer the foundation questions above
2. Prioritize which features are MVP vs nice-to-have
3. Start building Phase 1: Core Foundation
