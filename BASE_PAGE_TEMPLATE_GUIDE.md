# Base Page Template Guide

## File: `templates/base_page.html`

### Quick Start
Create a new page by extending the base template:

```html
{% extends "base_page.html" %}

{% block title %}My Page - Semptify{% endblock %}
{% block page_title %}My Page Title{% endblock %}

{% block content %}
    <!-- Your page content here -->
{% endblock %}
```

## Available Blocks

### Required Blocks
- `{% block content %}` - Main page content area

### Optional Blocks
- `{% block title %}` - Browser tab title (default: "Semptify")
- `{% block meta_description %}` - SEO description
- `{% block page_title %}` - H1 heading in page header
- `{% block page_header %}` - Override entire header section
- `{% block nav_items %}` - Customize navigation menu items
- `{% block extra_css %}` - Add page-specific CSS
- `{% block extra_js %}` - Add page-specific JavaScript

## Features Included

✅ **Responsive Layout**: Mobile-first Bootstrap 5 grid
✅ **Navigation Bar**: Collapsible menu with brand colors
✅ **Footer**: Links and tenant-friendly messaging
✅ **Brand Colors**: 
   - `--brand-maroon`: #500000
   - `--brand-gold`: #d4af37
   - `--brand-gradient`: maroon → gold
✅ **Cards**: Pre-styled with shadows and rounded corners
✅ **Buttons**: Primary button uses brand maroon
✅ **Typography**: System font stack for performance

## Common Use Cases

### 1. Simple Content Page
```html
{% extends "base_page.html" %}
{% block title %}About - Semptify{% endblock %}
{% block page_title %}About Us{% endblock %}
{% block content %}
<div class="card">
    <div class="card-body">
        <p>Your content here</p>
    </div>
</div>
{% endblock %}
```

### 2. Form Page
```html
{% extends "base_page.html" %}
{% block page_title %}Contact Form{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
                    <!-- form fields -->
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3. Custom Navigation
```html
{% extends "base_page.html" %}
{% block nav_items %}
<li class="nav-item">
    <a class="nav-link" href="/custom">Custom Link</a>
</li>
{{ super() }}  <!-- Include default nav items -->
{% endblock %}
```

### 4. Page-Specific Styles
```html
{% extends "base_page.html" %}
{% block extra_css %}
<style>
    .my-special-class {
        color: var(--brand-gold);
        font-weight: bold;
    }
</style>
{% endblock %}
```

## Best Practices

1. **Always set page title**: Improves SEO and user experience
2. **Use card containers**: Keeps content organized and styled
3. **Leverage Bootstrap grid**: `row` and `col-*` classes for layout
4. **Use brand colors**: Reference CSS variables for consistency
5. **Mobile-first**: Test responsive behavior at all breakpoints

## Example Route Handler
```python
@app.route('/my-page')
def my_page():
    return render_template('my_page.html',
                         page_subtitle='Optional subtitle text',
                         data={'key': 'value'})
```

## File Naming Convention
- Template files: `snake_case.html`
- Location: `templates/` (or blueprint subfolder)
- Example file: `templates/example_new_page.html`

---
See `templates/example_new_page.html` for complete working example.
