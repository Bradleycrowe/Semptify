# Formal Communication Methods Module

This module contains templates, delivery options, and multilingual help for formal tenant-landlord communications.

## Included Methods

- Lease Agreements
- Eviction Notices
- Rent Increase Letters
- Entry Notices

## Modal Triggers

- View
- Send
- Track
- Notarize

## Multilingual Support

English, Spanish, Somali, Hmong

## Wiring Instructions

1. Drop this folder into `Semptify/modules/CommunicationSuite/FormalMethods/`.
2. Wire modal triggers into the frontend UI (use `modal_triggers.json` to map trigger text to template IDs).
3. Enable voice commands such as:
	- “View lease”
	- “Send eviction”
	- “Switch to Somali”

## Files in this module

- `formal_communication.json` — metadata for formal templates (delivery recommendations, notary requirement, languages).
- `modal_triggers.json` — mapping from UI trigger text to formal template IDs.
- `help_texts.json` / `help_text_multilingual.json` — localized help text keyed by `help_text_key` in the templates.

If you'd like, I can also:

- Add modal HTML snippets and a small JS helper to open modals with localized help text.
- Wire a minimal Flask route or API endpoint that serves the module data to the UI.
- Implement the voice-command wiring (client-side JS that maps recognized phrases to the `voice_action_map.json` actions).
