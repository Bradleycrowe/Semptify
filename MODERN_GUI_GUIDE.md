# MODERN_GUI_GUIDE.md - Human-Centered Desktop Interface

## Overview
Completely redesigned GUI optimized for desktop/laptop use with:
- **Smooth UX Flow**: Intuitive multi-step wizards
- **Smart Auto-Fill**: Max 3 suggestions per field, learns from usage
- **Interactive Tooltips**: Hover for context and instructions
- **Modern Components**: Toggles, checkboxes, progress indicators
- **Contextual Design**: Human-friendly labels and descriptions

## Key Features

### 1. Smart Auto-Fill System
**Max 3 Choices** - Never overwhelming
- Learns from your input patterns
- Context-aware (different suggestions for different forms)
- Profile-specific (remembers per client/case)
- Frequency-based ranking (most-used appears first)

**How It Works**:
- Type in any field with `data-autofill` attribute
- Suggestions appear after 1 character
- Click to select or keep typing
- System records your choice for future suggestions

**Example**:
```html
<input type="text" 
       class="form-input" 
       data-autofill="landlord_name" 
       data-context="complaint"
       placeholder="Enter landlord name">
```

### 2. Interactive Tooltips
**Hover for Help** - No clutter, always available
- `?` icon next to labels
- Appears on mouse hover
- Clear, concise explanations
- Context-specific instructions

**Example**:
```html
<label class="form-label">
    Property Address
    <span class="tooltip-wrapper">
        <span class="tooltip-icon">?</span>
        <span class="tooltip-content">Full address including unit number</span>
    </span>
</label>
```

### 3. Toggle Switches
**On/Off Options** - Visual and tactile
- Smooth animation
- Clear active state (blue = on, gray = off)
- Perfect for yes/no options

**Example**:
```html
<div class="toggle-container">
    <div class="toggle-switch">
        <div class="toggle-knob"></div>
        <input type="hidden" name="urgent" value="0">
    </div>
    <label class="toggle-label">Mark as Urgent</label>
</div>
```

### 4. Modern Checkboxes
**Multiple Selections** - Clean design
- Custom styled (no ugly browser defaults)
- Visual check mark (✓) when selected
- Can combine with tooltips

**Example**:
```html
<div class="checkbox-container">
    <div class="checkbox-box">
        <span class="checkbox-check">✓</span>
    </div>
    <input type="checkbox" name="issue_maintenance" style="display:none">
    <label class="checkbox-label">Maintenance Issues</label>
</div>
```

### 5. Progress Indicators
**Multi-Step Wizards** - Always know where you are
- Visual steps with circles
- Active step highlighted
- Completed steps get green check
- Progress bar animates

### 6. Smooth Buttons
**Action Buttons** - Clear hierarchy
- Primary: Blue gradient with shadow, hover lifts
- Secondary: Gray background, subtle hover
- Icons supported for clarity

---

## URL Structure

### Main Routes
- **`/app`** - Modern GUI home
- **`/app/complaint`** - Complaint filing wizard
- **`/app/vault`** - Document vault (drag-drop)
- **`/app/timeline`** - Visual timeline builder
- **`/app/ledger`** - Financial ledger

### Auto-Fill API
- **POST `/app/api/autofill/suggest`**
  - Get suggestions (max 3)
  - Body: `{field, partial, context}`
  - Returns: `{suggestions: [{value, count, score}]}`

- **POST `/app/api/autofill/record`**
  - Record user input for learning
  - Body: `{field, value, context}`

- **POST `/app/api/autofill/predict`**
  - Predict related field (e.g., address → city)
  - Body: `{source_field, source_value, target_field}`

---

## Creating New Pages

### 1. Create Template (templates/modern_gui/your_page.html)
```html
{% extends "modern_gui/base.html" %}

{% block title %}Your Page Title{% endblock %}
{% block header_title %}Page Header{% endblock %}

{% block content %}
<form id="yourForm">
    <div class="form-section">
        <h2>Section Title</h2>
        
        <!-- Auto-fill input -->
        <div class="form-group">
            <label class="form-label">
                Field Label
                <span class="tooltip-wrapper">
                    <span class="tooltip-icon">?</span>
                    <span class="tooltip-content">Help text here</span>
                </span>
            </label>
            <input type="text" 
                   class="form-input" 
                   data-autofill="field_name" 
                   data-context="your_context">
        </div>
        
        <!-- Toggle -->
        <div class="toggle-container">
            <div class="toggle-switch">
                <div class="toggle-knob"></div>
                <input type="hidden" name="option" value="0">
            </div>
            <label class="toggle-label">Option Label</label>
        </div>
        
        <!-- Checkbox -->
        <div class="checkbox-container">
            <div class="checkbox-box">
                <span class="checkbox-check">✓</span>
            </div>
            <input type="checkbox" name="choice" style="display:none">
            <label class="checkbox-label">Choice Label</label>
        </div>
        
        <button type="submit" class="btn btn-primary">Submit</button>
    </div>
</form>
{% endblock %}
```

### 2. Add Route (modern_gui_routes.py)
```python
@modern_gui_bp.route("/your-page")
def your_page():
    profile = get_active_profile()
    return render_template("modern_gui/your_page.html", profile=profile)
```

---

## Auto-Fill Configuration

### Field Naming Convention
Use descriptive names that indicate the field's purpose:
- `landlord_name` - Landlord's name
- `property_address` - Property address
- `city` - City name
- `issue_description` - Issue description

### Context Types
Define context to separate different form types:
- `complaint` - Complaint forms
- `lease` - Lease documents
- `maintenance` - Maintenance requests
- `financial` - Payment/ledger forms
- `general` - Default context

### Max 3 Suggestions Rule
System automatically:
1. Ranks by frequency (profile > context > general)
2. Filters by partial match
3. Returns top 3 only
4. Shows usage count ("Used 5 time(s)")

---

## Customization

### Colors
Edit base.html `<style>` section:
- Primary: `#4A90E2` (blue)
- Secondary: `#f0f0f0` (gray)
- Success: `#4CAF50` (green)
- Gradient: `#667eea` to `#764ba2`

### Animations
All transitions set to `0.3s` for smooth feel.
Change in `.btn`, `.toggle-switch`, `.form-input:focus`, etc.

### Tooltips
Adjust position, size, or timing in `.tooltip-content` styles.

---

## Testing the GUI

### 1. Start Server
```powershell
.\Semptify_Launcher.ps1
```

### 2. Access Modern GUI
Browser: `http://localhost:8080/app`

### 3. Test Auto-Fill
1. Go to `/app/complaint`
2. Type in "Landlord Name" field
3. Enter a name, blur field (click outside)
4. Type again - should see suggestion appear
5. Use field 3 times with different names
6. Type again - should see max 3 suggestions ranked by frequency

### 4. Test Components
- **Tooltips**: Hover over `?` icons
- **Toggles**: Click switches (watch smooth animation)
- **Checkboxes**: Click to select/deselect
- **Progress**: Multi-step forms show progress bar

---

## Integration with Existing Modules

### Vault Integration
```python
from storage_manager import upload_file

@modern_gui_bp.route("/vault/upload", methods=["POST"])
def vault_upload():
    file = request.files['document']
    profile_id = get_active_profile()['id']
    upload_file(profile_id, file.filename, file.read())
    return jsonify({"success": True})
```

### Timeline Integration
Use auto-fill for event titles, locations, descriptions.

### Ledger Integration
Auto-fill for payee names, categories, recurring entries.

---

## Accessibility

- **Keyboard Navigation**: All components focusable
- **Screen Readers**: Proper labels and ARIA attributes
- **Contrast**: WCAG AA compliant colors
- **Focus States**: Clear blue outline on focus

---

## Performance

- **Auto-fill Caching**: Suggestions loaded once per field
- **Debouncing**: 300ms delay before showing suggestions
- **Local Storage**: Patterns stored locally (`data/autofill_patterns.json`)
- **Max 3 Results**: Prevents overwhelming dropdowns

---

## Next Steps

1. **Build More Forms**: Use templates as reference
2. **Customize Auto-Fill**: Add field relationships
3. **Add Intensity**: Integrate with existing modules
4. **User Testing**: Get feedback on flow and UX

