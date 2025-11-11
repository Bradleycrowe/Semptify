# 📝 Calendar Input Components - Complete Reference

Detailed documentation of all input widgets, forms, and interactive elements for the Semptify calendar system.

---

## 🎯 Input Component Categories

1. **Text Inputs**: Single-line text entry
2. **Text Areas**: Multi-line text entry
3. **Select Dropdowns**: Predefined options
4. **Date/Time Pickers**: Calendar and time selection
5. **Checkboxes**: Boolean toggles
6. **Radio Buttons**: Single selection from group
7. **Buttons**: Action triggers
8. **Sliders**: Value range selection
9. **Color Pickers**: Color selection
10. **Search Inputs**: Search with autocomplete

---

## 1️⃣ Text Input Components

### Event Title Input
```html
<input type="text" class="form-control" id="event-title" 
       placeholder="e.g., Send notice to landlord" required>
```

**Properties:**
- **Type**: Text
- **Required**: Yes
- **Max Length**: 200 characters
- **Placeholder**: Example text
- **Validation**: Non-empty

**JavaScript Validation:**
```javascript
const title = document.getElementById('event-title').value;
if (!title || title.trim().length === 0) {
    showError('Title is required');
    return;
}
if (title.length > 200) {
    showError('Title must be 200 characters or less');
    return;
}
```

**Used For:**
- Brief description of event
- Appears in event card
- Shown in calendar view
- Searchable field

---

### Ledger Entry Link Input
```html
<input type="text" class="form-control" id="event-ledger-entry" 
       placeholder="e.g., entry-id-123">
```

**Properties:**
- **Type**: Text
- **Required**: No
- **Format**: UUID or entry ID
- **Placeholder**: Example entry ID
- **Validation**: UUID format (optional)

**Purpose:**
- Link event to ledger entry
- Track audit trail
- Connect actions to records

**Example Values:**
- `entry-uuid-123abc`
- `1234567890`
- `complaint-notice-001`

---

### Assignee/Owner Input
```html
<input type="text" class="form-control" id="event-assignee" 
       placeholder="Who is responsible?">
```

**Properties:**
- **Type**: Text
- **Required**: No
- **Max Length**: 100
- **Validation**: Person name format

**Purpose:**
- Identify who owns task
- Used for delegation
- Shows in event details
- For team collaboration

**With Autocomplete:**
```javascript
const assigneeInput = document.getElementById('event-assignee');
const teamMembers = ['John Doe', 'Jane Smith', 'Admin'];

assigneeInput.addEventListener('input', function(e) {
    const value = e.target.value.toLowerCase();
    const matches = teamMembers.filter(m => m.toLowerCase().includes(value));
    showSuggestions(matches);
});
```

---

## 2️⃣ Text Area Components

### Event Description
```html
<textarea class="form-control" id="event-description" rows="3" 
          placeholder="Add details about this event..."></textarea>
```

**Properties:**
- **Type**: Textarea
- **Rows**: 3 (expandable)
- **Max Length**: 2000 characters
- **Placeholder**: Hint text
- **Validation**: None (optional)

**Features:**
- Rich text (future: Markdown support)
- Auto-expand on overflow
- Character counter

**Character Counter:**
```javascript
const textarea = document.getElementById('event-description');
const charCount = textarea.value.length;
const maxChars = 2000;
document.getElementById('char-count').textContent = `${charCount}/${maxChars}`;
```

**Used For:**
- Full event details
- Instructions for task
- Context and notes
- Legal descriptions

---

## 3️⃣ Select Dropdown Components

### Event Type Selector
```html
<select class="form-select" id="event-type" required onchange="updatePreview()">
    <option value="">-- Select Type --</option>
    <option value="deadline">⏰ Deadline (Must be done by date)</option>
    <option value="reminder">🔔 Reminder (FYI/follow-up)</option>
    <option value="action_needed">⚡ Action Needed (Do this soon)</option>
    <option value="completed">✓ Completed (Done)</option>
</select>
```

**Properties:**
- **Type**: Dropdown select
- **Required**: Yes
- **Options**: 4 predefined types
- **onChange**: Update preview
- **Icons**: Emoji for visual distinction

**Option Details:**

| Value | Label | Description | Color |
|-------|-------|-------------|-------|
| deadline | ⏰ Deadline | Must be done by date | Red |
| reminder | 🔔 Reminder | FYI/follow-up | Teal |
| action_needed | ⚡ Action Needed | Do this soon | Orange |
| completed | ✓ Completed | Done | Green |

**JavaScript Handling:**
```javascript
const eventType = document.getElementById('event-type').value;
const typeConfig = {
    deadline: { color: 'danger', priority: 2 },
    reminder: { color: 'info', priority: 0 },
    action_needed: { color: 'warning', priority: 1 },
    completed: { color: 'success', priority: 0 }
};
const config = typeConfig[eventType];
```

---

### Priority Level Selector
```html
<select class="form-select" id="event-priority" required onchange="updatePreview()">
    <option value="">-- Select Priority --</option>
    <option value="0">🟢 Low (Can wait)</option>
    <option value="1">🟠 Medium (Soon)</option>
    <option value="2">🔴 High (Urgent)</option>
</select>
```

**Properties:**
- **Type**: Dropdown select
- **Required**: Yes
- **Values**: 0, 1, 2 (numeric)
- **Options**: 3 priority levels
- **Icons**: Colored dots

**Priority Mapping:**

| Value | Label | Icon | Color | CSS Class |
|-------|-------|------|-------|-----------|
| 0 | Low | 🟢 | Green | priority-low |
| 1 | Medium | 🟠 | Orange | priority-medium |
| 2 | High | 🔴 | Red | priority-high |

**Styling:**
```css
.priority-low { background-color: #4caf50; }
.priority-medium { background-color: #ff9800; }
.priority-high { background-color: #f44336; }
```

---

### Category Selector
```html
<select class="form-select" id="event-category" onchange="updatePreview()">
    <option value="">-- Select Category --</option>
    <option value="payment">💰 Payment</option>
    <option value="complaint">📋 Complaint</option>
    <option value="maintenance">🔧 Maintenance</option>
    <option value="evidence">📸 Evidence</option>
    <option value="notice">📬 Notice</option>
    <option value="legal">⚖️ Legal Action</option>
    <option value="communication">💬 Communication</option>
    <option value="other">📌 Other</option>
</select>
```

**Properties:**
- **Type**: Dropdown select
- **Required**: No (defaults to 'other')
- **Options**: 8 predefined categories
- **Icons**: Emoji for quick identification

**Categories:**

| Value | Category | Icon | Usage |
|-------|----------|------|-------|
| payment | Payment | 💰 | Rent, fees, deposits |
| complaint | Complaint | 📋 | Tenant/landlord issues |
| maintenance | Maintenance | 🔧 | Repairs, broken items |
| evidence | Evidence | 📸 | Photos, documents |
| notice | Notice | 📬 | Official notifications |
| legal | Legal Action | ⚖️ | Court, attorney, complaints |
| communication | Communication | 💬 | Emails, calls, meetings |
| other | Other | 📌 | Miscellaneous |

---

### Recurring Pattern Selector
```html
<select class="form-select" id="recurring-pattern">
    <option value="daily">Daily</option>
    <option value="weekly">Weekly</option>
    <option value="biweekly">Every 2 weeks</option>
    <option value="monthly">Monthly</option>
    <option value="yearly">Yearly</option>
</select>
```

**Properties:**
- **Type**: Dropdown select
- **Required**: No (only if recurring enabled)
- **Options**: 5 recurrence patterns
- **Visibility**: Hidden until "Repeat" checkbox checked

**Pattern Details:**

| Pattern | Interval | Example |
|---------|----------|---------|
| daily | Every 24 hours | Habit tracking |
| weekly | Every 7 days | Weekly meetings |
| biweekly | Every 14 days | Bi-weekly reports |
| monthly | Same day each month | Monthly bills |
| yearly | Same date each year | Anniversaries |

---

## 4️⃣ Date/Time Picker Components

### Start Date & Time Picker
```html
<input type="datetime-local" class="form-control" id="event-start" 
       required onchange="updatePreview()">
```

**Properties:**
- **Type**: datetime-local
- **Required**: Yes
- **Format**: YYYY-MM-DDTHH:MM
- **Browser Support**: All modern browsers
- **Fallback**: Text input in older browsers

**Value Format:**
```
2025-11-05T09:30
 ↑ Date part    ↑ Time part
```

**JavaScript Usage:**
```javascript
const startInput = document.getElementById('event-start').value;
const startDate = new Date(startInput);
console.log(startDate); // Wed Nov 05 2025 09:30:00 GMT

// Set to current time
document.getElementById('event-start').valueAsDate = new Date();
```

---

### Due Date Picker
```html
<input type="date" class="form-control" id="event-due" 
       onchange="updatePreview()">
```

**Properties:**
- **Type**: date
- **Required**: No (optional deadline)
- **Format**: YYYY-MM-DD
- **Validation**: Must be >= start date

**Validation:**
```javascript
const startDate = new Date(document.getElementById('event-start').value);
const dueDate = new Date(document.getElementById('event-due').value);

if (dueDate < startDate) {
    showError('Due date must be on or after start date');
    return;
}
```

---

### Recurring Until Date Picker
```html
<input type="date" class="form-select" id="recurring-until">
```

**Properties:**
- **Type**: date
- **Required**: No (repeats indefinitely if empty)
- **Format**: YYYY-MM-DD
- **Visibility**: Only shown when "Repeat" checked

**Purpose:**
- Set end date for recurring events
- Leave empty for continuous recurrence

**Example:**
- Event: "Send monthly reminder"
- Pattern: Monthly
- Until: 2026-12-31
- Result: Monthly reminders from Nov 2025 → Dec 2026

---

## 5️⃣ Checkbox Components

### Recurring Event Checkbox
```html
<div class="checkbox-custom">
    <input type="checkbox" id="recurring-enabled" 
           onchange="toggleRecurringOptions()">
    <label for="recurring-enabled" style="margin: 0; cursor: pointer;">
        Repeat this event
    </label>
</div>
```

**Properties:**
- **Type**: Checkbox
- **Default**: Unchecked
- **onChange**: Toggle recurring options visibility
- **Label**: Clickable

**Behavior:**
```javascript
function toggleRecurringOptions() {
    const enabled = document.getElementById('recurring-enabled').checked;
    document.getElementById('recurring-details').style.display = 
        enabled ? 'block' : 'none';
}
```

---

### Notification Checkboxes
```html
<div class="checkbox-custom">
    <input type="checkbox" id="notify-on-due" checked>
    <label for="notify-on-due">🔔 Notify on due date</label>
</div>

<div class="checkbox-custom">
    <input type="checkbox" id="notify-before-24h" checked>
    <label for="notify-before-24h">🔔 Notify 24 hours before</label>
</div>

<div class="checkbox-custom">
    <input type="checkbox" id="notify-before-7d">
    <label for="notify-before-7d">🔔 Notify 7 days before</label>
</div>

<div class="checkbox-custom">
    <input type="checkbox" id="notify-on-overdue">
    <label for="notify-on-overdue">🔴 Notify if overdue</label>
</div>
```

**Properties:**
- **Type**: Checkbox group
- **Default**: First two checked
- **Labels**: Descriptive text with emoji
- **Independent**: Each can be toggled separately

**Notification Mapping:**

| ID | Trigger | Default | Purpose |
|----|---------|---------|---------| 
| notify-on-due | Due date reached | ✓ | Alert when deadline |
| notify-before-24h | 24h before due | ✓ | Preparation time |
| notify-before-7d | 7 days before | ☐ | Early warning |
| notify-on-overdue | Past due date | ☐ | Overdue alert |

**Serialization:**
```javascript
const notifications = {
    on_due: document.getElementById('notify-on-due').checked,
    before_24h: document.getElementById('notify-before-24h').checked,
    before_7d: document.getElementById('notify-before-7d').checked,
    on_overdue: document.getElementById('notify-on-overdue').checked
};
```

---

## 6️⃣ Button Components

### Create Event Button
```html
<button type="submit" class="btn-primary-custom">✓ Create Event</button>
```

**Properties:**
- **Type**: Submit button
- **Icon**: ✓ Checkmark
- **Color**: Primary blue
- **Hover**: Darker blue, lifted effect
- **Action**: Submit form

**CSS Styling:**
```css
.btn-primary-custom {
    background-color: #2c3e50;
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-primary-custom:hover {
    background-color: #34495e;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
```

---

### Clear Form Button
```html
<button type="reset" class="btn-secondary-custom">↻ Clear Form</button>
```

**Properties:**
- **Type**: Reset button
- **Icon**: ↻ Refresh
- **Color**: Gray
- **Action**: Reset all form fields

---

### Filter Buttons
```html
<button class="quick-filter-btn active" data-filter="all">All Events</button>
<button class="quick-filter-btn" data-filter="deadline">⏰ Deadlines</button>
<button class="quick-filter-btn" data-filter="reminder">🔔 Reminders</button>
```

**Properties:**
- **Type**: Toggle buttons
- **Icon**: Filter type indicator
- **State**: Active (highlighted) / Inactive
- **Data Attribute**: Filter identifier
- **Group**: Mutually exclusive

**Styling:**
```css
.quick-filter-btn {
    padding: 6px 12px;
    border: 2px solid #ddd;
    background-color: white;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
}

.quick-filter-btn.active {
    border-color: var(--info);
    background-color: var(--info);
    color: white;
}

.quick-filter-btn:hover {
    border-color: var(--info);
    background-color: var(--info);
    color: white;
}
```

---

## 7️⃣ Form Layout Components

### Two-Column Row
```html
<div class="row">
    <div class="col-md-6">
        <!-- First column content -->
    </div>
    <div class="col-md-6">
        <!-- Second column content -->
    </div>
</div>
```

**Responsive:**
- Desktop (MD): 2 equal columns
- Tablet/Mobile: Full width (stacked)

---

### Full-Width Section
```html
<div class="row">
    <div class="col-md-12">
        <!-- Full width content -->
    </div>
</div>
```

---

## 8️⃣ Display/Preview Components

### Event Preview Box
```html
<div class="event-form-preview" id="event-preview">
    <div style="font-weight: 600; margin-bottom: 10px;">📝 Event Preview:</div>
    
    <div class="preview-row">
        <div class="preview-label">Title:</div>
        <div class="preview-value" id="preview-title">--</div>
    </div>
    
    <div class="preview-row">
        <div class="preview-label">Type:</div>
        <div class="preview-value" id="preview-type">--</div>
    </div>
    
    <div class="preview-row">
        <div class="preview-label">Priority:</div>
        <div class="preview-value" id="preview-priority">--</div>
    </div>
    
    <div class="preview-row">
        <div class="preview-label">Start:</div>
        <div class="preview-value" id="preview-start">--</div>
    </div>
    
    <div class="preview-row">
        <div class="preview-label">Due:</div>
        <div class="preview-value" id="preview-due">--</div>
    </div>
</div>
```

**Features:**
- Real-time update as user types
- Shows form values before submission
- Helps prevent mistakes
- Read-only display

**Update Function:**
```javascript
function updatePreview() {
    document.getElementById('preview-title').textContent = 
        document.getElementById('event-title').value || '--';
    document.getElementById('preview-type').textContent = 
        document.getElementById('event-type').value || '--';
    // ... etc for all fields
}
```

---

## 9️⃣ Recurring Options Container

### Expandable Recurring Section
```html
<div class="recurring-options">
    <div class="checkbox-custom">
        <input type="checkbox" id="recurring-enabled" 
               onchange="toggleRecurringOptions()">
        <label for="recurring-enabled">Repeat this event</label>
    </div>
    
    <div id="recurring-details" style="display: none; margin-top: 10px;">
        <select class="form-select" id="recurring-pattern">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <!-- ... -->
        </select>
        
        <label class="form-label" style="margin-top: 10px;">Repeat until:</label>
        <input type="date" class="form-control" id="recurring-until">
    </div>
</div>
```

**Behavior:**
- Initially hidden (display: none)
- Shown when "Repeat" checked
- Contains pattern and end date

---

## 🔟 Form Submission & Validation

### Complete Form Submission Flow
```javascript
async function handleAddEvent(e) {
    e.preventDefault();
    
    // 1. Validate inputs
    const title = document.getElementById('event-title').value;
    if (!title) {
        showAlert('Title is required', 'danger');
        return;
    }
    
    // 2. Gather form data
    const eventData = {
        title: title,
        type: document.getElementById('event-type').value,
        priority: parseInt(document.getElementById('event-priority').value),
        start_date: document.getElementById('event-start').value,
        due_date: document.getElementById('event-due').value || null,
        description: document.getElementById('event-description').value,
        category: document.getElementById('event-category').value,
        assignee: document.getElementById('event-assignee').value,
        related_entry_id: document.getElementById('event-ledger-entry').value,
        is_recurring: document.getElementById('recurring-enabled').checked,
        recurring_pattern: document.getElementById('recurring-pattern').value,
        recurring_until: document.getElementById('recurring-until').value,
        notifications: {
            on_due: document.getElementById('notify-on-due').checked,
            before_24h: document.getElementById('notify-before-24h').checked,
            before_7d: document.getElementById('notify-before-7d').checked,
            on_overdue: document.getElementById('notify-on-overdue').checked
        }
    };
    
    // 3. Send to API
    try {
        const response = await fetch('/api/ledger-calendar/calendar/event', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(eventData)
        });
        
        if (response.ok) {
            // 4. Success
            showAlert('Event created successfully!', 'success');
            document.getElementById('event-form').reset();
            loadEvents();
        } else {
            // 5. Error
            showAlert('Error creating event', 'danger');
        }
    } catch (error) {
        console.error(error);
        showAlert('Network error', 'danger');
    }
}
```

---

## ✅ Accessibility Features

### Label Association
```html
<label class="form-label" for="event-title">Event Title *</label>
<input type="text" class="form-control" id="event-title">
```

### ARIA Labels
```html
<input type="text" id="search" aria-label="Search events"
       placeholder="Search...">
```

### Keyboard Navigation
- Tab: Move to next field
- Shift+Tab: Move to previous field
- Enter: Submit form
- Escape: Close modal
- Space: Toggle checkbox

### Screen Reader Support
- Semantic HTML (labels, fieldsets, etc.)
- ARIA attributes for complex widgets
- Status messages announced

---

## 📱 Mobile Considerations

### Touch-Friendly Sizing
```css
input, select, textarea, button {
    min-height: 44px;  /* iOS minimum touch target */
    min-width: 44px;
}
```

### Mobile Date/Time Input
```html
<!-- Desktop: datetime-local picker -->
<!-- Mobile: Native date/time wheels -->
<input type="datetime-local" id="event-start">
```

### Responsive Buttons
```css
@media (max-width: 576px) {
    button {
        width: 100%;
        margin-bottom: 10px;
    }
    
    .row {
        flex-direction: column;
    }
}
```

---

## 🎯 Summary

**Input Components Used:**
- 3× Text inputs (title, ledger entry, assignee)
- 1× Textarea (description)
- 4× Dropdowns (type, priority, category, recurrence)
- 2× Date pickers (start, due)
- 1× DateTime picker (start with time)
- 5× Checkboxes (recurring, 4 notifications)
- 2× Buttons (submit, reset)
- Filter buttons (8×)

**Total Input Fields: 20+**

**API Integration:**
- Single POST endpoint
- All fields serialized to JSON
- Response includes event ID
- Error handling with alerts

