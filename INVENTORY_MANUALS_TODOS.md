# Inventory: Manuals, Guides, Docs, Templates, and TODOs

This file is an automated inventory of documentation-like artifacts found in this repository. It groups items by category and includes a short excerpt or note for each entry to help you find and use them.

Generated: 2025-10-20

## How to use
- Files are listed with their repository path. Open the file to read full content.
- Excerpts show the title or first lines to identify the purpose quickly.

---

## Official Guides & Manuals

- `docs/admin-guide.md`
  - Title: "Semptify Admin Guide"
  - Excerpt: "This guide is the single source of truth for running, securing, operating, and troubleshooting Semptify. It assumes Windows + PowerShell..."
  - Purpose: Operational runbook, secrets management, deploy & verification steps, break-glass, health & metrics, troubleshooting.

- `README.md`
  - Title: "Semptify"
  - Excerpt: "Small Flask-based GUI for tenant-justice automation. This repository includes a development server, a production runner (`run_prod.py` using waitress), Docker support, tests, and CI workflows."
  - Purpose: Project overview, getting started, dev/prod run instructions, AI provider setup, RON notes, CI and release behavior.

- `docs/deployment_checklist.md`
  - Title: "Deployment Checklist for Semptify"
  - Excerpt: "This checklist helps ensure Semptify is configured correctly for Render (or similar) deployments."
  - Purpose: Environment variables, writable paths, pre/post deploy checks.

- `RUNNING_PRODUCTION.md`
  - Purpose: (See file for production-specific run/docs - referenced from root)

## Module-level READMEs and Help

- `modules/office_module/README.md`
  - Title: "Semptify Office module"
  - Excerpt: "This module provides a scaffold for a secure 'Office' workspace with: Certified Rooms (video), Notary Station, Document Center..."
  - Purpose: How to run demo backend, AI orchestrator demo, list of files in the module, caution about demo scaffolds vs production.

- `modules/office_module/help/admin_help.md`
  - Purpose: Admin help for Office module (user/admin operational guidance).

- `modules/office_module/help/organizer_help.md`
  - Purpose: Organizer-facing help.

- `modules/office_module/help/user_help.md`
  - Purpose: User quick guide (e.g., join room, upload, timestamp & lock).

## Docs & Templates (docs/ and docs/templates)

- `docs/index.html` (rendered site base file)
  - Purpose: HTML landing template used for generated pages.

- `docs/Semptify2_Modules_2025-10-18/` *(multiple .py docs)*
  - Notable: `backend_offensive_bundle.py`, `subpoena_builder.py`, `complaint_generator.py` — Python examples that act as docs/examples.

- `docs/law_notes/mn_checklist.md`
  - Purpose: Jurisdiction-specific checklist for Minnesota.

- `docs/templates/witness_statement_template.txt`
  - Purpose: A plain text witness statement template with instructions.

- `docs/templates/filing_packet_checklist.txt`
  - Purpose: Filing packet checklist template.

## Snapshots, Archives, and Generated Docs

- `.snapshots/*.md`
  - Purpose: Project snapshots including tree listings and past content. Example: `.snapshots/snapshot-2025-10-11T21_31_50_509Z.md`.

- `.github/copilot-instructions.md`
  - Purpose: Internal guidance for automated agents working with this repository (contains architecture snapshot and security notes).

## Templates & Site HTML (templates/ and static pages)

- `templates/` (many HTML templates)
  - Notable pages: `admin.html`, `copilot.html`, `vault.html`, `register.html`, `register_success.html`, `evidence_panel.html`, `law_notes/*` templates.
  - Purpose: UI templates used by the Flask app; many provide user-facing guidance and form layout.

## Helper Scripts & Operational Docs (scripts/)

- `scripts/bootstrap_secrets.ps1` - helper to generate FLASK_SECRET and ADMIN_TOKEN.
- `scripts/sync_render_secrets.ps1` - sync secrets to Render.
- `scripts/deploy_oneclick.ps1` - one-and-done deploy helper.
- `scripts/dev_server.ps1` - bootstraps venv and runs dev server.
- `scripts/*` - other operational scripts (deploy, setup, tests, audits).

## Tests referring to documentation (tests/)

- `tests/test_registration.py` - asserts the phrase "one-time token" in `register_success.html` (documents registration behavior).
- `tests/test_vault.py`, `tests/test_copilot.py`, `tests/test_admin_*` - various tests that reference admin, vault, and docs-driven behavior.

## TODOs & Action Items

This inventory found many references to docs and helper scripts but no centralized TODO file. To locate TODOs in source code, search for "TODO" or "FIXME". A quick scan returned matches in scripts and possibly templates. Consider running:

  grep -n "TODO\|FIXME" -R .

If you'd like, I can run a repository-wide TODO search and append results to this inventory.

## Additional Notes and Suggested Next Steps

- I focused on files that are clearly documentation-like (README, docs/, modules/*/help, templates, and scripts). If you want a deeper inventory (e.g., every template file, every docs/ subfolder, every test referencing a doc string), I can expand the list and include short excerpts for every file.
- I can also add cross-links to GitHub paths or generate a simple HTML index page under `docs/` for easier browsing.

---

If you want me to (pick any):
- Run a TODO/FIXME scan and include exact file:line excerpts.
- Expand the inventory to include every file under `templates/` and `docs/` with first-line excerpts.
- Create a `docs/INVENTORY.html` rendering this inventory for the docs site.

Tell me which and I'll continue.

