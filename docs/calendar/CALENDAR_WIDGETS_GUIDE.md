# 📅 Semptify Calendar Widgets - Complete Component Library

Comprehensive guide to all calendar widgets, input components, and interactive elements in the Semptify system.

---

## 🎯 Overview

The Calendar Widgets system provides a complete set of UI components for managing events, deadlines, reminders, and tasks within Semptify. All widgets are:

- **Interactive**: Real-time forms, filters, and previews
- **Responsive**: Mobile-friendly, works on all screen sizes
- **Integrated**: Connected to ledger/calendar backend APIs
- **Accessible**: Keyboard navigation, semantic HTML
- **Themeable**: Consistent color scheme with priority levels

---

## 📊 Statistics Dashboard

### Component: Event Statistics Cards

**Purpose**: Display high-level metrics about event status

**Four Cards:**
- **Total Events**: All events across system
- **Pending Actions**: Events not yet completed
- **Completed**: Finished events
- **Overdue**: Past-due events requiring attention

**Gradient Backgrounds:**
```
Total Events: Purple gradient (667eea → 764ba2)
Pending: Pink/Red gradient (f093fb → f5576c)
Completed: Blue/Cyan gradient (4facfe → 00f2fe)
Overdue: Pink/Gold gradient (fa709a → fee140)
```

**Features:**
- Auto-update on event changes
- Click to filter to that type
- Large numeric display
- Label descriptive

**HTML Structure:**
```html
<div class="stat-card">
    <div class="stat-value" id="total-events">0</div>
    <div class="stat-label">Total Events</div>
</div>
```

**JavaScript Update:**
```javascript
document.getElementById('total-events').textContent = total;
```

---

## 🔍 Quick Filter Buttons

### Component: Quick Filter Buttons

**Purpose**: One-click filtering of events by type/priority

**Filter Options:**
- ✓ All Events
- ⏰ Deadlines (event type: deadline)
- 🔔 Reminders (event type: reminder)
- ⚡ Actions Needed (event type: action_needed)
- ✓ Completed (event type: completed)
- 🔴 High Priority (priority: 2)
- 🟠 Medium Priority (priority: 1)
- 🟢 Low Priority (priority: 0)

**Visual States:**
- **Default**: White background, gray border
- **Hover**: Light gray background
- **Active**: Blue background, white text

**Implementation:**
```javascript
// Click handler
button.addEventListener('click', function() {
    currentFilter = this.dataset.filter;
    renderEventsList();
});

// Apply filter
function filterEvents(events) {
    if (currentFilter === 'deadline') {
        return events.filter(e => e.type === 'deadline');
    }
    // ... other filters
}
```

---

## ✨ Create New Event Form

### Component: Comprehensive Event Creation Form

**Form Sections:**

#### 1. Event Title & Type (Row 1)
```
[Event Title Input] | [Event Type Dropdown]
```
- **Title**: Free text, max 200 chars
- **Type**: Dropdown with 4 options
  - ⏰ Deadline (Must be done by date)
  - 🔔 Reminder (FYI/follow-up)
  - ⚡ Action Needed (Do this soon)
  - ✓ Completed (Done)

#### 2. Priority & Start Date (Row 2)
```
[Priority Dropdown] | [Start Date/Time Picker]
```
- **Priority**: 0=Low (🟢), 1=Medium (🟠), 2=High (🔴)
- **Start Date/Time**: datetime-local input (YYYY-MM-DD HH:MM)

#### 3. Due Date & Category (Row 3)
```
[Due Date Picker] | [Category Dropdown]
```
- **Due Date**: Optional date field
- **Category**: 8 options:
  - 💰 Payment
  - 📋 Complaint
  - 🔧 Maintenance
  - 📸 Evidence
  - 📬 Notice
  - ⚖️ Legal Action
  - 💬 Communication
  - 📌 Other

#### 4. Description (Full Width)
```
[Textarea: 3 rows for full details]
```

#### 5. Ledger Entry & Assignee (Row 4)
```
[Related Entry ID] | [Assignee/Owner Name]
```
- **Related Entry**: Link to ledger entry (optional)
- **Assignee**: Who is responsible (optional)

#### 6. Recurring Options (Expandable Section)
```
☐ Repeat this event
  └─ [Pattern Dropdown: Daily/Weekly/Biweekly/Monthly/Yearly]
  └─ [Repeat Until Date Picker]
```

#### 7. Notifications (Checkbox Group)
```
☑ Notify on due date
☑ Notify 24 hours before
☐ Notify 7 days before
☐ Notify if overdue
```

#### 8. Event Preview (Read-Only)
```
📝 Event Preview:
Title: ...
Type: ...
Priority: ...
Start: ...
Due: ...
```

#### 9. Action Buttons
```
[✓ Create Event Button] [↻ Clear Form Button]
```

**Form Submission:**
```javascript
async function handleAddEvent(e) {
    e.preventDefault();
    const eventData = {
        title: "...",
        type: "...",
        priority: 1,
        // ... all fields
    };
    const response = await fetch('/api/ledger-calendar/calendar/event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(eventData)
    });
}
```

---

## 📋 Events List Widget

### Component: Event Cards Display

**Card Layout:**
```
┌─ Event Card (colored left border) ─┐
│                                    │
│ Title [Type Badge] [Priority Dot]  │
│ Status Icon  Date @ Time           │
│ Description (if available)         │
│                                    │
└────────────────────────────────────┘
```

**Event Type Styling:**
- **Deadline**: Red left border (#e74c3c)
- **Reminder**: Teal left border (#00796b)
- **Action Needed**: Orange left border (#e65100)
- **Completed**: Green left border (#27ae60)

**Components:**
- **Title**: Bold text
- **Type Badge**: Colored pill with type name
- **Priority Dot**: Colored circle (0=🟢, 1=🟠, 2=🔴)
- **Status Icon**: Visual indicator (⏳=pending, ✓=completed, ❌=overdue)
- **Date/Time**: ISO format with time in HH:MM
- **Description**: Optional sub-text (truncated to 2 lines)

**Interactive:**
- Click card → Open event modal
- Hover → Slight shadow effect
- Filter buttons change displayed cards

**Rendering:**
```javascript
function renderEventsList() {
    const html = events.map(event => `
        <div class="event-card ${event.type}" onclick="viewEventDetails(event)">
            <div class="event-card-title">
                ${event.title}
                <span class="event-type-badge">${event.type}</span>
                <span class="priority-badge priority-${getPriorityName(event.priority)}"></span>
            </div>
            <div class="event-card-meta">
                ${new Date(event.start_date).toLocaleDateString()} @ ${new Date(event.start_date).toLocaleTimeString()}
            </div>
        </div>
    `).join('');
    document.getElementById('events-list').innerHTML = html;
}
```

---

## ⏰ Upcoming Events Widget

### Component: Next 7 Days Preview

**Purpose**: Quick view of what's coming up

**Features:**
- Filters events to next 7 days
- Sorted by date (earliest first)
- Click-to-view details
- Auto-refreshes with new events

**Display:**
```
📆 Upcoming Events (Next 7 Days)

[Event 1]
⏰ Nov 5, 2025 - 09:00

[Event 2]
⏰ Nov 6, 2025 - 14:30

(No upcoming events) - if empty
```

**Implementation:**
```javascript
function renderUpcomingEvents() {
    const now = new Date();
    const sevenDaysLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
    
    const upcoming = events
        .filter(e => new Date(e.start_date) >= now && new Date(e.start_date) <= sevenDaysLater)
        .sort((a, b) => new Date(a.start_date) - new Date(b.start_date));
}
```

---

## 💾 Export/Import Widget

### Component: Data Management

**Two Buttons:**

1. **📥 Export Events (JSON)**
   - Downloads all events as JSON file
   - Filename: `semptify-events-YYYY-MM-DD.json`
   - Useful for: Backup, migration, sharing

2. **📤 Import Events**
   - Opens file picker
   - Accepts .json files
   - Validates JSON structure
   - Merges with existing events

**Export Format:**
```json
[
  {
    "id": "event-123",
    "title": "Send notice to landlord",
    "type": "deadline",
    "priority": 2,
    "start_date": "2025-11-05T09:00:00",
    "due_date": "2025-11-05",
    "description": "...",
    "category": "notice",
    "assignee": "tenant",
    "related_entry_id": "ledger-456",
    "notifications": {...}
  }
]
```

**Implementation:**
```javascript
function exportEvents() {
    const dataStr = JSON.stringify(events, null, 2);
    const blob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `semptify-events-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
}
```

---

## 📆 Calendar View Widget

### Component: Full Calendar Display

**Navigation:**
```
[← Previous] November 2025 [Next →]
[Month] [Week] [Day]
```

**Three View Modes:**
1. **Month**: Full month grid with events
2. **Week**: 7-day timeline view
3. **Day**: Detailed hourly view

**Features:**
- Color-coded events by type
- Click event → view details
- Drag-to-create new events
- Resize events to change duration
- Event tooltips on hover

**FullCalendar Integration:**
```javascript
function initializeCalendar() {
    const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
        initialView: 'dayGridMonth',
        events: events.map(e => ({
            id: e.id,
            title: e.title,
            start: e.start_date,
            end: e.due_date || e.start_date,
            classNames: [`event-${e.type}`, `priority-${e.priority}`],
            extendedProps: {
                type: e.type,
                priority: e.priority,
                description: e.description
            }
        })),
        eventClick: handleEventClick,
        dateClick: handleDateClick,
    });
    calendar.render();
}
```

---

## 🔔 Event Details Modal

### Component: Event Inspection & Actions

**Triggered By:**
- Clicking event card
- Clicking calendar event
- API response

**Modal Content:**
```
┌─ Event Details ────────────────────┐
│ × [Close]                          │
├────────────────────────────────────┤
│ [Event Title in Blue Box]          │
│                                    │
│ Type: deadline                     │
│ Priority: High                     │
│ Status: Pending                    │
│ Start: Nov 5, 2025 @ 09:00        │
│ Due: Nov 5, 2025                  │
│ Description: Full description...   │
│                                    │
├────────────────────────────────────┤
│ [Close]  [Delete]  [Edit]         │
└────────────────────────────────────┘
```

**Available Actions:**
- **Close**: Dismiss modal
- **Delete**: Remove event (with confirmation)
- **Edit**: Open event in edit form

**Implementation:**
```javascript
function viewEventDetails(event) {
    selectedEvent = event;
    const modal = new bootstrap.Modal(document.getElementById('eventModal'));
    document.getElementById('eventModalBody').innerHTML = `
        <div class="info-box">
            <div class="info-box-title">${event.title}</div>
            <div class="info-box-text">
                Type: ${event.type}<br>
                Priority: ${getPriorityName(event.priority)}<br>
                Start: ${new Date(event.start_date).toLocaleString()}
            </div>
        </div>
    `;
    modal.show();
}
```

---

## 🎨 UI Styling & Colors

### Priority Colors
- **Low (0)**: 🟢 Green (#4caf50)
- **Medium (1)**: 🟠 Orange (#ff9800)
- **High (2)**: 🔴 Red (#f44336)

### Event Type Colors
- **Deadline**: Red (#e74c3c) - Must do
- **Reminder**: Teal (#00796b) - FYI
- **Action Needed**: Orange (#e65100) - Do soon
- **Completed**: Green (#4caf50) - Done

### Status Colors
- **Pending**: 🟠 Orange (#ff9800)
- **Completed**: 🟢 Green (#4caf50)
- **Overdue**: 🔴 Red (#f44336)

### Alert Banners
- **Success**: Green background, left border
- **Warning**: Yellow background, left border
- **Danger**: Red background, left border

---

## 📱 Responsive Design

### Breakpoints:
- **Desktop** (> 768px): Multi-column layouts
- **Tablet** (576px - 768px): 2-column grids
- **Mobile** (< 576px): Single column, full-width buttons

### Mobile Features:
- Touch-friendly buttons (min 44px)
- Larger form inputs
- Stacked layouts
- Horizontal scrolling for tables

---

## ♿ Accessibility

### Keyboard Navigation:
- Tab: Move between form fields
- Enter: Submit form, click buttons
- Escape: Close modals
- Arrow keys: Navigate calendar

### Screen Reader Support:
- ARIA labels on inputs
- Semantic HTML structure
- Form labels linked to inputs
- Status messages announced

### Color Contrast:
- WCAG AA compliant
- Not relying on color alone
- Icons with text labels

---

## 🔄 Real-Time Updates

### Auto-Refresh:
```javascript
setInterval(() => {
    loadEvents();
    updateStatistics();
    renderUpcomingEvents();
}, 30000); // Every 30 seconds
```

### WebSocket Integration (Future):
```javascript
const socket = io('/calendar');
socket.on('event_added', (event) => {
    events.push(event);
    renderEventsList();
});
socket.on('event_updated', (event) => {
    updateEvent(event);
});
```

---

## 🧪 Testing Scenarios

### Scenario 1: Create Payment Deadline
1. Title: "Pay rent"
2. Type: Deadline
3. Priority: High
4. Due: Nov 1, 2025
5. Category: Payment
6. Click: Create Event
7. Verify: Card appears, stat updates

### Scenario 2: Add Maintenance Reminder
1. Title: "Check heater"
2. Type: Reminder
3. Priority: Medium
4. Start: Nov 3, 2025
5. Click: Create Event
6. Verify: "Upcoming" widget shows it

### Scenario 3: Mark Task Completed
1. Select event
2. Click modal "Edit"
3. Change Type → Completed
4. Click Save
5. Verify: Card styling changes, stats update

### Scenario 4: Filter by Priority
1. Click "🔴 High Priority" button
2. Verify: Only high priority events show
3. Click "All Events"
4. Verify: All events show again

### Scenario 5: Export/Import
1. Click "📥 Export Events"
2. File downloads: semptify-events-YYYY-MM-DD.json
3. Open different browser/tab
4. Click "📤 Import Events"
5. Select downloaded file
6. Verify: All events appear

---

## 📊 API Integration Points

### Get Events
```
GET /api/ledger-calendar/calendar?start_date=...&end_date=...
Response: {events: [...]}
```

### Create Event
```
POST /api/ledger-calendar/calendar/event
Body: {title, type, priority, start_date, ...}
Response: {id: "event-123", ...}
```

### Update Event
```
PUT /api/ledger-calendar/calendar/event/{id}
Body: {updates...}
Response: {success: true}
```

### Delete Event
```
DELETE /api/ledger-calendar/calendar/event/{id}
Response: {success: true}
```

### Get Statistics
```
GET /api/ledger-calendar/calendar/stats
Response: {total: 10, pending: 5, completed: 3, overdue: 2}
```

---

## 🚀 Advanced Features

### Drag & Drop
- Drag events to reschedule
- Drop on date to create
- Hold Shift for multi-select

### Bulk Operations
- Select multiple events
- Mark all as complete
- Delete selected
- Export selected

### Search & Advanced Filters
- Full-text search
- Date range filter
- Category filter
- Assignee filter
- Combination filters

### Event Templates
- Save event patterns
- Quick-create from template
- Recurring event templates

### Notifications
- Browser notifications
- Email notifications (admin)
- SMS alerts (premium)
- Slack integration

---

## 📋 Component Checklist

- ✅ Statistics Dashboard (4 cards)
- ✅ Quick Filter Buttons (8 filters)
- ✅ Event Creation Form (9 sections)
- ✅ Event List Display (cards with details)
- ✅ Upcoming Events Widget (7-day preview)
- ✅ Calendar View (month/week/day)
- ✅ Event Details Modal
- ✅ Export/Import Functions
- ✅ Real-time Updates
- ✅ Responsive Design
- ✅ Accessibility Support

---

## 🔗 Access Calendar Widgets

**URL**: `http://localhost:8080/calendar-widgets`

**Features**:
- Full demo of all widgets
- Live event creation
- Real data integration
- Export/import testing
- Responsive preview

