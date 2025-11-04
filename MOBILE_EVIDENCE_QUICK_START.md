# Mobile Evidence Capture - Quick Reference

## System Architecture Summary

You now have a **complete mobile evidence capture system** that:

1. **Captures from Devices** (Android, iOS, Windows)
   - Video with GPS location
   - Audio with duration tracking
   - Photos with EXIF preservation
   - Location tagging (GPS accuracy measured)

2. **Imports Communications**
   - Voicemail messages (with transcription)
   - SMS/text messages (bidirectional)
   - Email (with headers and attachments)
   - Chat messages (Slack, Teams, Signal, WhatsApp, Telegram, etc)

3. **Routes Through Calendar**
   - Each capture creates a calendar entry
   - Linked to ledger with tamper-proof hashing
   - Connected to actor/property/case
   - Timestamp preserved exactly

4. **Intelligent Processing**
   - Rules automatically categorize evidence
   - Reactions trigger notifications
   - Evidence packets assembled automatically
   - Court-ready documents generated on-demand

5. **Evidence Vault**
   - All files stored with SHA256 hash
   - Metadata kept separate and searchable
   - Timeline accessible via calendar
   - Communications linked by phone/email

---

## API Endpoints Summary

### Mobile Upload (Multipart Form)
```
POST /api/evidence/capture/video       # Upload video with GPS
POST /api/evidence/capture/audio       # Upload audio with duration
POST /api/evidence/capture/photo       # Upload photo with location
```

### Communication Import (JSON)
```
POST /api/evidence/import/voicemail    # Voicemail message
POST /api/evidence/import/text-message # SMS/text message
POST /api/evidence/import/email        # Email with headers
POST /api/evidence/import/chat         # Chat platform message
```

### Evidence Retrieval (JSON)
```
GET /api/evidence/captures/<id>              # Get specific capture
GET /api/evidence/captures/type/{type}       # All video/audio/photo
GET /api/evidence/captures/actor/<actor_id>  # Actor's captures
GET /api/evidence/communications/phone/<num> # Phone communications
GET /api/evidence/communications/email/<addr># Email communications
GET /api/evidence/summary?days=90            # Time-based summary
GET /api/evidence/health                     # System status
```

---

## Example Usage: Tenant Captures Evidence

### 1. Mobile App Uploads Video
```bash
curl -X POST http://localhost:5000/api/evidence/capture/video \
  -F "file=@broken_window.mp4" \
  -F "actor_id=tenant-123" \
  -F "device_name=iPhone 12" \
  -F "description=Broken window - landlord refuses repair" \
  -F "location_lat=37.7749" \
  -F "location_lon=-122.4194" \
  -F "location_accuracy=10.5" \
  -F "duration_seconds=45.2"
```

**Response:**
```json
{
  "id": "capture-uuid-1",
  "capture_type": "video",
  "source_type": "mobile",
  "timestamp": "2025-01-15T14:30:00",
  "actor_id": "tenant-123",
  "device_name": "iPhone 12",
  "description": "Broken window - landlord refuses repair",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy_meters": 10.5,
    "map_url": "https://maps.google.com/?q=37.7749,-122.4194"
  },
  "file_size_bytes": 5242880,
  "hash_sha256": "abc123def456...",
  "mime_type": "video/mp4",
  "duration_seconds": 45.2
}
```

### 2. Calendar Entry Automatically Created
```
Calendar Entry:
- ID: entry-uuid-1
- Type: "evidence"
- Date: 2025-01-15
- Time: 14:30:00 UTC
- Actor: tenant-123
- Location: San Francisco, CA
- Related Document: capture-uuid-1
- Priority: HIGH (damage evidence)
- Status: "Evidence received and processed"
```

### 3. Rules Processing Triggered
```
Rule 1: is_damage_photo? → YES
  → Set calendar priority to HIGH
  → Add to "Evidence Needed" list

Rule 2: needs_landlord_notice? → YES
  → Auto-generate repair notice template
  → Suggest "24-hour repair demand" letter

Rule 3: build_evidence_packet? → YES
  → Create packet with:
    - Video file + metadata
    - GPS location map
    - Timestamp certificate
    - Legal summary
```

### 4. Evidence Packet Ready for Court
```
Packet Contents:
├─ Evidence Summary
│  ├─ Capture Date: 2025-01-15 14:30 UTC
│  ├─ Location: 37.7749, -122.4194 (10.5m accuracy)
│  ├─ Device: iPhone 12
│  └─ Status: Tamper-proof (hash verified)
│
├─ Media File
│  ├─ File: broken_window.mp4
│  ├─ Duration: 45 seconds
│  ├─ Hash: abc123def456...
│  └─ Size: 5.2 MB
│
├─ Location Map
│  ├─ Google Maps link
│  ├─ Satellite view
│  └─ Accuracy radius
│
├─ Related Communications
│  ├─ Emails from landlord
│  ├─ Text messages
│  └─ Repair request history
│
└─ Legal Context
   ├─ Applicable statutes
   ├─ Repair timeline
   └─ Suggested next action
```

---

## Configuration (via Admin Panel)

Access: `/admin/ledger/config`

**Adjustable Settings:**
```json
{
  "notification_settings": {
    "alert_days_before_statute_expiry": 30,
    "alert_days_before_service_deadline": 7,
    "alert_severe_weather_days_ahead": 3
  },
  "ledger_settings": {
    "retention_days": 2555,
    "enable_tamper_detection": true,
    "require_actor_verification": false
  }
}
```

**Environment Variables:**
```bash
SEMPTIFY_CONFIG_NOTIFICATION_ALERT_DAYS_BEFORE_STATUTE_EXPIRY=45
SEMPTIFY_CONFIG_LEDGER_RETENTION_DAYS=3650
```

---

## Linked Systems

All evidence integrates with:

### 1. **Calendar** (/api/ledger-calendar/)
- Timeline view of all evidence
- Linked to court dates/deadlines
- Filterable by type/actor/date

### 2. **Ledger** (/api/ledger-tracking/)
- Money ledger: damage amounts
- Time ledger: repair timelines
- Service ledger: delivery proof

### 3. **Data Flow** (/api/data-flow/)
- Rules trigger on evidence capture
- Automatic evidence packet assembly
- Notifications sent to relevant parties

### 4. **Court Packets**
- Auto-generated from all linked evidence
- Includes communications (email/SMS/chat)
- Formatted for court filing

---

## Storage Locations

```
evidence_capture/
├── metadata/
│   ├── capture_metadata.json      # All video/audio/photo
│   ├── voicemails.json            # Voicemail records
│   ├── text_messages.json         # SMS messages
│   ├── emails.json                # Email records
│   └── chat_messages.json         # Chat messages
│
uploads/
└── evidence/
    ├── broken_window.mp4          # Raw media files
    ├── tenant_statement.m4a       # Audio recordings
    ├── damage_photo_1.jpg         # Photos with EXIF
    └── ...                        # All captured media
```

---

## Supported Platforms

**Mobile:**
- ✓ Android (video, camera, location)
- ✓ iOS (video, camera, location)
- ✓ Windows Phone

**Communications Import:**
- ✓ Phone/Voicemail (export to email)
- ✓ SMS/Text (via backup tools)
- ✓ Email (all providers: Gmail, Outlook, ProtonMail)
- ✓ Slack (API integration)
- ✓ Microsoft Teams (API integration)
- ✓ Signal (manual export)
- ✓ WhatsApp (manual export)
- ✓ Telegram (manual export)
- ✓ SMS services (Google Voice, Twilio)

---

## Security Guarantees

✓ **Tamper-Proof**
- SHA256 hash on all files
- Metadata certificates
- Immutable ledger entries
- Append-only architecture

✓ **Privacy**
- Location data optional
- Searchable by phone/email (not stored)
- Raw headers preserved for verification

✓ **Admissibility**
- Exact timestamps
- GPS accuracy recorded
- Device information captured
- Complete audit trail

✓ **Chain of Custody**
- Actor tracked
- Upload timestamp
- File hash verification
- Modification history

---

## Next Development Phases

### Phase 2: Smart Processing
- OCR for text extraction (Google Vision API)
- Document classification
- Automatic evidence categorization
- Handwriting recognition

### Phase 3: Advanced Timeline
- Interactive visualization
- Communications threading
- Collaborative annotations
- Timeline export to court

### Phase 4: Mobile App
- React Native/Flutter app
- Real-time upload with retry
- Offline capture capability
- Instant location tagging
- QR barcode scanning

### Phase 5: Integration
- Lawyer portal access
- Court filing API
- Evidence sharing workflows
- Permissions management

---

## Support & Troubleshooting

**Upload Fails?**
- Check file size
- Verify location format (lat/lon as floats)
- Ensure actor_id is valid format

**Evidence Not Appearing in Calendar?**
- Check `/admin/ledger/health`
- Verify data_flow rules are loaded
- Check `/admin/ledger/stats` for counts

**Communications Not Importing?**
- Verify timestamp format (ISO 8601)
- Check phone number format
- Validate email addresses

**Questions?**
- See: `MOBILE_EVIDENCE_INTEGRATION.md`
- API docs: `/api/evidence/health`
- Config: `/admin/ledger/config`
