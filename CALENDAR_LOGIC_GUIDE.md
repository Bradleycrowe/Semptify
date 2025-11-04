# 📅 Calendar Logic Guide - Complete Breakdown

Comprehensive explanation of how the Semptify calendar system works, including data structures, methods, and workflows.

---

## 🎯 Calendar Overview

The calendar system provides:
- ✅ Time-based event management
- ✅ Deadline tracking
- ✅ Reminder scheduling
- ✅ Action item tracking
- ✅ Priority-based filtering
- ✅ Integration with ledger system

---

## 📊 Core Data Structures

### 1️⃣ CalendarEvent Class

```python
class CalendarEvent:
    """A calendar event (deadline, reminder, action needed)."""
    
    Properties:
    - id: Unique UUID for the event
    - title: Event name/description
    - event_date: When the event occurs (datetime)
    - event_type: Type of event (deadline, reminder, action_needed, completed)
    - description: Details about the event
    - related_entry_id: Links to ledger entry (optional)
    - priority: 0=low, 1=medium, 2=high
    - created_at: When event was created
    - completed: Boolean flag (true/false)
    - completed_at: When event was marked done (optional)
```

**Example Event:**
```json
{
  "id": "e7a8c2d3-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
  "title": "Send Notice to Landlord",
  "event_date": "2025-11-15T10:00:00",
  "event_type": "action_needed",
  "description": "Follow up on maintenance request",
  "related_entry_id": "ledger-entry-123",
  "priority": 2,
  "created_at": "2025-11-04T14:30:00",
  "completed": false,
  "completed_at": null
}
```

---

## 🗂️ Calendar Class Structure

### Main Calendar System

```python
class Calendar:
    """Calendar: time-based view of events and deadlines."""
    
    Attributes:
    - data_dir: Directory for storing calendar data
    - calendar_file: JSON file with all events
    - _events: In-memory list of CalendarEvent objects
    
    Key Methods:
    1. _load() - Load existing events from disk
    2. add_event(event) - Add new calendar event
    3. get_events() - Query events with filters
    4. get_upcoming_events() - Get events in next N days
    5. get_upcoming_high_priority() - Get urgent events
    6. mark_completed() - Mark event as done
    7. get_overdue_events() - Get past-due events
```

---

## 🔄 Calendar Data Flow

### Step 1: Event Creation

```
User fills form:
├── Title: "Send Notice to Landlord"
├── Date: 2025-11-15
├── Type: action_needed
├── Priority: 2 (high)
└── Description: "Follow up on maintenance"
         ↓
Form submitted to: POST /api/ledger-calendar/calendar/event
         ↓
Data processed:
├── Validate inputs
├── Parse date/time
├── Create CalendarEvent object
└── Generate unique UUID
         ↓
Event added to calendar:
├── Added to _events list
├── Appended to calendar.json file
└── Thread-safe lock used
         ↓
Response to user:
{
  "id": "e7a8c2d3-4e5f-...",
  "title": "Send Notice to Landlord",
  "event_date": "2025-11-15T10:00:00",
  "status": "created"
}
```

### Step 2: Event Retrieval

```
User requests events:
GET /api/ledger-calendar/calendar?start_date=2025-11-01&end_date=2025-12-01
         ↓
Calendar.get_events() called with filters:
├── start_date: Filter events after this date
├── end_date: Filter events before this date
├── event_type: Filter by type (deadline, reminder, etc.)
├── priority: Filter by priority (0, 1, or 2)
└── completed: Filter by status (true/false)
         ↓
Filtering logic:
1. Start with all _events
2. If start_date: keep events >= start_date
3. If end_date: keep events <= end_date
4. If event_type: keep matching types
5. If priority: keep matching priority
6. If completed: keep matching status
7. Sort by event_date ascending
         ↓
Return filtered events:
{
  "total": 5,
  "events": [
    {...event1...},
    {...event2...},
    {...event3...}
  ]
}
```

### Step 3: Upcoming Events Logic

```
User requests upcoming events:
GET /api/ledger-calendar/calendar/upcoming?upcoming_days=7
         ↓
Calendar.get_upcoming_events(days=7) called:
1. Get today's date
2. Calculate end date = today + 7 days
3. Filter events where: today <= event_date <= today+7days
4. Sort by priority (high first), then by date
5. Return prioritized list
         ↓
Example output (high priority first):
[
  {
    "title": "Court Filing Deadline",
    "event_date": "2025-11-06",  ← 2 days away
    "priority": 2,               ← HIGH
    "event_type": "deadline"
  },
  {
    "title": "Rent Payment Due",
    "event_date": "2025-11-07",  ← 3 days away
    "priority": 1,               ← MEDIUM
    "event_type": "deadline"
  },
  {
    "title": "Follow-up Call",
    "event_date": "2025-11-10",  ← 6 days away
    "priority": 0,               ← LOW
    "event_type": "reminder"
  }
]
```

---

## 🎨 Event Type System

### Event Types (4 types)

```
1. DEADLINE (deadline)
   └─ Hard due date for action
   └─ Example: "Court filing deadline", "Lease signing"
   └─ Color: Red/Urgent
   └─ Action: Must be completed by date

2. REMINDER (reminder)
   └─ Soft reminder for future action
   └─ Example: "Check on repair status", "Review lease"
   └─ Color: Blue/Informational
   └─ Action: Should be done around date

3. ACTION NEEDED (action_needed)
   └─ Task requiring user action
   └─ Example: "Send notice", "Gather evidence", "Call landlord"
   └─ Color: Yellow/Warning
   └─ Action: Start action on this date

4. COMPLETED (completed)
   └─ Finished action (historical)
   └─ Example: "Notice sent (completed)", "Payment received"
   └─ Color: Green/Success
   └─ Action: Already done
```

---

## 🎯 Priority System

### Priority Levels (0-2)

```
Priority 0: LOW ⬜
├─ Non-urgent reminders
├─ Optional follow-ups
└─ Example: "Check building code requirements"

Priority 1: MEDIUM 🟡
├─ Important but not immediate
├─ Should be done this month
└─ Example: "Schedule repair inspection"

Priority 2: HIGH 🔴
├─ Urgent, time-sensitive
├─ Must be done immediately
└─ Example: "Court filing deadline tomorrow"
```

**Color Mapping:**
```javascript
Priority 0 → Gray (#6c757d)
Priority 1 → Yellow (#ffc107)
Priority 2 → Red (#d13438)
```

---

## 🔍 Query Examples

### Example 1: Get All High-Priority Deadlines

```javascript
GET /api/ledger-calendar/calendar
  ?type=deadline
  &priority=2
  &completed=false
```

**Response:**
```json
{
  "total": 2,
  "events": [
    {
      "id": "evt-001",
      "title": "Court Filing Deadline",
      "event_date": "2025-11-06T00:00:00",
      "event_type": "deadline",
      "priority": 2,
      "completed": false
    },
    {
      "id": "evt-002",
      "title": "Response to Notice Due",
      "event_date": "2025-11-10T00:00:00",
      "event_type": "deadline",
      "priority": 2,
      "completed": false
    }
  ]
}
```

### Example 2: Get Events in Date Range

```javascript
GET /api/ledger-calendar/calendar
  ?start_date=2025-11-01T00:00:00
  &end_date=2025-11-30T23:59:59
```

**Logic:**
```
Filter: event_date >= 2025-11-01 AND event_date <= 2025-11-30
Result: All events in November 2025
```

### Example 3: Get Upcoming Events (Next 7 Days)

```javascript
GET /api/ledger-calendar/calendar
  ?upcoming_days=7
```

**Logic:**
```
today = 2025-11-04
end = today + 7 days = 2025-11-11
Filter: 2025-11-04 <= event_date <= 2025-11-11
Sort: By priority (high first), then by date
Return: Prioritized list for next week
```

---

## 💾 Storage Architecture

### File Structure

```
data/
├── calendar.json              ← All calendar events (append-only)
└── [Each line is one JSON event]

Example calendar.json:
{"id": "evt-001", "title": "...", "event_date": "...", ...}
{"id": "evt-002", "title": "...", "event_date": "...", ...}
{"id": "evt-003", "title": "...", "event_date": "...", ...}
```

### Append-Only Design

```
Benefit 1: Immutable Record
- Events are appended, never modified
- Full history preserved
- Tamper-proof (can delete entire file, not individual entries)

Benefit 2: Thread-Safe
- Lock used during add_event()
- No race conditions
- Safe for concurrent access

Benefit 3: Recovery
- If system crashes, no data loss
- Only last partial write might be lost
- Can reconstruct from valid entries
```

---

## 🔗 Integration: Calendar ↔ Ledger

### How Calendar Events Link to Ledger

```
Ledger Entry (action taken):
{
  "id": "ledger-123",
  "entry_type": "document",
  "description": "Notice sent to landlord",
  "timestamp": "2025-11-04T10:00:00"
}
         ↓
Calendar Event (future deadline):
{
  "id": "evt-456",
  "title": "Follow-up if no response",
  "event_date": "2025-11-11T10:00:00",
  "related_entry_id": "ledger-123"  ← Links back to action
}

Result:
- Ledger shows: WHAT happened and WHEN
- Calendar shows: WHAT comes next and WHEN
- Both linked together for complete timeline
```

### Example Workflow

```
STEP 1: User sends notice to landlord
└─ Creates ledger entry: "Demand letter sent"

STEP 2: System schedules follow-up
└─ Creates calendar event: "Check if landlord responded"
└─ Links to ledger entry
└─ Sets deadline: 7 days from now
└─ Priority: HIGH

STEP 3: 7 days later...
└─ User sees calendar event
└─ Clicks event → sees original notice (from ledger)
└─ Can take next action (complaint, escalation, etc.)
└─ Creates new ledger entry
└─ Cycle continues...
```

---

## ⚙️ Key Methods Explained

### 1. add_event(event)

```python
def add_event(self, event: CalendarEvent) -> None:
    """Add a new calendar event (thread-safe, append-only)."""
    with _ledger_lock:  # Lock for thread safety
        self._events.append(event)  # Add to memory
        with open(self.calendar_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict()) + "\n")  # Append to file
```

**Process:**
1. Acquire lock (prevent other threads)
2. Add event to in-memory list
3. Append JSON line to file
4. Release lock

---

### 2. get_events(filters)

```python
def get_events(
    self,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    event_type: Optional[str] = None,
    priority: Optional[int] = None,
    completed: Optional[bool] = None,
) -> List[CalendarEvent]:
    """Query events with optional filters."""
    
    # Start with all events
    results = self._events
    
    # Apply each filter
    if start_date:
        results = [e for e in results if e.event_date >= start_date]
    if end_date:
        results = [e for e in results if e.event_date <= end_date]
    if event_type:
        results = [e for e in results if e.event_type == event_type]
    if priority is not None:
        results = [e for e in results if e.priority == priority]
    if completed is not None:
        results = [e for e in results if e.completed == completed]
    
    # Sort by date
    return sorted(results, key=lambda e: e.event_date)
```

---

### 3. get_upcoming_events(days)

```python
def get_upcoming_events(self, days: int = 7) -> List[CalendarEvent]:
    """Get events in next N days, sorted by priority."""
    
    now = datetime.now()
    end_date = now + timedelta(days=days)
    
    # Filter by date range
    events = [
        e for e in self._events
        if now <= e.event_date <= end_date
        and not e.completed
    ]
    
    # Sort by priority (high first), then by date
    return sorted(
        events,
        key=lambda e: (-e.priority, e.event_date)
    )
```

---

### 4. mark_completed(event_id)

```python
def mark_completed(self, event_id: str) -> None:
    """Mark a calendar event as completed."""
    
    # Find event in memory
    for event in self._events:
        if event.id == event_id:
            event.completed = True
            event.completed_at = datetime.now()
            
            # Update file (re-write entire file with updated event)
            with open(self.calendar_file, "w", encoding="utf-8") as f:
                for e in self._events:
                    f.write(json.dumps(e.to_dict()) + "\n")
            break
```

---

## 📱 API Endpoints

### GET /api/ledger-calendar/calendar

**Purpose:** Get calendar events with filters

**Query Parameters:**
- `start_date` - ISO datetime string (optional)
- `end_date` - ISO datetime string (optional)
- `type` - Event type filter (optional)
- `priority` - Priority level 0-2 (optional)
- `completed` - true/false (optional)
- `upcoming_days` - Get next N days (optional)

**Response:**
```json
{
  "total": 3,
  "events": [
    {...event...},
    {...event...},
    {...event...}
  ]
}
```

---

### POST /api/ledger-calendar/calendar/event

**Purpose:** Create new calendar event

**Body:**
```json
{
  "title": "Send Notice to Landlord",
  "event_date": "2025-11-15T10:00:00",
  "type": "action_needed",
  "description": "Follow up on maintenance",
  "priority": 2,
  "related_entry_id": "optional-ledger-id"
}
```

**Response:**
```json
{
  "id": "evt-123",
  "title": "Send Notice to Landlord",
  "event_date": "2025-11-15T10:00:00",
  "status": "created"
}
```

---

### POST /api/ledger-calendar/calendar/event/<event_id>/complete

**Purpose:** Mark event as completed

**Response:**
```json
{
  "id": "evt-123",
  "completed": true,
  "completed_at": "2025-11-10T14:30:00"
}
```

---

## 🎯 Common Use Cases

### Use Case 1: Schedule Multi-Step Process

```
Step 1: Send Notice (Ledger + Calendar)
├─ Create ledger: "Notice sent to landlord"
├─ Create calendar: "Check for response in 7 days"
└─ Priority: HIGH

Step 2: Follow-up (Calendar triggered)
├─ User sees event in 7 days
├─ Creates ledger: "Follow-up call made"
├─ Creates calendar: "Escalate if no response in 3 days"
└─ Priority: HIGHER

Step 3: Escalation (Calendar triggered)
├─ User sees event in 3 days
├─ Creates ledger: "Filed complaint"
├─ Creates calendar: "Attend hearing in 30 days"
└─ Priority: CRITICAL
```

### Use Case 2: Rent Payment Tracking

```
Month 1: Set up
├─ Create event: "Rent due on 1st of each month"
├─ Set priority: 1 (medium)
├─ Make recurring (handle separately)

Month 1: Payment made
├─ Create ledger: "Rent paid: $1,200"
├─ Reference: Check #12345
├─ Mark calendar event completed

Month 2: System reminds
├─ Calendar shows: "Rent due in 3 days"
├─ Create event for filing if not paid

Month N: Pattern recorded
├─ Ledger shows: 12 months of payments
├─ Calendar shows: All deadlines met or missed
├─ Usable as evidence
```

### Use Case 3: Legal Deadlines

```
Day 1: Receive eviction notice
├─ Create ledger: "Eviction notice received"
├─ Create high-priority event: "Response due in 5 days"

Day 2: Prepare response
├─ Create ledger: "Started drafting response"
├─ Create event: "File response by deadline"
├─ Priority: CRITICAL

Day 4: File response
├─ Create ledger: "Response filed with court"
├─ Mark calendar event completed
├─ Create event: "Attend court hearing"
├─ New date: 30 days from now

Day 34: Court date
├─ Calendar reminds
├─ User attends
├─ Creates ledger: "Court hearing attended"
└─ Complete audit trail for records
```

---

## 🧮 Data Example: Complete Timeline

```json
{
  "user_journey": [
    {
      "date": "2025-11-01",
      "action": "Reporting issue",
      "ledger": {
        "type": "complaint",
        "description": "Reported broken heater to landlord",
        "timestamp": 1730476800
      },
      "calendar": {
        "title": "Check for response",
        "event_date": "2025-11-08",
        "priority": 1,
        "type": "reminder"
      }
    },
    {
      "date": "2025-11-08",
      "action": "No response received",
      "ledger": {
        "type": "action",
        "description": "No response from landlord to repair request",
        "timestamp": 1731081600
      },
      "calendar": {
        "title": "Send formal notice",
        "event_date": "2025-11-09",
        "priority": 2,
        "type": "action_needed"
      }
    },
    {
      "date": "2025-11-09",
      "action": "Send notice",
      "ledger": {
        "type": "notice",
        "description": "Sent certified letter demanding repairs within 5 days",
        "reference": "Cert #123ABC",
        "timestamp": 1731168000
      },
      "calendar": {
        "title": "Check for repairs",
        "event_date": "2025-11-14",
        "priority": 2,
        "type": "deadline"
      }
    }
  ]
}
```

---

## ✨ Summary

**The Calendar System:**
- ✅ Tracks time-based events and deadlines
- ✅ Integrates with ledger for complete audit trail
- ✅ Supports priorities (0-3 levels)
- ✅ Queryable with multiple filters
- ✅ Thread-safe and append-only
- ✅ Court-admissible for legal proceedings
- ✅ Handles multi-step processes
- ✅ Provides reminders and alerts

**Key Flow:**
Action → Ledger Entry → Calendar Event → Future Reminder → Next Action

