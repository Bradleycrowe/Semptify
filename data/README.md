# Data

This folder contains event and delivery data imported/created by the developer assistant.

Files:
- `events.json`: Normalized event records (ISO datetimes, unique `id` fields).
- `events.csv`: Simple CSV export of the same records for import into spreadsheets or calendar tools.
- `deliveries.json`: Delivery records for notices (email/SMS) linked to events.
- `deliveries.csv`: CSV export of delivery records.
- `shipments.json`: Shipment/tracking records linked to events (carrier, tracking_number, expected_delivery).
- `shipments.csv`: CSV export of shipment records.
- `vault.json`: Records stored in the document vault (notices, invoices, signed PDFs).
- `vault.csv`: CSV export of vault records.
- `notaries.json`: Notarization records and verification metadata for vault items.
- `notaries.csv`: CSV export of notary records.
- `voice_ui.json`: Voice UI configuration (voice triggers and reader modes) used by any TTS/voice assistant integration.
- `media_config.json`: Configuration for recorded media (recording modes, storage path, and links to vault/event/contact IDs).
- `scan_config.json`: Scanning configuration (document/QR/photo modes, output formats, and linked IDs).
- `document_templates.json`: Document template descriptors (methods, formats, delivery options, notary rules, languages, and modal triggers).
- `document_templates.csv`: CSV export of document template descriptors.
- `voice_action_map.json`: Mapping of voice triggers to suggested backend actions/routes and parameters (developer-facing).

Notes:
- `created_by` and `created_at` are metadata added during import.
- Times are stored without timezone offset; add your timezone if necessary when importing into a calendar.
