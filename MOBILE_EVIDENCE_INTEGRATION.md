# Semptify Mobile Evidence Capture & Data Flow Integration

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MOBILE DEVICES (Android/iOS/Windows)             │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │  Camera/AV  │  │  Phone Logs │  │ Messaging  │                │
│  │ (Video/Pic) │  │(Voicemail)  │  │ (Email/SMS/│                │
│  │  + Location │  │  + Messages │  │  Chat)     │                │
│  └─────────────┘  └─────────────┘  └─────────────┘                │
│         │                │                  │                      │
│         └────────────────┴──────────────────┘                      │
│                          │                                          │
│                    Upload to Semptify                              │
│                          │                                          │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │   AV CAPTURE LAYER (/api/evidence)      │
        │                                          │
        │  - register_capture() [video/audio/pic] │
        │  - import_voicemail()                   │
        │  - import_text_message()                │
        │  - import_email()                       │
        │  - import_chat_message()                │
        │                                          │
        │  ✓ Metadata extraction                  │
        │  ✓ GPS location tagging                 │
        │  ✓ SHA256 tamper-proof hashing          │
        │  ✓ EXIF preservation                    │
        └──────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │  CALENDAR/LEDGER HUB (Central Router)   │
        │                                          │
        │  - Create calendar entry for each       │
        │    piece of evidence                    │
        │  - Link to ledger transactions          │
        │  - Assign unique document ID            │
        │  - Record timestamp/actor/context       │
        └──────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │   DATA FLOW ENGINE (Rules Processing)   │
        │                                          │
        │  - Apply rules to evidence              │
        │  - Categorize document type             │
        │  - Trigger reactions                    │
        │  - Create evidence packets              │
        │  - Generate notifications               │
        └──────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │        EVIDENCE VAULT (Storage)         │
        │                                          │
        │  - Court packets with all context       │
        │  - Linked communications                │
        │  - Timeline views                       │
        │  - Tamper-proof audit trail             │
        └──────────────────────────────────────────┘
```

---

## Modules & APIs

### 1. **av_capture.py** - Audio/Visual Capture Manager
Handles all evidence capture and communication imports.

**Classes:**
- `LocationData` - GPS coordinates + accuracy
- `CaptureMetadata` - Video/audio/photo metadata
- `VoicemailImport` - Voicemail records
- `TextMessageImport` - SMS/text messages
- `EmailImport` - Email records
- `ChatMessageImport` - Chat platform messages (Slack, Teams, Signal, etc)
- `AVCaptureManager` - Central manager (singleton)

**Key Methods:**
```python
manager = get_av_manager()

# Register captured file
capture = manager.register_capture(
    capture_type="video",
    source_type="ios",
    file_path="/path/to/video.mp4",
    location=LocationData(lat, lon, accuracy),
    actor_id="tenant-123",
    description="Broken window proof"
)

# Import communications
voicemail = manager.import_voicemail(
    from_phone="+1234567890",
    duration_seconds=45.5,
    timestamp=datetime.now(),
    transcription="AI-generated transcript"
)

email = manager.import_email(
    from_email="landlord@example.com",
    to_email=["tenant@example.com"],
    subject="Lease Notice",
    body_text="...",
    timestamp=datetime.now()
)

# Retrieve evidence
captures = manager.get_captures_by_actor("tenant-123")
comms = manager.get_communications_for_number("+1234567890")
evidence = manager.get_all_evidence_by_date(days=90)
```

**Storage:**
- All metadata in: `evidence_capture/metadata/`
- Files stored in: `uploads/evidence/`
- Tamper-proof SHA256 hashing for all files

---

### 2. **av_routes.py** - Mobile Upload & Import Endpoints

**Video/Audio/Photo Upload:**
```
POST /api/evidence/capture/video
POST /api/evidence/capture/audio
POST /api/evidence/capture/photo

Multipart form data:
- file: The media file
- actor_id: Optional - who captured it
- device_name: Device identifier
- description: What was captured
- location_lat/lon/accuracy: GPS data
- duration_seconds: For audio/video
```

**Communication Imports:**
```
POST /api/evidence/import/voicemail
POST /api/evidence/import/text-message
POST /api/evidence/import/email
POST /api/evidence/import/chat

JSON body with message details
```

**Evidence Retrieval:**
```
GET /api/evidence/captures/<capture_id>
GET /api/evidence/captures/type/{video|audio|photo}
GET /api/evidence/captures/actor/<actor_id>
GET /api/evidence/communications/phone/<phone_number>
GET /api/evidence/communications/email/<email_address>
GET /api/evidence/summary?days=90
GET /api/evidence/health
```

---

## Data Flow Example: Tenant Files Complaint with Photo

```
1. MOBILE CAPTURE
   Tenant takes photo on iPhone:
   - Photo of broken window
   - GPS location tagged
   - Timestamp: 2025-01-15T10:30:00Z
   - Actor: tenant-123

2. UPLOAD TO SEMPTIFY
   POST /api/evidence/capture/photo
   - File uploaded
   - EXIF data preserved
   - SHA256 hash: abc123def456...
   - Capture ID: capture-uuid-1

3. CALENDAR ENTRY CREATED
   Entry recorded in ledger_calendar:
   - ID: entry-uuid-1
   - Timestamp: 2025-01-15T10:30:00Z
   - Type: "evidence"
   - Actor: tenant-123
   - Doc ID: capture-uuid-1
   - Context: {
       location: {lat, lon, accuracy},
       device: "iPhone",
       description: "Broken window proof"
     }

4. RULES PROCESSING (Data Flow Engine)
   Rules evaluated:
   - Rule: "photo_of_damage?" → YES
     → Set priority HIGH
     → Create evidence packet
   - Rule: "needs_landlord_notice?" → YES
     → Auto-generate repair notice template
   - Rule: "create_calendar_event?" → YES
     → Event: "Evidence: Window Damage" due today

5. EVIDENCE PACKET CREATED
   Automatically assembled:
   - Photo with location map
   - Timestamp proof
   - Metadata certificate
   - Suggested next actions
   - Links to any related communications

6. LEDGER ENTRIES UPDATED
   - Evidence logged with hash/certificate
   - Linked to tenant account
   - Searchable by date/type/location

7. NOTIFICATIONS SENT
   - Tenant: "Photo received and processed"
   - Landlord: "New evidence received"
   - Calendar: Event created with location

8. AVAILABLE FOR COURT PACKET
   When needed:
   - All evidence retrieved by query
   - Location map generated
   - Timeline created
   - Related communications included
   - Court-ready format generated
```

---

## Integration with Calendar/Ledger

**Each piece of evidence creates:**

1. **Calendar Entry** - When it happened
   - Type: "evidence"
   - Timestamp: Exact capture time
   - Location: GPS if provided
   - Actor: Who captured/sent
   - Links: Related documents

2. **Ledger Transaction** - Audit trail
   - Type: "evidence_captured"
   - Amount: 1 (just a count)
   - Description: What was captured
   - Hash: SHA256 of file for tamper detection
   - Certificate: Metadata proof

3. **Data Flow Event** - Triggers reactions
   - Input: New capture registered
   - Rules: Applied automatically
   - Output: Evidence packet, notifications, calendar events

---

## Mobile Device Support

**Android:**
- Camera/video via Intent sharing
- Location via Android Services
- Voicemail/SMS export via backup tools
- Email client integration
- Chat app message export

**iOS:**
- Camera/video via Share Sheet
- Location via Core Location
- Voicemail forwarding (email-based)
- iCloud Mail integration
- Slack/Teams app sharing

**Windows/Desktop:**
- File upload for evidence
- Email client integration (Outlook)
- Screen recording/screenshots
- Chat platform exports

**Cloud Integration:**
- Email exports (Gmail, Outlook, ProtonMail)
- Chat platform exports (Slack API, Teams API)
- Messaging backups (WhatsApp, Telegram)
- Voice services (Google Voice, Twilio)

---

## Security Features

✓ **Tamper-Proof:**
- SHA256 hash on all files
- Metadata certificates
- Append-only ledger
- Immutable timestamps

✓ **Location Privacy:**
- GPS data optional
- Accuracy measured
- Map generation on-demand
- Stored separately from media

✓ **Communication Integrity:**
- Raw headers preserved (for email)
- Phone numbers sanitized in queries
- Message text searchable
- Sender verification via metadata

✓ **Audit Trail:**
- Every import logged
- Actor tracked
- Timestamp exact
- All queries logged

---

## Next Steps

1. **Mobile App Integration** - Build React Native/Flutter app
2. **Smart Document Processing** - OCR for text extraction
3. **Evidence Packet Assembly** - Auto-generate court-ready documents
4. **Timeline Visualization** - Interactive timeline of evidence
5. **Communication Analysis** - Thread together related messages
6. **Advanced Search** - Find evidence by content, location, date

---

## Configuration

Admin can adjust via `/admin/ledger/config`:
- Retention policies
- Alert thresholds
- Tamper detection settings
- Notification preferences

All evidence integrates seamlessly with:
- **Statute of Limitations** - Deadline tracking
- **Money Ledger** - Cost/damage amounts
- **Time Ledger** - Duration tracking
- **Weather Integration** - Context for outdoor evidence
- **Court Packets** - Automatic assembly with all context
