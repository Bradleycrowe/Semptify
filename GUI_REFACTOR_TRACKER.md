# 📋 SEMPTIFY GUI MASTER LIST - REFACTORING TRACKER

## 🎯 PRIMARY USER DASHBOARDS (PRIORITY: CRITICAL)

1. ✅ **Learning Dashboard**        learning_dashboard_routes.py (421 lines)
   - Status: REFACTORED ✅
   - Uses: /system/context
   - Template: templates/learning_dashboard/
   
2. ❌ **Brad GUI**                  brad_gui_routes.py (347 lines)
   - Status: NEEDS REFACTORING
   - Current: Direct DB queries
   - Target: /system/context
   - Template: templates/brad_gui/
   
3. ❌ **Modern GUI**                modern_gui_routes.py (76 lines)
   - Status: NEEDS REFACTORING
   - Current: Direct DB queries
   - Target: /system/context
   - Template: templates/modern_gui/
   
4. ❌ **Main Dashboard**            main_dashboard_routes.py (56 lines)
   - Status: NEEDS REFACTORING
   - Current: Direct DB queries
   - Target: /system/context
   - Template: templates/main_dashboard/
   
5. ❌ **Calendar Vault UI**         calendar_vault_ui_routes.py (48 lines)
   - Status: NEEDS REFACTORING
   - Current: Direct DB queries
   - Target: /system/context
   - Template: templates/calendar_vault/

---

## ⚙️ FEATURE GUIS (PRIORITY: MEDIUM)

6. ⚠️ **Complaint Filing Wizard**   complaint_filing_routes.py (218 lines)
   - Status: NEEDS CONTEXT AUTO-FILL
   - Target: /system/context for pre-population
   
7. ⚠️ **Document Explorer**         doc_explorer_routes.py (111 lines)
   - Status: NEEDS DOCUMENT INTELLIGENCE
   - Target: Connect to document_intelligence.py
   
8. ⚠️ **Onboarding Flow**           onboarding_routes.py (120 lines)
   - Status: NEEDS CONTEXT-AWARE FLOW
   - Target: Personalized based on /system/context
   
9. ⚠️ **Journey Tracker**           journey_routes.py (51 lines)
   - Status: BASIC
   - Target: Context-driven progress

---

## 📊 SPECIALIZED SYSTEMS (PRIORITY: LOW - ALREADY WORKING)

10. ✅ **Ledger System**            ledger_*.py (4 files, 1500+ lines)
    - Status: WORKING
    - Note: Comprehensive rent tracking
    
11. ✅ **Calendar System**          calendar_*.py (7 files, 900+ lines)
    - Status: WORKING
    - Note: Timeline + storage integration
    
12. ✅ **Storage/Vault**            storage_*.py + vault.py (3 files, 500+ lines)
    - Status: WORKING (Dropbox OAuth, R2)
    - Note: Document uploads functional
    
13. ✅ **Housing Programs**         housing_programs_routes.py (532 lines)
    - Status: WORKING
    - Note: Large reference system

---

## 🔧 ADMIN/DEVELOPER GUIS (PRIORITY: MAINTENANCE)

14. ✅ **Admin Control Panel**      admin/routes.py (446 lines)
    - Status: WORKING (enforced/open modes)
    
15. ✅ **Route Discovery**          route_discovery_routes.py (500 lines)
    - Status: WORKING (dev tool)
    
16. ✅ **Feature Admin**            feature_admin_routes.py (61 lines)
    - Status: WORKING (feature flags)
    
17. ✅ **Maintenance Tools**        maintenance_routes.py (141 lines)
    - Status: WORKING (DB cleanup)

---

## 📦 INTEGRATION LAYERS (PRIORITY: INFRASTRUCTURE - DONE!)

18. ✅ **System Integration**       system_integration_routes.py (249 lines)
    - Status: REGISTERED ✅ (just activated!)
    - Provides: /system/context
    
19. ✅ **Brad Integration**         brad_integration_routes.py (442 lines)
    - Status: REGISTERED ✅
    - Provides: /brad/integrate/*
    
20. ✅ **Context API**              context_api_routes.py (166 lines)
    - Status: WORKING
    - Provides: /api/context/*

---

## 📈 REFACTORING PROGRESS

TOTAL GUIs:           20
REFACTORED:            1 (5%)
WORKING (NO CHANGE):  13 (65%)
NEEDS REFACTORING:     4 (20%) ← THIS WEEK!
NEEDS ENHANCEMENT:     2 (10%)

---

## 🎯 REFACTORING ORDER (START NOW!)

**TODAY:**
1. Brad GUI          (347 lines) - Biggest user-facing GUI
2. Modern GUI        (76 lines)  - Smallest, quick win

**TOMORROW:**
3. Main Dashboard    (56 lines)  - Primary landing page
4. Calendar Vault UI (48 lines)  - Document-focused

**RESULT:** 100% of primary dashboards using unified context! 🚀

