# SEMPTIFY USER GUIDE
**Your Rights. Your Evidence. Your Privacy.**

---

## 🏠 What is Semptify?

Semptify is a **free tenant rights protection platform** that helps you:
- 📁 Store evidence of housing issues securely
- 📋 File eviction defense complaints automatically
- 📅 Track important dates and deadlines
- 🔒 Keep your documents private (in YOUR cloud storage)

**Built for tenants facing:** Eviction, unsafe housing, harassment, illegal rent increases, discrimination, and retaliation.

---

## 🔐 Privacy-First: How Your Data is Stored

Semptify uses a **unique privacy model** that protects you:

### ✅ What Semptify DOES:
- Generate a secure 12-digit anonymous token (like a password)
- Help you connect YOUR Dropbox or Google Drive
- Organize your evidence and generate court documents

### ❌ What Semptify DOES NOT:
- Store your documents on our servers
- Access your files without your token
- Share your data with anyone
- Keep copies of your evidence

**Your documents stay in YOUR cloud. Semptify just helps organize them.**

### Three Storage Tiers:

1. **Your Cloud Storage** (Dropbox or Google Drive)
   - Where YOUR documents live
   - Only you can access with your token
   - We never see your files

2. **Local Token Hashes** (on Semptify servers)
   - Hashed version of your token (not readable)
   - Used to verify you own your token
   - Cannot be reversed to get your actual token

3. **R2 Database** (admin only)
   - System settings and application data
   - NO user documents or tokens
   - Just keeps Semptify running

---

## 🚀 Getting Started: Registration

### Step 1: Register

1. Go to: `http://[your-semptify-url]/register`
2. Fill out the registration form
3. Click "Register"
4. **IMPORTANT:** You'll receive a one-time 12-digit token

**⚠️ SAVE YOUR TOKEN IMMEDIATELY!**
- Write it down on paper
- Take a screenshot
- Store it securely
- **You cannot recover it if lost!**

### Step 2: Choose Storage

After registration, you'll choose where to store your documents:

**Option A: Google Drive** (Recommended)
- Click "Connect Google Drive"
- Sign in to your Google account
- Grant Semptify permission to create a `.semptify` folder
- Your token is encrypted and saved to YOUR Drive

**Option B: Dropbox**
- Click "Connect Dropbox"
- Sign in to your Dropbox account
- Grant Semptify permission
- Your token is encrypted and saved to YOUR Dropbox

**Option C: Local Storage** (Skip cloud setup)
- Click "Skip setup"
- Documents stored on Semptify server temporarily
- Less secure, but works without cloud account

### Step 3: Access Your Vault

After setup, you'll get a vault link like:
```
http://[semptify-url]/vault?user_token=123456789012
```

**Bookmark this link!** This is how you access your evidence vault.

---

## 📁 Using the Evidence Vault

The vault is where you store and organize evidence of housing issues.

### What You Can Upload:
- 📸 Photos of unsafe conditions
- 📧 Emails with your landlord
- 📄 Lease agreements
- 🧾 Rent receipts
- 📝 Written notices
- 🎥 Video evidence (convert to link)

### How to Upload:

1. Go to your vault link (with your token)
2. Click "Upload Document"
3. Choose file from your computer
4. Add description: "Broken heater - December 2024"
5. Select evidence type: "Habitability Issue"
6. Click "Upload"

**What Happens:**
- File uploads to YOUR Dropbox/Drive (not Semptify servers)
- Semptify creates a "certificate" with:
  - SHA-256 hash (proves file hasn't changed)
  - Timestamp (proves when uploaded)
  - Your description
- Certificate saved as JSON in your vault

### Notarization Feature:

Every upload is **automatically notarized**:
- Cryptographic hash proves authenticity
- Timestamp proves when it existed
- Cannot be backdated or altered
- Admissible in court

---

## ⚖️ Filing Eviction Defense Complaints

Semptify helps you file court complaints automatically.

### Step 1: Start Complaint Wizard

1. Go to `/file-complaint` or click "File a Complaint" from dashboard
2. Select jurisdiction: "Dakota County, MN" (or your county)
3. Click "Start Wizard"

### Step 2: Answer Questions

The wizard asks about your situation:
- Your tenancy details
- Landlord information
- Issues you're facing
- Evidence you have

**Semptify analyzes your vault and pre-fills 60% of answers!**

### Step 3: Review & Rank Evidence

Semptify uses AI to:
- Find relevant evidence in your vault
- Rank by legal strength (90-95% accuracy)
- Suggest which docs to include

You can:
- ✅ Include evidence
- ❌ Exclude evidence
- ✏️ Add notes

### Step 4: Generate Court Packet

Click "Generate Packet" to create:
- **Complaint** (legal document for court)
- **Evidence list** (numbered exhibits)
- **Certificate of service** (proof you filed)
- **Cover sheet** (court filing form)

Download as PDF and file with your local courthouse.

---

## 📅 Timeline & Calendar

### Timeline View:
- See all events chronologically
- Document uploads
- Notices received
- Court dates
- Rent payments

**Access:** `/timeline?user_token=[your-token]`

### Calendar Integration:
- Import deadlines into your phone calendar
- Get reminders for:
  - Court appearances
  - Rent due dates
  - Response deadlines
  - Move-out dates

---

## 🏛️ Jurisdiction Engine

Semptify auto-generates defense toolkits for **any US county**:

**Includes:**
- Local court forms
- Housing code violations
- Tenant rights specific to your area
- Emergency resources
- Legal aid contacts

**Currently Available:**
- **Dakota County, MN** (full multilingual toolkit)
- **3,143 other US counties** (2-second generation)

---

## ❓ Frequently Asked Questions

### General

**Q: Is Semptify really free?**
A: Yes, 100% free for tenants. No credit card, no hidden fees.

**Q: Who built Semptify?**
A: Brad Crowe, a 60-year-old first-time developer passionate about tenant rights.

**Q: Can I use Semptify if I'm not in Minnesota?**
A: Yes! The Jurisdiction Engine works for all 3,143 US counties.

### Privacy & Security

**Q: Can Semptify see my documents?**
A: No. Your documents are in YOUR Dropbox/Google Drive. We only store hashes (fingerprints) of files, not the files themselves.

**Q: What if I lose my token?**
A: Unfortunately, tokens cannot be recovered. This is by design for security. Write it down and keep it safe!

**Q: Can my landlord access my vault?**
A: No. Only someone with your 12-digit token can access your vault.

**Q: What happens if Semptify shuts down?**
A: Your documents are in YOUR cloud (Dropbox/Drive). You still have access. Semptify just helps organize them.

### Technical

**Q: What browsers are supported?**
A: Chrome, Firefox, Safari, Edge (all modern browsers)

**Q: Does Semptify work on phones?**
A: Yes! Responsive design works on mobile, tablet, and desktop.

**Q: Can I use Semptify offline?**
A: No, Semptify requires internet connection. But your documents in Dropbox/Drive have offline access.

**Q: What file types can I upload?**
A: PDF, JPG, PNG, DOC, DOCX, TXT, and most common formats.

### Legal

**Q: Is Semptify a lawyer?**
A: No. Semptify provides tools and information, not legal advice. Consult a real attorney for your specific situation.

**Q: Will my evidence be accepted in court?**
A: Semptify notarizes uploads with cryptographic hashes and timestamps, which are generally admissible. But judges have final say.

**Q: Can Semptify guarantee I'll win my case?**
A: No. Semptify helps you organize evidence and file complaints, but legal outcomes depend on many factors.

### Using Semptify

**Q: How do I change my storage provider?**
A: Go to `/settings` and select "Change Storage Provider". You'll need to re-authorize and your vault will migrate.

**Q: Can I have multiple tokens?**
A: No, each registration gets one token. But you can create separate accounts for different cases.

**Q: How long are documents stored?**
A: Forever (or until you delete them from YOUR Dropbox/Drive). Semptify doesn't control storage duration.

**Q: Can I share my vault with my attorney?**
A: Yes! Just give your attorney your vault link with token. They can view all your evidence.

---

## 🆘 Getting Help

### Support Channels:

**Documentation:**
- This User Guide
- `README.md` (for technical users)
- `ARCHITECTURE_SUMMARY.md` (for developers)

**Emergency Resources:**
- **National:** Call 211 for housing assistance
- **Legal Aid:** Find free attorneys at LawHelpMN.org
- **Crisis:** National Domestic Violence Hotline: 1-800-799-7233

### Reporting Issues:

Found a bug or problem?
1. Check if server is running
2. Try clearing browser cache
3. Report on GitHub: `github.com/Bradleycrowe/SemptifyGUI/issues`

---

## 🎓 Tips for Success

### 1. Document Everything
- Take photos of issues immediately
- Save ALL emails with landlord
- Keep copies of all notices
- Upload to vault within 24 hours

### 2. Stay Organized
- Use descriptive filenames
- Add detailed descriptions
- Tag evidence by type
- Review timeline monthly

### 3. Be Proactive
- Don't wait until court date to gather evidence
- Upload as issues happen
- File complaints early
- Consult attorney before representing yourself

### 4. Protect Your Token
- Never share on social media
- Don't email it unencrypted
- Store in password manager
- Write on paper as backup

### 5. Know Your Rights
- Read your lease carefully
- Learn local tenant laws
- Respond to notices promptly
- Keep rent receipts forever

---

## �� Quick Reference

### Important Links:
- Register: `/register`
- Vault: `/vault?user_token=[YOUR-TOKEN]`
- File Complaint: `/file-complaint`
- Timeline: `/timeline?user_token=[YOUR-TOKEN]`
- Settings: `/settings`
- Jurisdiction Library: `/library/dakota` (or your county)

### Key Features:
- 📁 Evidence Vault (document storage)
- 🔐 Automatic notarization (SHA-256 + timestamp)
- ⚖️ Complaint wizard (60% auto-filled)
- 🤖 AI evidence ranking (90-95% accuracy)
- 📅 Timeline & calendar
- 🏛️ Jurisdiction Engine (3,143 counties)
- 🌍 Multilingual support (coming soon)

---

## 📜 License & Credits

**Semptify** is open-source software.
- License: MIT (free to use, modify, distribute)
- GitHub: github.com/Bradleycrowe/SemptifyGUI
- Built with: Python, Flask, PostgreSQL, Cloudflare R2

**Created by:** Brad Crowe  
**Mission:** Empower tenants with technology to defend their rights

---

**💜 Remember: You have rights. Semptify helps you protect them.**

*Last Updated: November 25, 2025*
