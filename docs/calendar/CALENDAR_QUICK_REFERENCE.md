.....................# 🚀 Calendar Widgets - Quick Reference Card

One-page cheat sheet for calendar widget development and integration.

---

## 📍 Access Points

**Live Demo Page:**
```
http://localhost:8080/calendar-widgets
```

**API Endpoints:**
```
GET    /api/ledger-calendar/calendar
POST   /api/ledger-calendar/calendar/event
PUT    /api/ledger-calendar/calendar/event/{id}
DELETE /api/ledger-calendar/calendar/event/{id}
GET    /api/ledger-calendar/calendar/stats
```

**Template Files:**
```
templates/calendar_widgets.html      (Main widget page)
templates/ledger_calendar_dashboard.html (Alternative dashboard)
CALENDAR_WIDGETS_GUIDE.md             (Full documentation)
CALENDAR_INPUT_COMPONENTS.md          (Input fields reference)
```

---

## 🎯 Key Components

| Component | Purpose | Count |
|-----------|---------|-------|
| Statistics Cards | Show metrics | 4 |
| Quick Filters | Filter events | 8 |
| Event Form | Create events | 1 |
| Events List | Display events | 1 |
| Upcoming Widget | Next 7 days | 1 |
| Calendar View | Month/week/day | 1 |
| Event Modal | Details popup | 1 |
| Export/Import | Data management | 2 buttons |

---

## 📋 Form Fields

### Required Fields (Must be filled)
```
1. Title              (text input)
2. Event Type         (dropdown: deadline/reminder/action/completed)
3. Priority Level     (dropdown: 0/1/2)
4. Start Date & Time  (datetime picker)
```

### Optional Fields (Can be left empty)
```
5. Due Date           (date picker)
6. Category           (dropdown: payment/complaint/etc)
7. Description        (textarea)
8. Assignee           (text input)
9. Related Entry ID   (text input)
10. Recurring         (checkbox + nested fields)
11. Notifications     (4 checkboxes)
```

---

## 🎨 Styling Reference

### Priority Colors
- 🟢 Low (0): #4caf50
- 🟠 Medium (1): #ff9800
- 🔴 High (2): #f44336

### Event Type Colors
- 🔴 Deadline: #e74c3c
- 🟦 Reminder: #00796b
- 🟠 Action: #e65100
- ✓ Completed: #27ae60

### Status Colors
- ⏳ Pending: #ff9800
- ✓ Completed: #4caf50
- ❌ Overdue: #f44336

### Buttons
- Primary: #2c3e50 (dark blue-gray)
- Secondary: #95a5a6 (gray)
- Success: #27ae60 (green)
- Danger: #e74c3c (red)

---

## 📡 API Quick Calls

### Create Event
```bash
curl -X POST http://localhost:8080/api/ledger-calendar/calendar/event \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Send notice",
    "type": "deadline",
    "priority": 2,
    "start_date": "2025-11-05T09:00:00",
    "due_date": "2025-11-05",
    "description": "Send formal notice to landlord",
    "category": "notice"
  }'
```

### Get Events
```bash
curl http://localhost:8080/api/ledger-calendar/calendar?start_date=2025-11-01&end_date=2025-11-30
```

### Get Statistics
```bash
curl http://localhost:8080/api/ledger-calendar/calendar/stats
```

---

## 🔄 Data Flow

```
User Input (Form)
       ↓
JavaScript Validation
       ↓
Event Data Object Created
       ↓
POST to /api/ledger-calendar/calendar/event
       ↓
Backend Processing
       ↓
Database Storage
       ↓
Response with Event ID
       ↓
UI Update (reload events)
       ↓
Show Success Message
```

---

## 🧪 Quick Test Scenarios

### Scenario 1: Create Payment Event
```
Title: Pay Rent
Type: Deadline
Priority: High (2)
Start: 2025-11-01 09:00
Due: 2025-11-01
Category: Payment
→ Submit
→ Verify: Stats update, card appears
```

### Scenario 2: Filter by Priority
```
Click: "🔴 High Priority" button
→ Verify: Only high-priority events show
Click: "All Events"
→ Verify: All events show again
```

### Scenario 3: Export Events
```
Click: "📥 Export Events (JSON)"
→ Download: semptify-events-YYYY-MM-DD.json
→ Verify: File has all events in JSON format
```

---

## 🔧 JavaScript Functions

### Load Events
```javascript
loadEvents() // Fetch from API, update all displays
```

### Update Statistics
```javascript
updateStatistics() // Count pending/completed/overdue
```

### Render Events List
```javascript
renderEventsList() // Display events based on filter
```

### Render Upcoming
```javascript
renderUpcomingEvents() // Show next 7 days
```

### Add Event
```javascript
handleAddEvent(e) // Submit form, create event
```

### Filter Events
```javascript
filterEvents(events) // Apply current filter
```

### View Details
```javascript
viewEventDetails(event) // Open modal with event info
```

### Export/Import
```javascript
exportEvents()      // Download JSON
importEvents()      // Upload JSON
handleImportFile()  // Process imported file
```

---

## 🎯 Common Patterns

### Get Event by Type
```javascript
const deadlines = events.filter(e => e.type === 'deadline');
const reminders = events.filter(e => e.type === 'reminder');
```

### Sort by Date
```javascript
events.sort((a, b) => new Date(a.start_date) - new Date(b.start_date));
```

### Sort by Priority
```javascript
events.sort((a, b) => b.priority - a.priority);
```

### Filter Overdue
```javascript
const overdue = events.filter(e => new Date(e.due_date) < new Date());
```

### Get Statistics
```javascript
{
  total: events.length,
  pending: events.filter(e => e.type !== 'completed').length,
  completed: events.filter(e => e.type === 'completed').length,
  overdue: events.filter(e => new Date(e.due_date) < now).length
}
```

---

## 🚨 Error Handling

### Show Alert
```javascript
showAlert(message, type) // type: 'success', 'warning', 'danger'
```

### Validation Errors
```javascript
if (!title) showAlert('Title is required', 'danger');
if (priority === '') showAlert('Select priority', 'danger');
if (dueDate < startDate) showAlert('Due date must be after start', 'danger');
```

### API Errors
```javascript
try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('API error');
    const data = await response.json();
} catch (error) {
    showAlert('Error: ' + error.message, 'danger');
}
```

---

## 📱 Mobile Responsive

**Desktop (> 768px):**
- 2-column form layout
- Side-by-side buttons
- Full-width tables

**Tablet (576px - 768px):**
- 2-column grids
- Stacked buttons

**Mobile (< 576px):**
- 1-column layout
- Full-width buttons
- Vertical stacking
- Larger touch targets

---

## ⌨️ Keyboard Shortcuts

- `Tab`: Next field
- `Shift+Tab`: Previous field
- `Enter`: Submit form
- `Escape`: Close modal
- `Space`: Toggle checkbox
- `Arrow Keys`: Navigate calendar

---

## 🎨 CSS Classes Reference

### Form Classes
- `.form-label` - Label styling
- `.form-control` - Text input styling
- `.form-select` - Dropdown styling
- `.form-check` - Checkbox wrapper

### Button Classes
- `.btn-primary-custom` - Blue button
- `.btn-secondary-custom` - Gray button
- `.quick-filter-btn` - Filter button
- `.quick-filter-btn.active` - Active filter

### Event Classes
- `.event-card` - Event card container
- `.event-card.deadline` - Deadline styling
- `.event-card.reminder` - Reminder styling
- `.event-card.action` - Action styling
- `.event-card.completed` - Completed styling

### Component Classes
- `.widget-container` - Widget wrapper
- `.widget-title` - Widget header
- `.stat-card` - Statistics card
- `.stats-grid` - Statistics grid
- `.events-list` - Events container
- `.event-type-badge` - Type badge
- `.priority-badge` - Priority dot
- `.event-form-preview` - Preview box

### Alert Classes
- `.alert-success` - Green alert
- `.alert-warning` - Yellow alert
- `.alert-danger` - Red alert
- `.alert-banner` - Alert styling

---

## 📊 Data Structure

### Event Object
```javascript
{
  id: "event-uuid-123",
  title: "Send notice to landlord",
  type: "deadline",              // deadline|reminder|action_needed|completed
  priority: 2,                   // 0=low, 1=medium, 2=high
  start_date: "2025-11-05T09:00:00",
  due_date: "2025-11-05",
  description: "Send formal notice",
  category: "notice",            // payment|complaint|maintenance|etc
  assignee: "John Doe",
  related_entry_id: "ledger-456",
  is_recurring: false,
  recurring_pattern: null,       // daily|weekly|biweekly|monthly|yearly
  recurring_until: null,
  notifications: {
    on_due: true,
    before_24h: true,
    before_7d: false,
    on_overdue: false
  }
}
```

---

## ✅ Checklist for New Feature

- [ ] Form field added to HTML
- [ ] Validation added to JavaScript
- [ ] Field included in event data object
- [ ] Field serialized in API request
- [ ] Backend route handles new field
- [ ] Database schema updated
- [ ] Response includes new field
- [ ] UI displays new field
- [ ] Tests added
- [ ] Documentation updated

---

## 🔗 Related Files

```
📁 Semptify/
├── Semptify.py                              (Route: /calendar-widgets)
├── ledger_calendar.py                       (Calendar/Ledger backend)
├── ledger_calendar_routes.py               (API endpoints)
├── templates/
│   ├── calendar_widgets.html               (Widget page)
│   └── ledger_calendar_dashboard.html      (Dashboard)
├── CALENDAR_WIDGETS_GUIDE.md              (Full guide)
├── CALENDAR_INPUT_COMPONENTS.md           (Input reference)
└── LOGIC_FLOW_COMPLETE.md                 (Decision trees)
```

---

## 💡 Pro Tips

1. **Validation**: Always validate on both client (JavaScript) and server (Flask)
2. **Real-time Preview**: Update preview box as user types
3. **Recurring Events**: Generate multiple events on creation, don't store pattern
4. **Timestamps**: Use ISO 8601 format everywhere
5. **Hashing**: All events linked to ledger entries get SHA256 hash
6. **Error Handling**: Show user-friendly messages, log errors server-side
7. **Performance**: Load events in chunks, paginate large lists
8. **Caching**: Cache event list locally, refresh every 30 seconds
9. **Accessibility**: Always include form labels and ARIA attributes
10. **Testing**: Test on mobile, tablet, desktop before release

---

## 🎓 Learning Resources

- **FullCalendar Documentation**: https://fullcalendar.io/docs
- **Bootstrap 5 Forms**: https://getbootstrap.com/docs/5.0/forms/
- **HTML Input Types**: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input
- **Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **JavaScript Date**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date

---

## 📞 Support

For issues or questions:
1. Check `CALENDAR_WIDGETS_GUIDE.md` for detailed info
2. Check `CALENDAR_INPUT_COMPONENTS.md` for input specifics
3. Review `LOGIC_FLOW_COMPLETE.md` for business logic
4. Check API logs for server errors
5. Use browser DevTools console for client errors

