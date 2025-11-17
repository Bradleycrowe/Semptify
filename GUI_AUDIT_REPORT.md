# Semptify GUI Audit Report

Generated: Sun 11/16/2025

## Summary

- ✅ Working routes: 88
- ❌ Routes with missing templates: 23
- ⚠️ API/redirect routes: 230
- Total routes: 337

## Missing Templates

- `/admin` needs `admin.html`
  - File: `Semptify.py`
  - Function: `admin_dashboard`

- `/admin` needs `admin.html`
  - File: `Semptify.py`
  - Function: `admin_dashboard`

- `/admin` needs `admin.html`
  - File: `admin\routes.py`
  - Function: `admin_dashboard`

- `/all` needs `all.html`
  - File: `Semptify.py`
  - Function: `all_page`

- `/api/resource/contribute` needs `admin.html`
  - File: `Semptify.py`
  - Function: `api_contribute_resource`

- `/comm` needs `communication_suite.html`
  - File: `Semptify.py`
  - Function: `comm_suite_demo`

- `/dashboard-old` needs `dashboard.html`
  - File: `Semptify.py`
  - Function: `dashboard_old`

- `/group/<group_id>` needs `group.html`
  - File: `Semptify.py`
  - Function: `group_page`

- `/health` needs `admin/health.html`
  - File: `admin\routes.py`
  - Function: `health_dashboard`

- `/legal_advisor` needs `legal_advisor.html`
  - File: `generated\routes\legal_advisor_routes.py`
  - Function: `legal_advisor_page`

- `/move_checklist_form` needs `move_checklist_preview.html`
  - File: `Semptify.py`
  - Function: `move_checklist_form`

- `/move_checklist_form` needs `move_checklist_form.html`
  - File: `Semptify.py`
  - Function: `move_checklist_form`

- `/office` needs `office.html`
  - File: `Semptify.py`
  - Function: `office`

- `/packet_form` needs `packet_preview.html`
  - File: `Semptify.py`
  - Function: `packet_form`

- `/packet_form` needs `packet_form.html`
  - File: `Semptify.py`
  - Function: `packet_form`

- `/programs-for-landlords` needs `landlord_programs.html`
  - File: `housing_programs_routes.py`
  - Function: `landlord_programs_page`

- `/seed/start` needs `seed_bootstrap_start.html`
  - File: `seed_bootstrap_routes.py`
  - Function: `seed_start`

- `/service_animal_form` needs `service_animal_preview.html`
  - File: `Semptify.py`
  - Function: `service_animal_form`

- `/service_animal_form` needs `service_animal_form.html`
  - File: `Semptify.py`
  - Function: `service_animal_form`

- `/settings` needs `user_settings.html`
  - File: `Semptify.py`
  - Function: `user_settings`

- `/settings` needs `user_settings.html`
  - File: `Semptify.py`
  - Function: `user_settings`

- `/witness_form` needs `witness_preview.html`
  - File: `Semptify.py`
  - Function: `witness_form`

- `/witness_form` needs `witness_form.html`
  - File: `Semptify.py`
  - Function: `witness_form`

## All Route Mappings

✅ `/` → `admin/feature_dashboard.html` (in `feature_admin_routes.py`)
✅ `/` → `index_simple.html` (in `Semptify.py`)
✅ `/` → `admin/dashboard.html` (in `admin\routes.py`)
✅ `/` → `admin/dashboard.html` (in `backups\backup_20251021182344\admin\routes.py`)
✅ `/` → `admin/dashboard.html` (in `backups\before_rename_20251021183523\admin_routes.py`)
✅ `/` → `admin/dashboard.html` (in `backups\before_rename_20251021183523\backups_backup_20251021182344_admin_routes.py`)
✅ `/` → `index.html` (in `backups\before_rename_20251021222753\Semptify.py`)
⚠️ `/_html_list` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/about` → `placeholder.html` (in `Semptify.py`)
⚠️ `/action/log` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
⚠️ `/actor/<actor_id>/flow` → `NO_TEMPLATE` (in `data_flow_routes.py`)
❌ `/admin` → `admin.html` (in `Semptify.py`)
❌ `/admin` → `admin.html` (in `Semptify.py`)
❌ `/admin` → `admin.html` (in `admin\routes.py`)
✅ `/admin/learning` → `admin_learning.html` (in `Semptify.py`)
⚠️ `/admin/learning/download` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/admin/learning/reset` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/admin/logs` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/admin/metrics` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/admin/prime_learning` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/admin/reset` → `NO_TEMPLATE` (in `learning_routes.py`)
⚠️ `/admin/status` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/admin/users` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/agencies` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/alerts/thresholds` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/alerts/thresholds/update` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
❌ `/all` → `all.html` (in `Semptify.py`)
⚠️ `/api/analyze` → `NO_TEMPLATE` (in `demo_routes.py`)
⚠️ `/api/attorney_finder` → `NO_TEMPLATE` (in `attorney_finder_routes.py`)
⚠️ `/api/attorney_finder` → `NO_TEMPLATE` (in `routes\attorney_finder_routes.py`)
⚠️ `/api/cards` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/complaint/get-procedures/<venue_key>` → `NO_TEMPLATE` (in `complaint_filing_routes.py`)
⚠️ `/api/complaint/identify-venues` → `NO_TEMPLATE` (in `complaint_filing_routes.py`)
⚠️ `/api/complaint/track-outcome` → `NO_TEMPLATE` (in `complaint_filing_routes.py`)
⚠️ `/api/complaint/update-procedure` → `NO_TEMPLATE` (in `complaint_filing_routes.py`)
⚠️ `/api/court-packet/<packet_id>/add-document` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/court-packet/<packet_id>/update-section` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/court-packet/create` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/dashboard` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/dashboard/update` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/evidence-copilot` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/features` → `NO_TEMPLATE` (in `feature_admin_routes.py`)
⚠️ `/api/features/<name>` → `NO_TEMPLATE` (in `feature_admin_routes.py`)
⚠️ `/api/features/<name>/health` → `NO_TEMPLATE` (in `feature_admin_routes.py`)
⚠️ `/api/issue/report` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/learning/action` → `NO_TEMPLATE` (in `learning_dashboard_routes.py`)
⚠️ `/api/learning/curiosity/answer` → `NO_TEMPLATE` (in `learning_dashboard_routes.py`)
⚠️ `/api/learning/curiosity/questions` → `NO_TEMPLATE` (in `learning_dashboard_routes.py`)
⚠️ `/api/learning/dashboard` → `NO_TEMPLATE` (in `learning_dashboard_routes.py`)
⚠️ `/api/learning/feedback` → `NO_TEMPLATE` (in `learning_dashboard_routes.py`)
⚠️ `/api/legal_advisor` → `NO_TEMPLATE` (in `generated\routes\legal_advisor_routes.py`)
⚠️ `/api/library/category/<category>` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/fun-fact` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/greeting` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/info-card/<resource_id>` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/jurisdiction/<jurisdiction>` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/relevant` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/resource/<resource_id>` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/library/search` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/ocr/process` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/ocr/search` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/onboarding/skip` → `NO_TEMPLATE` (in `onboarding_routes.py`)
⚠️ `/api/onboarding/submit` → `NO_TEMPLATE` (in `onboarding_routes.py`)
⚠️ `/api/outcome/report` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/programs/all-categories` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/category/<category>` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/eligibility-check` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/guide/<program_id>` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/intensity-recommendations` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/quick-help` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/search` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/programs/track-outcome` → `NO_TEMPLATE` (in `housing_programs_routes.py`)
⚠️ `/api/regenerate-token` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/register/adaptive` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/rent_calculator` → `NO_TEMPLATE` (in `rent_calculator_routes.py`)
⚠️ `/api/rent_calculator` → `NO_TEMPLATE` (in `routes\rent_calculator_routes.py`)
❌ `/api/resource/contribute` → `vault.html` (in `Semptify.py`)
⚠️ `/api/setup-auto-storage` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/smart-inbox/scan` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/smart-inbox/update` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/stats` → `NO_TEMPLATE` (in `feature_admin_routes.py`)
⚠️ `/api/test` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/timeline/events` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/voice/log-call` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/api/voice/save-memo` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/apply` → `NO_TEMPLATE` (in `improvement_routes.py`)
✅ `/attorney` → `pages/attorney.html` (in `Semptify.py`)
✅ `/attorney_finder` → `attorney_finder.html` (in `attorney_finder_routes.py`)
✅ `/attorney_finder` → `attorney_finder.html` (in `routes\attorney_finder_routes.py`)
⚠️ `/auth/google-drive` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/calendar` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
✅ `/calendar-timeline` → `calendar_timeline.html` (in `Semptify.py`)
✅ `/calendar-timeline-horizontal` → `calendar_timeline_horizontal.html` (in `Semptify.py`)
✅ `/calendar-widgets` → `placeholder.html` (in `Semptify.py`)
⚠️ `/calendar/event` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
⚠️ `/calendar/event/<event_id>/complete` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
⚠️ `/calendar/upcoming` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
⚠️ `/capabilities` → `NO_TEMPLATE` (in `seed_api_routes.py`)
⚠️ `/capture/audio` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/capture/photo` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/capture/video` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/captures/<capture_id>` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/captures/actor/<actor_id>` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/captures/type/<capture_type>` → `NO_TEMPLATE` (in `av_routes.py`)
✅ `/cards` → `cards.html` (in `Semptify.py`)
⚠️ `/cell/<user_id>/<cell>` → `NO_TEMPLATE` (in `dashboard_api_routes.py`)
❌ `/comm` → `communication_suite.html` (in `Semptify.py`)
⚠️ `/comm/metadata` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/communications/email/<email_address>` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/communications/phone/<phone_number>` → `NO_TEMPLATE` (in `av_routes.py`)
✅ `/complaint-filing` → `file_complaint.html` (in `Semptify.py`)
⚠️ `/complaint-library` → `NO_TEMPLATE` (in `complaint_filing_routes.py`)
⚠️ `/config` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/config/reset` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/config/section/<section>` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/config/update` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
✅ `/control-panel` → `admin/control_panel.html` (in `admin\routes.py`)
⚠️ `/copilot` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/court-packet` → `pages/court_packet.html` (in `Semptify.py`)
⚠️ `/court-packet/<doc_id>` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
✅ `/court-packet/<packet_id>` → `pages/court_packet_detail.html` (in `Semptify.py`)
✅ `/courtroom` → `pages/courtroom.html` (in `Semptify.py`)
✅ `/dashboard` → `learning_dashboard.html` (in `learning_dashboard_routes.py`)
⚠️ `/dashboard` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
✅ `/dashboard` → `dashboard_grid.html` (in `Semptify.py`)
✅ `/dashboard` → `dashboard_grid.html` (in `Semptify.py`)
✅ `/dashboard-grid` → `dashboard_grid.html` (in `Semptify.py`)
❌ `/dashboard-old` → `dashboard.html` (in `Semptify.py`)
⚠️ `/deadlines` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
✅ `/demand-letter` → `placeholder.html` (in `Semptify.py`)
⚠️ `/document/<doc_id>/flow` → `NO_TEMPLATE` (in `data_flow_routes.py`)
⚠️ `/durations` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/durations/update` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
✅ `/email` → `admin/email_panel.html` (in `admin\routes.py`)
⚠️ `/engine/<capability_name>` → `NO_TEMPLATE` (in `seed_api_routes.py`)
⚠️ `/events` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/events` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/events/<event_id>` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/events/<event_id>` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/evidence/by-date` → `NO_TEMPLATE` (in `av_routes.py`)
✅ `/evidence/gallery` → `placeholder.html` (in `Semptify.py`)
⚠️ `/evidence/summary` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/execute/<capability>` → `NO_TEMPLATE` (in `journey_routes.py`)
⚠️ `/export/ical` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/fact-check` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/fact-check-batch` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
✅ `/faq` → `placeholder.html` (in `Semptify.py`)
✅ `/features` → `placeholder.html` (in `Semptify.py`)
⚠️ `/feedback` → `NO_TEMPLATE` (in `learning_routes.py`)
✅ `/file-complaint` → `file_complaint.html` (in `complaint_filing_routes.py`)
⚠️ `/filing-success-stories` → `NO_TEMPLATE` (in `complaint_filing_routes.py`)
⚠️ `/forms` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/functions` → `NO_TEMPLATE` (in `data_flow_routes.py`)
✅ `/get-started` → `placeholder.html` (in `Semptify.py`)
✅ `/getting-started` → `pages/getting_started.html` (in `Semptify.py`)
❌ `/group/<group_id>` → `group.html` (in `Semptify.py`)
⚠️ `/health` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/health` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/health` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/health` → `NO_TEMPLATE` (in `Semptify.py`)
❌ `/health` → `admin/health.html` (in `admin\routes.py`)
⚠️ `/health` → `NO_TEMPLATE` (in `backups\before_rename_20251021222753\Semptify.py`)
⚠️ `/health/reports` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/health/run` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/healthz` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/help` → `placeholder.html` (in `Semptify.py`)
✅ `/housing-programs` → `housing_programs.html` (in `housing_programs_routes.py`)
✅ `/how-it-works` → `placeholder.html` (in `Semptify.py`)
✅ `/human` → `admin/human_perspective.html` (in `admin\routes.py`)
⚠️ `/import/chat` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/import/email` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/import/text-message` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/import/voicemail` → `NO_TEMPLATE` (in `av_routes.py`)
⚠️ `/info` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/insights` → `NO_TEMPLATE` (in `learning_routes.py`)
⚠️ `/integration-status` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/interact` → `NO_TEMPLATE` (in `seed_api_routes.py`)
⚠️ `/issue-temp-access` → `NO_TEMPLATE` (in `admin\routes.py`)
✅ `/journey` → `housing_journey.html` (in `Semptify.py`)
⚠️ `/jurisdiction` → `NO_TEMPLATE` (in `journey_routes.py`)
✅ `/jurisdiction` → `pages/jurisdiction.html` (in `Semptify.py`)
⚠️ `/jurisdiction-info` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
✅ `/know-your-rights` → `placeholder.html` (in `Semptify.py`)
✅ `/landlord-research` → `pages/landlord_research.html` (in `Semptify.py`)
✅ `/laws` → `pages/laws.html` (in `Semptify.py`)
⚠️ `/layout/<user_id>` → `NO_TEMPLATE` (in `dashboard_api_routes.py`)
✅ `/learning` → `preliminary_learning.html` (in `Semptify.py`)
✅ `/learning-dashboard` → `learning_dashboard.html` (in `Semptify.py`)
⚠️ `/learning-module-query` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/learning-module-sources/<module_name>` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/ledger` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
✅ `/ledger-calendar` → `ledger_calendar_dashboard.html` (in `Semptify.py`)
⚠️ `/ledger/<entry_id>` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
⚠️ `/ledger/export` → `NO_TEMPLATE` (in `ledger_calendar_routes.py`)
❌ `/legal_advisor` → `legal_advisor.html` (in `generated\routes\legal_advisor_routes.py`)
⚠️ `/legal_notary/start` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/library` → `placeholder.html` (in `Semptify.py`)
⚠️ `/list-temp-access` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/map-category` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/metrics` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/money/add` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/money/balance/<actor_id>` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/money/summary/<actor_id>` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/money/transactions/<actor_id>` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
✅ `/move-in` → `pages/move_in.html` (in `Semptify.py`)
❌ `/move_checklist_form` → `move_checklist_preview.html` (in `Semptify.py`)
⚠️ `/notary` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/observe` → `NO_TEMPLATE` (in `learning_routes.py`)
⚠️ `/observe/sequence` → `NO_TEMPLATE` (in `learning_routes.py`)
✅ `/ocr` → `pages/ocr.html` (in `Semptify.py`)
❌ `/office` → `office.html` (in `Semptify.py`)
✅ `/onboarding` → `onboarding.html` (in `onboarding_routes.py`)
✅ `/packet/export` → `filing_packet.html` (in `Semptify.py`)
❌ `/packet_form` → `packet_preview.html` (in `Semptify.py`)
⚠️ `/plan` → `NO_TEMPLATE` (in `improvement_routes.py`)
✅ `/plan` → `personalized_plan.html` (in `Semptify.py`)
✅ `/privacy` → `pages/privacy.html` (in `Semptify.py`)
✅ `/privacy` → `pages/privacy.html` (in `Semptify.py`)
⚠️ `/procedures` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/process-document` → `NO_TEMPLATE` (in `data_flow_routes.py`)
❌ `/programs-for-landlords` → `landlord_programs.html` (in `housing_programs_routes.py`)
⚠️ `/progress/<user_id>` → `NO_TEMPLATE` (in `dashboard_api_routes.py`)
⚠️ `/proposals` → `NO_TEMPLATE` (in `improvement_routes.py`)
⚠️ `/qualified-routes` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/query-sources` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/query-statistics` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/quick-reference` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/readyz` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/reasoning` → `demo_reasoning.html` (in `demo_routes.py`)
✅ `/recover` → `token_recovery.html` (in `Semptify.py`)
✅ `/register-burgundy` → `register_option3_burgundy.html` (in `Semptify.py`)
✅ `/register-forest` → `register_option2_forest.html` (in `Semptify.py`)
⚠️ `/register-functions` → `NO_TEMPLATE` (in `data_flow_routes.py`)
✅ `/register-navy` → `register_option1_navy.html` (in `Semptify.py`)
✅ `/register-slate` → `register_option4_slate.html` (in `Semptify.py`)
⚠️ `/register-sources` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/registry` → `NO_TEMPLATE` (in `data_flow_routes.py`)
⚠️ `/registry` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/registry/by-category/<category>` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/release_now` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/release_now` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/release_now` → `NO_TEMPLATE` (in `backups\backup_20251021182344\admin\routes.py`)
⚠️ `/release_now` → `NO_TEMPLATE` (in `backups\before_rename_20251021183523\admin_routes.py`)
⚠️ `/release_now` → `NO_TEMPLATE` (in `backups\before_rename_20251021183523\backups_backup_20251021182344_admin_routes.py`)
⚠️ `/rent-ledger` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
✅ `/rent_calculator` → `rent_calculator.html` (in `rent_calculator_routes.py`)
✅ `/rent_calculator` → `rent_calculator.html` (in `routes\rent_calculator_routes.py`)
✅ `/research` → `pages/research.html` (in `Semptify.py`)
⚠️ `/reset` → `NO_TEMPLATE` (in `seed_api_routes.py`)
⚠️ `/resources` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
✅ `/resources` → `resources.html` (in `Semptify.py`)
⚠️ `/resources/download/filing_packet_checklist.txt` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/resources/download/filing_packet_timeline.txt` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/resources/download/witness_statement.txt` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/resources/filing_packet` → `filing_packet.html` (in `Semptify.py`)
✅ `/resources/move_checklist` → `move_checklist.html` (in `Semptify.py`)
✅ `/resources/service_animal` → `service_animal.html` (in `Semptify.py`)
✅ `/resources/witness_statement` → `witness_statement.html` (in `Semptify.py`)
⚠️ `/resources/witness_statement_save` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/respond` → `NO_TEMPLATE` (in `journey_routes.py`)
⚠️ `/revoke-temp-access` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/rotate_token` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/routes-by-category/<category>` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/run` → `NO_TEMPLATE` (in `maintenance_routes.py`)
⚠️ `/scan` → `NO_TEMPLATE` (in `improvement_routes.py`)
⚠️ `/scan` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
✅ `/security` → `admin/security_panel.html` (in `admin\routes.py`)
⚠️ `/seed/assess` → `NO_TEMPLATE` (in `seed_bootstrap_routes.py`)
⚠️ `/seed/generate` → `NO_TEMPLATE` (in `seed_bootstrap_routes.py`)
⚠️ `/seed/plan` → `NO_TEMPLATE` (in `seed_bootstrap_routes.py`)
❌ `/seed/start` → `seed_bootstrap_start.html` (in `seed_bootstrap_routes.py`)
⚠️ `/sensitivities` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/sensitivities/update` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/sensitivity/deadline` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/sensitivity/list` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/service-date/add` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
❌ `/service_animal_form` → `service_animal_preview.html` (in `Semptify.py`)
❌ `/settings` → `user_settings.html` (in `Semptify.py`)
❌ `/settings` → `user_settings.html` (in `Semptify.py`)
✅ `/setup` → `user_setup.html` (in `Semptify.py`)
✅ `/setup/situation` → `setup_situation.html` (in `Semptify.py`)
✅ `/signin` → `signin_simple.html` (in `Semptify.py`)
✅ `/smart-inbox` → `pages/smart_inbox.html` (in `Semptify.py`)
⚠️ `/sources` → `NO_TEMPLATE` (in `ollama_routes.py`)
⚠️ `/sources-for-learning/<module_name>` → `NO_TEMPLATE` (in `route_discovery_routes.py`)
⚠️ `/start` → `NO_TEMPLATE` (in `journey_routes.py`)
⚠️ `/statistics` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/statistics` → `NO_TEMPLATE` (in `data_flow_routes.py`)
⚠️ `/stats` → `NO_TEMPLATE` (in `learning_routes.py`)
⚠️ `/stats` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/status` → `NO_TEMPLATE` (in `journey_routes.py`)
⚠️ `/status` → `NO_TEMPLATE` (in `maintenance_routes.py`)
⚠️ `/status` → `NO_TEMPLATE` (in `seed_api_routes.py`)
⚠️ `/statute/<statute_id>/toll` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/statute/active` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/statute/create` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/statute/expiring-soon` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/statutes/summary` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
✅ `/storage-db` → `admin/storage_db.html` (in `admin\routes.py`)
⚠️ `/storage-db/download` → `NO_TEMPLATE` (in `admin\routes.py`)
⚠️ `/storage-db/sync` → `NO_TEMPLATE` (in `admin\routes.py`)
✅ `/storage-setup` → `choose_storage.html` (in `Semptify.py`)
⚠️ `/suggest` → `NO_TEMPLATE` (in `learning_routes.py`)
⚠️ `/summarize` → `NO_TEMPLATE` (in `ollama_routes.py`)
⚠️ `/tasks` → `NO_TEMPLATE` (in `maintenance_routes.py`)
✅ `/terms` → `placeholder.html` (in `Semptify.py`)
⚠️ `/test-login` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/time/add` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/time/summary/<actor_id>` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/timeline` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
⚠️ `/timeline` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/timeline-ruler` → `timeline_ruler.html` (in `Semptify.py`)
✅ `/timeline-simple` → `timeline_simple_horizontal.html` (in `Semptify.py`)
⚠️ `/timeline-test` → `NO_TEMPLATE` (in `Semptify.py`)
⚠️ `/timeline/add` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/tools` → `placeholder.html` (in `Semptify.py`)
✅ `/tools/complaint-generator` → `placeholder.html` (in `Semptify.py`)
✅ `/tools/court-packet` → `placeholder.html` (in `Semptify.py`)
✅ `/tools/rights-explorer` → `placeholder.html` (in `Semptify.py`)
✅ `/tools/statute-calculator` → `placeholder.html` (in `Semptify.py`)
⚠️ `/types` → `NO_TEMPLATE` (in `calendar_timeline_routes.py`)
⚠️ `/update-knowledge` → `NO_TEMPLATE` (in `preliminary_learning_routes.py`)
✅ `/users-panel` → `admin/users_panel.html` (in `admin\routes.py`)
⚠️ `/users-panel/export` → `NO_TEMPLATE` (in `admin\routes.py`)
✅ `/vault` → `vault_login.html` (in `Semptify.py`)
✅ `/vault` → `vault_login.html` (in `Semptify.py`)
✅ `/vault` → `vault_login.html` (in `Semptify.py`)
✅ `/vault-login` → `vault_login.html` (in `Semptify.py`)
⚠️ `/vault/upload` → `NO_TEMPLATE` (in `Semptify.py`)
✅ `/voice-capture` → `pages/voice_capture.html` (in `Semptify.py`)
⚠️ `/weather/<date>/<location>` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/weather/add` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/weather/period` → `NO_TEMPLATE` (in `ledger_tracking_routes.py`)
⚠️ `/weather/settings` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/weather/settings/update` → `NO_TEMPLATE` (in `ledger_admin_routes.py`)
⚠️ `/widgets` → `NO_TEMPLATE` (in `dashboard_api_routes.py`)
❌ `/witness_form` → `witness_preview.html` (in `Semptify.py`)
