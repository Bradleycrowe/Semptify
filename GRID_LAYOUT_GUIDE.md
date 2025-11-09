# Semptify Page Grid Layout System
## 6 Rows × 3 Columns Master Template

---

## 📐 Grid Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                          HEADER (Full Width)                         │
│                    Logo | Title | User Menu | Settings               │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────┬──────────────────────┐
│                      │                      │                      │
│   ROW 1 | COL 1      │   ROW 1 | COL 2      │   ROW 1 | COL 3      │
│  (Stage Selector)    │   (Quick Stats)      │   (User Info Card)   │
│                      │                      │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│                      │                      │                      │
│   ROW 2 | COL 1      │   ROW 2 | COL 2      │   ROW 2 | COL 3      │
│ (Current Issue/      │  (Next Steps Box)    │  (Resources Panel)   │
│  Status Display)     │                      │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│                      │                      │                      │
│   ROW 3 | COL 1      │   ROW 3 | COL 2      │   ROW 3 | COL 3      │
│  (Timeline/          │  (Legal Info Box)    │  (Warnings/Alerts)   │
│   Progress Bar)      │                      │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│                      │                      │                      │
│   ROW 4 | COL 1      │   ROW 4 | COL 2      │   ROW 4 | COL 3      │
│  (Action Buttons)    │  (Learning/AI Tips)  │  (Contact Resources) │
│                      │                      │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│                      │                      │                      │
│   ROW 5 | COL 1      │   ROW 5 | COL 2      │   ROW 5 | COL 3      │
│  (History/Past)      │  (Documents Upload)  │  (Case Files Vault)  │
│                      │                      │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│                      │                      │                      │
│   ROW 6 | COL 1      │   ROW 6 | COL 2      │   ROW 6 | COL 3      │
│  (Debug/Footer)      │  (Footer Navigation) │  (Help/Support)      │
│                      │                      │                      │
└──────────────────────┴──────────────────────┴──────────────────────┘
```

---

## 🎯 Detailed Grid Cell Reference

### **ROW 1: User Status & Overview**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Stage Selector** | **Quick Stats** | **User Card** |
| Dropdown: "Currently I am:" | Rent, Status, Deadline | Name, Contact, Location |
| SEARCHING / APPLYING / ... | Progress %, Next Action | Verified Badge |
| Change Stage Button | Key Metrics | Edit Profile Link |

### **ROW 2: Current Situation & Actions**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Issue/Status Display** | **Next Steps** | **Resources** |
| What's happening NOW | 1. Do this | Links to Help |
| Icon + Description | 2. Then this | Programs Available |
| Severity Level | 3. Finally this | Local Contacts |

### **ROW 3: Tracking & Legal**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Timeline/Progress** | **Legal Information** | **Warnings/Alerts** |
| Visual timeline bar | Applicable laws | Critical warnings |
| Days since issue | Rights summary | Required actions |
| Milestones marked | Procedures to follow | Time-sensitive items |

### **ROW 4: Actions & Learning**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Primary Actions** | **AI Tips/Learning** | **Help & Support** |
| Main CTA buttons | Smart suggestions | Contact info |
| File complaint, etc. | "Try this..." | Phone/Email/Chat |
| Export document | "Success tip" | FAQ Links |

### **ROW 5: Records & Evidence**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **History/Past** | **Upload Documents** | **Vault/Case Files** |
| Previous issues | Drag & drop area | All stored docs |
| Past resolutions | File picker | Organized by type |
| Timeline view | Preview on upload | Search/filter |

### **ROW 6: Navigation & Support**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Debug/System** | **Footer Nav** | **Help & Feedback** |
| Dev info (hidden) | Home, About, Terms | Support tickets |
| Stage data display | Privacy, Contact | Send feedback |
| Logs (admin only) | Version info | Documentation |

---

## 📱 CSS Grid Implementation

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;  /* 3 equal columns */
  grid-template-rows: auto auto auto auto auto auto;  /* 6 rows */
  gap: 20px;  /* Space between cells */
  padding: 20px;
  max-width: 1400px;
}

.grid-cell {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Specific cell positioning */
.row1-col1 { grid-column: 1; grid-row: 1; }
.row1-col2 { grid-column: 2; grid-row: 1; }
.row1-col3 { grid-column: 3; grid-row: 1; }

.row2-col1 { grid-column: 1; grid-row: 2; }
.row2-col2 { grid-column: 2; grid-row: 2; }
.row2-col3 { grid-column: 3; grid-row: 2; }

/* ... and so on for all 6 rows */

/* Wide components spanning multiple columns */
.full-width { grid-column: 1 / -1; }  /* Spans all 3 columns */
.two-cols { grid-column: span 2; }     /* Spans 2 columns */
```

---

## 🔄 Stage-Aware Grid Example

### **When User Selects: "SEARCHING"**

| ROW 1, COL 1 | ROW 1, COL 2 | ROW 1, COL 3 |
|--------------|--------------|--------------|
| Stage: **SEARCHING** ✏️ | 0% Complete | User: John Doe |

| ROW 2, COL 1 | ROW 2, COL 2 | ROW 2, COL 3 |
|--------------|--------------|--------------|
| Looking for apartment in Eagan, MN | Next: Apply to listings | Available: 12 rentals |

| ROW 3, COL 1 | ROW 3, COL 2 | ROW 3, COL 3 |
|--------------|--------------|--------------|
| Timeline: Day 1 of search | Fair Housing Act | ⚠️ Budget concerns |

---

### **When User Selects: "HAVING TROUBLE"**

| ROW 1, COL 1 | ROW 1, COL 2 | ROW 1, COL 3 |
|--------------|--------------|--------------|
| Stage: **HAVING TROUBLE** ✏️ | Issue: No Heat | User: John Doe |

| ROW 2, COL 1 | ROW 2, COL 2 | ROW 2, COL 3 |
|--------------|--------------|--------------|
| 🔴 EMERGENCY: No heat 48hrs | 1. Document NOW | Tenant Rights Orgs |

| ROW 3, COL 1 | ROW 3, COL 2 | ROW 3, COL 3 |
|--------------|--------------|--------------|
| Deadline: 7 days to respond | Minnesota § 504B.365 | 🚨 CRITICAL: Health hazard |

---

## ✅ Does This Work?

**Advantages:**
- ✅ Consistent layout across all pages
- ✅ Easy to rearrange components
- ✅ Responsive (can stack on mobile)
- ✅ Stage-specific content fills the grid
- ✅ Clear hierarchy and organization
- ✅ All elements visible without scrolling on desktop

**Responsive Breakdown:**
- **Desktop (1400px+):** 3 columns as shown
- **Tablet (768-1200px):** Collapse to 2 columns
- **Mobile (< 768px):** Stack to 1 column

---

## 🚀 Ready to Implement?

Should I create:
1. **HTML template** with this 6×3 grid structure?
2. **CSS styling** for responsive layout?
3. **Stage-specific content** that fills each cell?
4. **JavaScript** to swap content when stage changes?

**Confirm:** Does this grid layout work for your vision?

