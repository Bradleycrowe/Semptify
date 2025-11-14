# Semptify UI - Responsive Design Guide

## Understanding Column Widths, Breakpoints, and Card Sizes

---

## Table of Contents
1. [Column Count](#column-count)
2. [Breakpoints](#breakpoints)
3. [Card Sizes](#card-sizes)
4. [Calculating Column Widths](#calculating-column-widths)
5. [Current Implementation](#current-implementation)
6. [Customization Examples](#customization-examples)

---

## Column Count

**What it controls:** How many cards appear side-by-side at different screen sizes.

### Current Implementation in `dashboard_simple.html`:
```css
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
```

### What This Means:
- `repeat(auto-fit, ...)` = Browser automatically decides how many columns fit
- `minmax(280px, 1fr)` = Each card is minimum 280px, maximum equal width (1fr)

### Real-World Results:
| Screen Size | Width | Columns | Reason |
|-------------|-------|---------|--------|
| **Phone** | 375px | 1 | Only 280px fits |
| **Tablet** | 768px | 2 | 2×280px = 560px fits |
| **Desktop** | 1200px | 3-4 | 4×280px = 1120px fits |

### Manual Column Control (Alternative):
```css
/* Force specific columns at each breakpoint */
@media (min-width: 768px) {
    grid-template-columns: repeat(2, 1fr);  /* 2 columns */
}
@media (min-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);  /* 3 columns */
}
```

---

## Breakpoints

**What they are:** Screen widths where the design changes layout.

### Current Breakpoints in `style.css`:
```css
@media (min-width: 768px) {
    /* Tablet and up */
    .container { width: 90%; max-width: 1200px; }
    header nav { width: auto; }
}
```

### Standard Breakpoint Ranges:
| Range | Device Type | Typical Columns |
|-------|-------------|-----------------|
| **320px - 767px** | Mobile phones | 1 column |
| **768px - 1023px** | Tablets | 2 columns |
| **1024px - 1199px** | Laptops | 3 columns |
| **1200px+** | Desktops | 4 columns |

### Bootstrap 5 Breakpoints (Used by Semptify):
| Name | Min Width | Device |
|------|-----------|--------|
| `sm` | 576px | Small phones |
| `md` | 768px | Tablets |
| `lg` | 992px | Laptops |
| `xl` | 1200px | Desktops |
| `xxl` | 1400px | Large screens |

### Why 768px?
This is the typical width where tablets switch from portrait to landscape mode.

---

## Card Sizes

**What it controls:** The dimensions of action cards in the dashboard.

### Current Card Sizing in `dashboard_simple.html`:
```css
.action-card {
    padding: 30px;           /* Internal spacing */
    border-radius: 15px;     /* Rounded corners */
    /* Width controlled by grid: minmax(280px, 1fr) */
}

.action-icon {
    font-size: 48px;         /* Icon size */
}

.action-title {
    font-size: 20px;         /* Title text */
}

.action-description {
    font-size: 14px;         /* Description text */
}
```

### Card Width Logic:
- **Minimum:** 280px (won't shrink smaller)
- **Maximum:** 1fr (equal share of available space)
- **Gap between cards:** 20px

### Example Calculation (1200px screen with 4 cards):
```
Available space = 1200px - (3 gaps × 20px) = 1140px
Each card width = 1140px ÷ 4 = 285px
```

### Adjusting Card Sizes:
```css
/* Larger minimum (fewer cards per row) */
minmax(350px, 1fr)  /* Forces max 3 cards on 1200px screen */

/* Smaller minimum (more cards per row) */
minmax(220px, 1fr)  /* Allows 5 cards on 1200px screen */
```

---

## Calculating Column Widths

### Formula:
```
Column Width = (Container Width - (Number of Gaps × Gap Size)) ÷ Number of Columns
```

### Current Setup Calculations:

#### **Mobile (320px - 767px)**
- Container: `95%` of screen = ~304px on 320px phone
- Columns: **1** (only 280px minmax fits)
- Gaps: 0
- **Column width: ~304px** (full width minus padding)

**Calculation:**
```
304px - (0 gaps × 20px) = 304px
304px ÷ 1 column = 304px per card
```

---

#### **Tablet (768px)**
- Container: `90%` = ~691px
- Columns: **2** (2×280px = 560px fits)
- Gaps: 1 × 20px = 20px
- **Column width: 335px each**

**Calculation:**
```
691px - (1 gap × 20px) = 671px
671px ÷ 2 columns = 335.5px per card
```

---

#### **Desktop (1024px)**
- Container: `90%` = ~922px
- Columns: **3** (3×280px = 840px fits)
- Gaps: 2 × 20px = 40px
- **Column width: 294px each**

**Calculation:**
```
922px - (2 gaps × 20px) = 882px
882px ÷ 3 columns = 294px per card
```

---

#### **Large Desktop (1200px+)**
- Container: `90%` capped at `1200px` max
- Columns: **4** (4×280px = 1120px fits)
- Gaps: 3 × 20px = 60px
- **Column width: 285px each**

**Calculation:**
```
1200px - (3 gaps × 20px) = 1140px
1140px ÷ 4 columns = 285px per card
```

---

## Current Implementation

### File: `dashboard_simple.html`

```css
.actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
}
```

### File: `style.css`

```css
/* Mobile First - Default */
.container {
    width: 95%;
    margin: 0 auto;
    padding: 15px 0;
}

/* Tablet and Desktop */
@media (min-width: 768px) {
    .container {
        width: 90%;
        max-width: 1200px;
    }
}
```

---

## Customization Examples

### Example 1: Exact Pixel Widths at Each Breakpoint

```css
/* Mobile: 1 column, full width */
.actions-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}

/* Tablet: 2 columns, exactly 340px each */
@media (min-width: 768px) {
    .actions-grid {
        grid-template-columns: 340px 340px;
        justify-content: center;
    }
}

/* Desktop: 3 columns, exactly 300px each */
@media (min-width: 1024px) {
    .actions-grid {
        grid-template-columns: 300px 300px 300px;
    }
}

/* Large Desktop: 4 columns, exactly 280px each */
@media (min-width: 1200px) {
    .actions-grid {
        grid-template-columns: 280px 280px 280px 280px;
    }
}
```

---

### Example 2: Percentage-Based Widths

```css
/* Mobile: 1 column, full width */
.actions-grid {
    display: grid;
    grid-template-columns: 100%;
    gap: 20px;
}

/* Tablet: 2 equal columns at 48% each (4% total gap) */
@media (min-width: 768px) {
    .actions-grid {
        grid-template-columns: 48% 48%;
        gap: 4%;
    }
}

/* Desktop: 3 equal columns at 31% each */
@media (min-width: 1024px) {
    .actions-grid {
        grid-template-columns: 31% 31% 31%;
        gap: 3.5%;
    }
}
```

---

### Example 3: Asymmetric Column Widths (Custom Layout)

```css
/* Desktop: 3 columns with different widths */
@media (min-width: 1024px) {
    .actions-grid {
        grid-template-columns: 20% 65% 15%;
        gap: 20px;
    }
}
```

**Result on 1200px container:**
- **Column 1 (left):** 240px (20% of 1200px)
- **Column 2 (center):** 780px (65% of 1200px)
- **Column 3 (right):** 180px (15% of 1200px)

---

### Example 4: Mixed Units (Sidebar + Content)

```css
/* Desktop: Sidebar + Main Content */
@media (min-width: 1024px) {
    .actions-grid {
        grid-template-columns: 250px 1fr;  /* Fixed sidebar, flexible content */
        gap: 30px;
    }
}
```

---

## Quick Reference Table

### Current Semptify Layout at Different Screens:

| Screen Width | Container Width | Columns | Gap | Card Width | Total Cards Visible |
|--------------|-----------------|---------|-----|------------|---------------------|
| 320px (Phone) | 304px (95%) | 1 | 0px | 304px | 1 |
| 375px (iPhone) | 356px (95%) | 1 | 0px | 356px | 1 |
| 768px (Tablet) | 691px (90%) | 2 | 20px | 335px | 2 |
| 1024px (Laptop) | 922px (90%) | 3 | 40px | 294px | 3 |
| 1200px (Desktop) | 1200px (max) | 4 | 60px | 285px | 4 |

---

## Tips for Customization

### 1. **Maintain Minimum Card Width**
Always ensure cards don't get too narrow:
```css
minmax(280px, 1fr)  /* Good - readable on all devices */
minmax(150px, 1fr)  /* Too narrow - text cramped */
```

### 2. **Consider Content**
- **Text-heavy cards:** Need wider columns (300px+)
- **Icon-only cards:** Can be narrower (200px+)
- **Image cards:** Match aspect ratio (e.g., 300px for 3:4 images)

### 3. **Test Gap Sizes**
```css
gap: 10px;  /* Tight, compact look */
gap: 20px;  /* Balanced (current) */
gap: 40px;  /* Spacious, airy */
```

### 4. **Use Browser DevTools**
- Press F12 in browser
- Click "Toggle Device Toolbar" (Ctrl+Shift+M)
- Test different screen sizes
- Inspect computed widths in real-time

---

## Converting to PDF

### Method 1: VS Code Extension
1. Install "Markdown PDF" extension
2. Open this file
3. Press `Ctrl+Shift+P`
4. Type "Markdown PDF: Export (pdf)"
5. Done!

### Method 2: Online Converter
1. Visit: https://www.markdowntopdf.com/
2. Copy/paste this file's content
3. Click "Convert"
4. Download PDF

### Method 3: Pandoc (Command Line)
```powershell
pandoc UI_RESPONSIVE_DESIGN_GUIDE.md -o UI_RESPONSIVE_DESIGN_GUIDE.pdf
```

---

**Document Created:** November 13, 2025  
**Semptify Version:** Current  
**Last Updated:** See file modification date
