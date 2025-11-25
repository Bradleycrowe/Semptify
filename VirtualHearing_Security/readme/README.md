# Virtual Hearing Security Flow - Semptify

**Version:** 1.0.0  
**Date:** 2025-11-25  
**For:** Dakota County Eviction Defense

## Purpose

Secure, compliant interface for tenants joining virtual eviction hearings through Minnesota Judicial Branch Zoom sessions. Ensures proper authentication, device readiness, document security, and court rule compliance.

## Features

### 🔒 Trust Banner
- Displays encryption status
- Explains court security measures
- Clarifies recording prohibition

### 👤 Identity Verification (Step 1)
- Legal name (must match summons)
- Case number validation
- Summons and hearing date tracking

### ✅ Readiness Checklist (Step 2)
- Name confirmation
- Device testing (camera/mic)
- Document submission reminder (eFS only)
- Interpreter request option
- Security rules acknowledgment

### 📄 Prepared Participant Certificate (Step 3)
- Symbolic confidence badge
- Downloadable/printable certificate
- Timestamp verification
- "Ready for secure hearing" status

### �� Secure Redirect Panel (Step 4)
- Verified court links only
- eFile & eServe portal
- Court records search (MCRO)
- Housing Resource Line
- "VERIFIED" badges for trust

### ⏳ Waiting Room Status (Step 5)
- Real-time admission tracking
- Calming instructions
- Final preparation tips

## Usage

### Direct Access
Open `flows/virtual_hearing_security.html` in any browser.

### Integration with Semptify
```html
<a href="/VirtualHearing_Security/flows/virtual_hearing_security.html" class="btn">
  Join Secure Hearing
</a>
```

### From Dakota County Module
Link from main eviction defense:
- Process Flow → Virtual Hearing Security
- Timeline Tracker → Join Hearing button

## Security Compliance

### Court Requirements Met
✅ Encryption disclosure  
✅ Identity verification  
✅ Recording prohibition notice  
✅ Official portal redirection  
✅ Waiting room simulation  

### Data Protection
- No sensitive data stored
- Audit logs optional (local only)
- Certificate generation client-side
- No external API calls (except official court links)

## File Structure

```
VirtualHearing_Security/
├── flows/
│   └── virtual_hearing_security.html   # Main interface
├── data/
│   └── security_config.json            # Court requirements
├── logs/
│   └── audit_log_template.md           # Optional tracking
├── certificates/                       # Generated certificates
└── readme/
    └── README.md                       # This file
```

## Customization

### Multilingual Support
Add translation strings to `security_config.json`:
```json
"translations": {
  "es": {
    "trust_banner": "Conexión segura gestionada por el tribunal",
    "step1_title": "Verificación de Identidad"
  }
}
```

### Branding
Modify CSS variables in `virtual_hearing_security.html`:
```css
:root {
  --primary-color: #667eea;
  --secondary-color: #38b2ac;
}
```

## Legal Disclaimer

This interface assists with virtual hearing access but does not provide legal advice. Tenants should consult with legal aid or an attorney for case-specific guidance.

**Free Legal Help:**
- Minnesota Legal Aid: 651-297-1274
- Housing Resource Line: 651-554-5751
- LawHelp MN: https://www.lawhelpmn.org/

## Support

**Maintainer:** Semptify Development Team  
**Contact:** Via GitHub issues or Semptify support

## Version History

- **1.0.0** (2025-11-25): Initial release
  - Complete 5-step security flow
  - Trust banner and encryption disclosure
  - Device testing and readiness checklist
  - Prepared Participant Certificate
  - Verified link panel
  - Waiting room status tracker

---

**Made with ❤️ for tenant justice and court security compliance**
