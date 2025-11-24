# Attorney Directory - Future Feature

## Status: Planned for Post-MVP

### Feature Requirements

**Goal:** Help users find qualified tenant rights attorneys in Minnesota

**Core Functionality:**
- Search by city/county
- Filter by practice area (eviction defense, habitability, discrimination)
- Display attorney profiles (name, firm, phone, email, years experience)
- Show ratings/reviews if available
- Integration with case data (suggest attorneys based on case type)

### Implementation Options Researched

1. **Minnesota State Bar Association API** - Official directory, requires API key
2. **Avvo API** - Commercial marketplace, partnership required
3. **Justia Directory** - Public but no official API
4. **Curated JSON List** - Manual research, 10-20 top attorneys
5. **Legal Aid Integration** - Connect to HOME Line, Mid-Minnesota Legal Aid

### Decision: Deferred to Post-MVP

**Rationale:**
- Not critical path for MVP functionality
- Requires legal vetting (attorney advertising rules)
- API partnerships take time to establish
- Users can find attorneys independently while feature is being built
- Core Context System + Complaint Filing is higher value

### MVP Placeholder

Create simple UI in attorney finder:
- "Attorney Referral Service - Coming Soon"
- Link to Minnesota State Bar referral service
- Link to HOME Line (tenant hotline)
- Link to Mid-Minnesota Legal Aid
- Note: "We're building a curated directory of tenant rights attorneys"

### Post-MVP Implementation Plan

**Phase 1: Manual Directory (2-3 hours)**
- Research top 20 Minnesota tenant rights attorneys
- Create `data/attorney_directory.json` with profiles
- Simple search UI by city and practice area

**Phase 2: Dynamic Updates (4-6 hours)**
- Admin UI to add/edit attorney profiles
- Quarterly update reminders
- User-submitted attorney reviews

**Phase 3: API Integration (8-10 hours)**
- Partner with state bar or legal directory
- Real-time availability checking
- Automated profile updates
- Integration with case assessment (suggest best attorney based on case details)

### Files to Create

- `attorney_placeholder.html` - "Coming Soon" page with links
- `ATTORNEY_DIRECTORY_SPEC.md` - Full feature specification
- Update `attorney_finder_routes.py` to show placeholder

### Estimated Timeline

- Post-MVP Phase 1: Sprint 2 (after launch)
- Post-MVP Phase 2: Sprint 3
- Post-MVP Phase 3: Sprint 4 (if API partnerships secured)

**For now:** Focus on shipping Core MVP with Context System + Complaint Filing. Users get 90% of value from document intelligence and case assessment alone.