# SEMPTIFY TODO LIST

## IMMEDIATE (Current Sprint)
- [x] Fix dashboard datetime error
- [x] Fix housing_programs link (hyphen vs underscore)
- [x] Create unified GUI homepage with onboarding flow
- [x] Add intensity engine explanation
- [x] Test all working links
- [x] Remove broken 404 links
- [x] Create Start-Semptify.ps1 macro
- [x] Push unified GUI to GitHub

## SHORT TERM (Next 2 Weeks)
- [ ] Fix vault to work without token for browsing (low intensity)
- [ ] Wire up AI Copilot route
- [ ] Complete settings page functionality
- [ ] Add admin panel access
- [ ] Test registration → storage → journey → vault flow

## MEDIUM TERM (Phase 1 - Build Core DNA)
**See REGENERATION_PLAN.md for full details**
- [ ] Create /core/ directory structure
- [ ] Extract and unify auth logic (vault.py, security.py → core/auth.py)
- [ ] Build unified storage backend (core/storage.py)
- [ ] Implement intensity engine with user profiling (core/intensity.py)
- [ ] Create base_unified.html template
- [ ] Build core router with intensity-aware redirects

## LONG TERM (Phases 2-5 - Module Regeneration)
**Cellular Regeneration Approach - Replace old modules with unified architecture**

### Phase 2: Critical Modules (Weeks 2-3)
- [ ] Regenerate Vault module with intensity awareness
- [ ] Regenerate Timeline (auto-populated from vault)
- [ ] Regenerate Journey (becomes intensity engine interface)
- [ ] Regenerate Settings (unified storage/auth config)

### Phase 3: Workflow Modules (Week 3)
- [ ] Consolidate Calendar (merge 5 blueprints → 1 unified)
- [ ] Rebuild Ledger with unified storage
- [ ] Rebuild Complaint Filing with intensity engine integration

### Phase 4: Integration & Migration (Week 4)
- [ ] Create legacy route redirects (old → new)
- [ ] Data migration scripts
- [ ] Intensity engine learning from existing user data
- [ ] Full flow testing (low → medium → high intensity)

### Phase 5: Advanced Features (Week 5)
- [ ] Regenerate Housing Programs (adaptive search)
- [ ] Rebuild AI Copilot (intensity-aware suggestions)
- [ ] Rebuild Admin Panel (unified monitoring)

## BACKLOG (Future Enhancements)
- [ ] Multi-language support
- [ ] Mobile-responsive templates
- [ ] Offline mode with sync
- [ ] Export case files to PDF
- [ ] Integration with court e-filing systems
- [ ] Tenant rights chatbot
- [ ] Housing advocate collaboration features

## TECHNICAL DEBT
- [ ] Remove unused route files (after regeneration)
- [ ] Consolidate 30+ blueprints to 10 unified modules
- [ ] Standardize error handling across all modules
- [ ] Add comprehensive logging
- [ ] Security audit of token system
- [ ] Performance optimization (caching, lazy loading)

---

**Philosophy:** Like cellular regeneration - every 7 years, rebuild with improved DNA for increased longevity and usability.

**Current Focus:** Short term fixes → Phase 1: Build Core DNA → Regenerate all modules
