"""
SEMPTIFY TOOLKIT - Complete Standalone Suite
All tools work independently, no Flask required
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import os
import sys
import sqlite3
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import webbrowser
from typing import Optional

# ============================================================================
# UNIVERSAL LAUNCHER - Main Menu
# ============================================================================

class SemptifyToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Semptify Toolkit - Choose Your Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Header
        header = tk.Label(root, text="🛡️ SEMPTIFY TOOLKIT", 
                         font=('Arial', 24, 'bold'),
                         bg='#1a1a2e', fg='#00d4ff')
        header.pack(pady=30)
        
        subtitle = tk.Label(root, text="Tenant Rights Protection Tools - No Internet Required", 
                           font=('Arial', 12),
                           bg='#1a1a2e', fg='#aaaaaa')
        subtitle.pack(pady=5)
        
        # Tools grid
        tools_frame = tk.Frame(root, bg='#1a1a2e')
        tools_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
        tools = [
            ("📁 Document Vault", "Secure document storage with SHA-256 hashing", self.launch_vault),
            ("💰 Payment Ledger", "Track rent payments and late fees", self.launch_ledger),
            ("📅 Timeline Tracker", "Document all tenant-landlord interactions", self.launch_timeline),
            ("⚖️ Complaint Builder", "Generate legal letters and notices", self.launch_complaint),
            ("📆 Calendar & Reminders", "Track deadlines and court dates", self.launch_calendar),
            ("🔍 Evidence Logger", "Organize photos and proof", self.launch_evidence),
            ("📊 Full Dashboard", "All-in-one management interface", self.launch_dashboard),
            ("🔧 Database Inspector", "View and manage your data", self.launch_db_inspector),
            ("📦 Backup Manager", "Export and backup all data", self.launch_backup),
        ]
        
        row = 0
        col = 0
        for name, desc, command in tools:
            self.create_tool_button(tools_frame, name, desc, command, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Footer
        footer = tk.Label(root, text="All data stored locally • Privacy-first • No tracking", 
                         font=('Arial', 9),
                         bg='#1a1a2e', fg='#666666')
        footer.pack(side='bottom', pady=10)
    
    def create_tool_button(self, parent, name, desc, command, row, col):
        frame = tk.Frame(parent, bg='#16213e', relief='raised', bd=2)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        btn = tk.Button(frame, text=name, command=command,
                       bg='#0f3460', fg='white', font=('Arial', 12, 'bold'),
                       padx=15, pady=15, relief='flat', cursor='hand2')
        btn.pack(fill='both', expand=True)
        
        lbl = tk.Label(frame, text=desc, wraplength=200,
                      bg='#16213e', fg='#aaaaaa', font=('Arial', 8))
        lbl.pack(pady=5)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg='#00d4ff', fg='#1a1a2e')
        def on_leave(e):
            btn.config(bg='#0f3460', fg='white')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Make columns equal width
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=1)
    
    def launch_vault(self):
        DocumentVault()
    
    def launch_ledger(self):
        PaymentLedger()
    
    def launch_timeline(self):
        TimelineTracker()
    
    def launch_complaint(self):
        ComplaintBuilder()
    
    def launch_calendar(self):
        CalendarReminders()
    
    def launch_evidence(self):
        EvidenceLogger()
    
    def launch_dashboard(self):
        FullDashboard()
    
    def launch_db_inspector(self):
        DatabaseInspector()
    
    def launch_backup(self):
        BackupManager()

# ============================================================================
# TOOL 1: DOCUMENT VAULT
# ============================================================================

class DocumentVault:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Document Vault")
        self.window.geometry("900x600")
        self.window.configure(bg='#2c3e50')
        
        self.db_path = "semptify_toolkit.db"
        self.init_db()
        
        # Title
        tk.Label(self.window, text="📁 DOCUMENT VAULT", 
                font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Controls
        controls = tk.Frame(self.window, bg='#34495e')
        controls.pack(fill='x', padx=10, pady=5)
        
        tk.Button(controls, text="�� Upload", command=self.upload,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side='left', padx=3)
        
        tk.Button(controls, text="👁️ Open", command=self.open_doc,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side='left', padx=3)
        
        tk.Button(controls, text="🗑️ Delete", command=self.delete,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side='left', padx=3)
        
        tk.Button(controls, text="✅ Verify Hash", command=self.verify_hash,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side='left', padx=3)
        
        # Document list
        columns = ('File', 'Category', 'Date', 'Size', 'Hash')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')
        
        # Status
        self.status = tk.Label(self.window, text="Ready", 
                              bg='#34495e', fg='white', anchor='w')
        self.status.pack(side='bottom', fill='x')
        
        self.load_documents()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault_documents (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                filepath TEXT,
                file_hash TEXT,
                category TEXT,
                size INTEGER,
                upload_date TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def upload(self):
        filepath = filedialog.askopenfilename(title="Select Document")
        if not filepath:
            return
        
        # Calculate hash
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Copy to vault
        Path("uploads/vault").mkdir(parents=True, exist_ok=True)
        filename = Path(filepath).name
        dest = Path(f"uploads/vault/{filename}")
        
        counter = 1
        while dest.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            dest = Path(f"uploads/vault/{stem}_{counter}{suffix}")
            counter += 1
        
        shutil.copy(filepath, dest)
        
        # Get category
        category = simpledialog.askstring("Category", "Document category (e.g., Receipt, Notice, Photo):", 
                                         initialvalue="Document")
        
        # Save to DB
        size = Path(filepath).stat().st_size
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vault_documents (filename, filepath, file_hash, category, size, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (dest.name, str(dest), file_hash, category, size, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.load_documents()
        self.status.config(text=f"✓ Uploaded: {dest.name} | Hash: {file_hash[:16]}...")
    
    def load_documents(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT filename, category, upload_date, size, file_hash FROM vault_documents ORDER BY upload_date DESC')
        
        for row in cursor.fetchall():
            filename, cat, date, size, hash_val = row
            size_kb = f"{size/1024:.1f}KB"
            hash_short = hash_val[:16] + "..."
            self.tree.insert('', 'end', values=(filename, cat, date[:10], size_kb, hash_short))
        
        conn.close()
    
    def open_doc(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        filename = self.tree.item(selected[0])['values'][0]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT filepath FROM vault_documents WHERE filename = ?', (filename,))
        result = cursor.fetchone()
        conn.close()
        
        if result and Path(result[0]).exists():
            os.startfile(result[0])
            self.status.config(text=f"✓ Opened: {filename}")
    
    def delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        if messagebox.askyesno("Confirm", "Delete selected document?"):
            filename = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT filepath FROM vault_documents WHERE filename = ?', (filename,))
            result = cursor.fetchone()
            
            if result:
                try:
                    Path(result[0]).unlink()
                except:
                    pass
                cursor.execute('DELETE FROM vault_documents WHERE filename = ?', (filename,))
                conn.commit()
            
            conn.close()
            self.load_documents()
            self.status.config(text=f"✓ Deleted: {filename}")
    
    def verify_hash(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        filename = self.tree.item(selected[0])['values'][0]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT filepath, file_hash FROM vault_documents WHERE filename = ?', (filename,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return
        
        filepath, stored_hash = result
        
        if not Path(filepath).exists():
            messagebox.showerror("Error", "File not found!")
            return
        
        # Recalculate hash
        with open(filepath, 'rb') as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        
        if current_hash == stored_hash:
            messagebox.showinfo("Verified", f"✓ Document integrity verified!\n\nHash: {current_hash}")
            self.status.config(text=f"✓ Verified: {filename}")
        else:
            messagebox.showerror("Tampered", f"⚠️ DOCUMENT HAS BEEN MODIFIED!\n\nStored:  {stored_hash}\nCurrent: {current_hash}")
            self.status.config(text=f"⚠️ VERIFICATION FAILED: {filename}")

# ============================================================================
# TOOL 2: PAYMENT LEDGER
# ============================================================================

class PaymentLedger:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Payment Ledger")
        self.window.geometry("800x600")
        self.window.configure(bg='#2c3e50')
        
        self.db_path = "semptify_toolkit.db"
        self.init_db()
        
        tk.Label(self.window, text="💰 PAYMENT LEDGER", 
                font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Add payment form
        form = tk.Frame(self.window, bg='#34495e', relief='raised', bd=2)
        form.pack(fill='x', padx=10, pady=5)
        
        tk.Label(form, text="Add Payment:", font=('Arial', 11, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, columnspan=6, pady=5)
        
        tk.Label(form, text="Date:", bg='#34495e', fg='white').grid(row=1, column=0, padx=3)
        self.date_entry = tk.Entry(form, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=3)
        
        tk.Label(form, text="Amount:", bg='#34495e', fg='white').grid(row=1, column=2, padx=3)
        self.amount_entry = tk.Entry(form, width=12)
        self.amount_entry.grid(row=1, column=3, padx=3)
        
        tk.Label(form, text="Type:", bg='#34495e', fg='white').grid(row=2, column=0, padx=3)
        self.type_combo = ttk.Combobox(form, values=['Rent', 'Late Fee', 'Deposit', 'Utility', 'Other'], width=10)
        self.type_combo.set('Rent')
        self.type_combo.grid(row=2, column=1, padx=3)
        
        tk.Label(form, text="Notes:", bg='#34495e', fg='white').grid(row=2, column=2, padx=3)
        self.notes_entry = tk.Entry(form, width=25)
        self.notes_entry.grid(row=2, column=3, columnspan=2, padx=3)
        
        tk.Button(form, text="➕ Add", command=self.add_payment,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).grid(row=3, column=0, columnspan=6, pady=8)
        
        # Payment list
        columns = ('Date', 'Amount', 'Type', 'Notes')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')
        
        # Summary
        self.summary = tk.Label(self.window, text="", font=('Arial', 12, 'bold'),
                               bg='#34495e', fg='#2ecc71')
        self.summary.pack(side='bottom', fill='x', pady=5)
        
        self.load_payments()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledger_payments (
                id INTEGER PRIMARY KEY,
                date TEXT,
                amount REAL,
                type TEXT,
                notes TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_payment(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        pay_type = self.type_combo.get()
        notes = self.notes_entry.get()
        
        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ledger_payments (date, amount, type, notes, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, pay_type, notes, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        
        self.load_payments()
    
    def load_payments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT date, amount, type, notes FROM ledger_payments ORDER BY date DESC')
        
        total = 0
        for row in cursor.fetchall():
            date, amount, pay_type, notes = row
            self.tree.insert('', 'end', values=(date, f"${amount:.2f}", pay_type, notes))
            total += amount
        
        conn.close()
        
        self.summary.config(text=f"  Total Payments: ${total:,.2f}  ")

# ============================================================================
# TOOL 3: TIMELINE TRACKER
# ============================================================================

class TimelineTracker:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Timeline Tracker")
        self.window.geometry("800x600")
        self.window.configure(bg='#2c3e50')
        
        self.db_path = "semptify_toolkit.db"
        self.init_db()
        
        tk.Label(self.window, text="📅 TIMELINE TRACKER", 
                font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Add event form
        form = tk.Frame(self.window, bg='#34495e', relief='raised', bd=2)
        form.pack(fill='x', padx=10, pady=5)
        
        tk.Label(form, text="Add Event:", font=('Arial', 11, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, columnspan=4, pady=5)
        
        tk.Label(form, text="Date:", bg='#34495e', fg='white').grid(row=1, column=0, padx=3)
        self.date_entry = tk.Entry(form, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=3)
        
        tk.Label(form, text="Title:", bg='#34495e', fg='white').grid(row=1, column=2, padx=3)
        self.title_entry = tk.Entry(form, width=30)
        self.title_entry.grid(row=1, column=3, padx=3)
        
        tk.Label(form, text="Category:", bg='#34495e', fg='white').grid(row=2, column=0, padx=3)
        self.cat_combo = ttk.Combobox(form, values=['Issue', 'Maintenance', 'Payment', 'Communication', 'Legal', 'Other'], width=10)
        self.cat_combo.set('Issue')
        self.cat_combo.grid(row=2, column=1, padx=3)
        
        tk.Label(form, text="Description:", bg='#34495e', fg='white').grid(row=2, column=2, padx=3)
        self.desc_entry = tk.Entry(form, width=30)
        self.desc_entry.grid(row=2, column=3, padx=3)
        
        tk.Button(form, text="➕ Add Event", command=self.add_event,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).grid(row=3, column=0, columnspan=4, pady=8)
        
        # Timeline display
        self.timeline_text = scrolledtext.ScrolledText(self.window, height=25,
                                                       bg='#1a1a1a', fg='#00ff00',
                                                       font=('Consolas', 10))
        self.timeline_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.load_timeline()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timeline_events (
                id INTEGER PRIMARY KEY,
                date TEXT,
                title TEXT,
                category TEXT,
                description TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_event(self):
        date = self.date_entry.get()
        title = self.title_entry.get()
        category = self.cat_combo.get()
        description = self.desc_entry.get()
        
        if not title:
            messagebox.showwarning("Missing", "Please enter a title")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO timeline_events (date, title, category, description, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, title, category, description, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        
        self.load_timeline()
    
    def load_timeline(self):
        self.timeline_text.delete(1.0, tk.END)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT date, title, category, description FROM timeline_events ORDER BY date DESC')
        
        self.timeline_text.insert(tk.END, "═" * 80 + "\n")
        self.timeline_text.insert(tk.END, "                    TENANT-LANDLORD INTERACTION TIMELINE\n")
        self.timeline_text.insert(tk.END, "═" * 80 + "\n\n")
        
        for row in cursor.fetchall():
            date, title, category, description = row
            self.timeline_text.insert(tk.END, f"📅 {date} - [{category}]\n")
            self.timeline_text.insert(tk.END, f"   ▶ {title}\n")
            if description:
                self.timeline_text.insert(tk.END, f"   {description}\n")
            self.timeline_text.insert(tk.END, "\n")
        
        conn.close()

# ============================================================================
# TOOL 4: COMPLAINT BUILDER
# ============================================================================

class ComplaintBuilder:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Complaint Builder")
        self.window.geometry("900x700")
        self.window.configure(bg='#2c3e50')
        
        tk.Label(self.window, text="⚖️ COMPLAINT & LETTER BUILDER", 
                font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Template selector
        controls = tk.Frame(self.window, bg='#34495e')
        controls.pack(fill='x', padx=10, pady=5)
        
        tk.Label(controls, text="Template:", bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.template_combo = ttk.Combobox(controls, values=[
            'Maintenance Request',
            'Rent Withholding Notice',
            'Security Deposit Demand',
            'Harassment Complaint',
            'Retaliation Notice',
            'Lease Violation Notice',
            'Repair and Deduct Notice',
            'Custom Letter'
        ], width=30)
        self.template_combo.set('Maintenance Request')
        self.template_combo.pack(side='left', padx=5)
        
        tk.Button(controls, text="📝 Load", command=self.load_template,
                 bg='#3498db', fg='white', font=('Arial', 9, 'bold'),
                 padx=10, pady=3).pack(side='left', padx=3)
        
        tk.Button(controls, text="💾 Save", command=self.save,
                 bg='#27ae60', fg='white', font=('Arial', 9, 'bold'),
                 padx=10, pady=3).pack(side='left', padx=3)
        
        tk.Button(controls, text="📧 Export", command=self.export,
                 bg='#e67e22', fg='white', font=('Arial', 9, 'bold'),
                 padx=10, pady=3).pack(side='left', padx=3)
        
        # Editor
        self.editor = scrolledtext.ScrolledText(self.window, height=30,
                                                bg='white', fg='black',
                                                font=('Arial', 11),
                                                wrap='word')
        self.editor.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Status
        self.status = tk.Label(self.window, text="Select a template to begin", 
                              bg='#34495e', fg='white', anchor='w')
        self.status.pack(side='bottom', fill='x')
    
    def load_template(self):
        template = self.template_combo.get()
        
        templates = {
            'Maintenance Request': f"""Date: {datetime.now().strftime("%B %d, %Y")}

To: [Landlord Name]
    [Landlord Address]

Re: Urgent Maintenance Request - [Property Address]

Dear [Landlord Name],

I am writing to formally request immediate repairs for the following issue(s) at my rental unit located at [Property Address]:

[DESCRIBE ISSUE IN DETAIL - Include when it started, how it affects habitability]

This issue severely impacts my ability to safely and comfortably occupy the premises. Under [State] Residential Landlord and Tenant Act, landlords are required to:
- Maintain the premises in habitable condition
- Make all necessary repairs to keep the dwelling fit for human habitation
- Comply with building and housing codes

I am requesting that you address this issue within [7-14] days as required by law. Please contact me at [Phone] or [Email] to schedule the repairs.

If repairs are not completed within this timeframe, I may be forced to exercise my legal remedies including:
- Rent withholding
- Repair and deduct
- Termination of lease
- Legal action

I trust this matter will be resolved promptly.

Sincerely,
[Your Name]
[Your Address]
[Phone Number]
[Email]

CC: [Local housing authority if applicable]
""",
            'Rent Withholding Notice': f"""Date: {datetime.now().strftime("%B %d, %Y")}

To: [Landlord Name]
    [Landlord Address]

Re: NOTICE OF RENT WITHHOLDING - Uninhabitable Conditions

Dear [Landlord Name],

This letter serves as formal notice that I am withholding rent payment for [Property Address] due to the following unresolved conditions that render the premises uninhabitable:

DOCUMENTED ISSUES:
1. [Issue #1] - First reported on [Date]
2. [Issue #2] - First reported on [Date]
3. [Issue #3] - First reported on [Date]

TIMELINE OF NOTIFICATIONS:
- [Date]: Initial verbal complaint
- [Date]: Written complaint submitted
- [Date]: Follow-up request
- [Date]: This formal notice

Under [State] law, tenants have the right to withhold rent when:
- The premises are not maintained in habitable condition
- Repairs affect health and safety
- Landlord has been properly notified and failed to act

I am depositing rent payments into an escrow account and will release funds once:
1. All repairs are completed to code
2. Premises pass inspection
3. Issues are fully resolved

I remain willing to work cooperatively to resolve these matters.

Sincerely,
[Your Name]

ATTACHMENTS:
- Photo documentation
- Previous correspondence
- Inspection reports (if any)
""",
            'Security Deposit Demand': f"""Date: {datetime.now().strftime("%B %d, %Y")}

To: [Landlord Name]
    [Landlord Address]

Re: DEMAND FOR RETURN OF SECURITY DEPOSIT

Dear [Landlord Name],

I vacated the rental property at [Property Address] on [Move-Out Date]. As of today, [X] days have passed and I have not received:
- My security deposit of $[Amount]
- An itemized statement of deductions

Under [State] law, landlords must:
- Return security deposits within [21-30] days of move-out
- Provide itemized list of any deductions
- Include receipts for repairs exceeding $[Amount]

MOVE-OUT CONDITION:
- Property was cleaned thoroughly
- All keys were returned on [Date]
- Move-out inspection was [completed/requested]
- No damage beyond normal wear and tear

This letter serves as formal demand for immediate return of my full security deposit of $[Amount].

If my deposit is not returned within [5-10] business days, I will file a claim in small claims court seeking:
- Full deposit amount: $[Amount]
- Statutory penalties: $[2-3x deposit]
- Court costs and attorney fees
- Interest as allowed by law

I expect this matter to be resolved immediately.

Sincerely,
[Your Name]
[Current Address]
[Phone]
[Email]
""",
        }
        
        text = templates.get(template, "Select a template from the dropdown menu.")
        
        self.editor.delete(1.0, tk.END)
        self.editor.insert(tk.END, text)
        
        self.status.config(text=f"✓ Loaded: {template}")
    
    def save(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("Word", "*.docx")]
        )
        
        if filename:
            content = self.editor.get(1.0, tk.END)
            with open(filename, 'w') as f:
                f.write(content)
            
            self.status.config(text=f"✓ Saved: {Path(filename).name}")
    
    def export(self):
        content = self.editor.get(1.0, tk.END)
        
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        filename = export_dir / f"complaint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write(content)
        
        messagebox.showinfo("Exported", f"Document saved to:\n{filename}\n\nReady for email attachment!")
        self.status.config(text=f"✓ Exported to: {filename}")

# ============================================================================
# TOOL 5: CALENDAR & REMINDERS
# ============================================================================

class CalendarReminders:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Calendar & Reminders")
        self.window.geometry("800x600")
        self.window.configure(bg='#2c3e50')
        
        self.db_path = "semptify_toolkit.db"
        self.init_db()
        
        tk.Label(self.window, text="📆 DEADLINES & REMINDERS", 
                font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Add reminder form
        form = tk.Frame(self.window, bg='#34495e', relief='raised', bd=2)
        form.pack(fill='x', padx=10, pady=5)
        
        tk.Label(form, text="Add Deadline:", font=('Arial', 11, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, columnspan=4, pady=5)
        
        tk.Label(form, text="Date:", bg='#34495e', fg='white').grid(row=1, column=0, padx=3)
        self.date_entry = tk.Entry(form, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=3)
        
        tk.Label(form, text="Title:", bg='#34495e', fg='white').grid(row=1, column=2, padx=3)
        self.title_entry = tk.Entry(form, width=30)
        self.title_entry.grid(row=1, column=3, padx=3)
        
        tk.Button(form, text="➕ Add", command=self.add_reminder,
                 bg='#e67e22', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).grid(row=2, column=0, columnspan=4, pady=8)
        
        # Calendar display
        self.calendar_text = scrolledtext.ScrolledText(self.window, height=25,
                                                       bg='#1a1a1a', fg='#ffaa00',
                                                       font=('Consolas', 10))
        self.calendar_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.load_calendar()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calendar_reminders (
                id INTEGER PRIMARY KEY,
                date TEXT,
                title TEXT,
                description TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_reminder(self):
        date = self.date_entry.get()
        title = self.title_entry.get()
        
        if not title:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO calendar_reminders (date, title, created_at)
            VALUES (?, ?, ?)
        ''', (date, title, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.title_entry.delete(0, tk.END)
        self.load_calendar()
    
    def load_calendar(self):
        self.calendar_text.delete(1.0, tk.END)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT date, title, description FROM calendar_reminders ORDER BY date')
        
        self.calendar_text.insert(tk.END, "═" * 80 + "\n")
        self.calendar_text.insert(tk.END, "                    UPCOMING DEADLINES & COURT DATES\n")
        self.calendar_text.insert(tk.END, "═" * 80 + "\n\n")
        
        today = datetime.now().date()
        
        for row in cursor.fetchall():
            date, title, description = row
            try:
                event_date = datetime.strptime(date, "%Y-%m-%d").date()
                days_until = (event_date - today).days
                
                if days_until < 0:
                    status = "⚠️ OVERDUE"
                    color = ""
                elif days_until == 0:
                    status = "🔴 TODAY"
                    color = ""
                elif days_until <= 3:
                    status = f"�� {days_until} days"
                    color = ""
                elif days_until <= 7:
                    status = f"🟡 {days_until} days"
                    color = ""
                else:
                    status = f"🟢 {days_until} days"
                    color = ""
                
                self.calendar_text.insert(tk.END, f"{status} - {date}\n")
                self.calendar_text.insert(tk.END, f"   ▶ {title}\n")
                if description:
                    self.calendar_text.insert(tk.END, f"   {description}\n")
                self.calendar_text.insert(tk.END, "\n")
            except:
                pass
        
        conn.close()

# ============================================================================
# TOOL 6: EVIDENCE LOGGER
# ============================================================================

class EvidenceLogger:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Evidence Logger")
        self.window.geometry("900x600")
        self.window.configure(bg='#2c3e50')
        
        tk.Label(self.window, text="🔍 EVIDENCE & PHOTO LOGGER", 
                font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Controls
        controls = tk.Frame(self.window, bg='#34495e')
        controls.pack(fill='x', padx=10, pady=5)
        
        tk.Button(controls, text="📷 Add Photo", command=self.add_photo,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side='left', padx=3)
        
        tk.Button(controls, text="👁️ View", command=self.view_evidence,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side='left', padx=3)
        
        # Evidence list
        columns = ('Date', 'Type', 'Description', 'File')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')
        
        # Status
        self.status = tk.Label(self.window, text="Add photos and documents as evidence", 
                              bg='#34495e', fg='white', anchor='w')
        self.status.pack(side='bottom', fill='x')
        
        self.evidence_log = []
        self.load_evidence()
    
    def add_photo(self):
        filepath = filedialog.askopenfilename(
            title="Select Evidence Photo",
            filetypes=[("Images", "*.jpg *.jpeg *.png"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        # Get description
        description = simpledialog.askstring("Description", "Describe this evidence:")
        if not description:
            description = "No description"
        
        # Copy to evidence folder
        Path("uploads/evidence").mkdir(parents=True, exist_ok=True)
        filename = Path(filepath).name
        dest = Path(f"uploads/evidence/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        shutil.copy(filepath, dest)
        
        # Log it
        evidence = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'type': 'Photo',
            'description': description,
            'file': str(dest)
        }
        self.evidence_log.append(evidence)
        
        # Save to JSON
        with open('evidence_log.json', 'w') as f:
            json.dump(self.evidence_log, f, indent=2)
        
        self.load_evidence()
        self.status.config(text=f"✓ Added: {filename}")
    
    def load_evidence(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if Path('evidence_log.json').exists():
            with open('evidence_log.json', 'r') as f:
                self.evidence_log = json.load(f)
        
        for ev in self.evidence_log:
            self.tree.insert('', 'end', values=(
                ev['date'],
                ev['type'],
                ev['description'],
                Path(ev['file']).name
            ))
    
    def view_evidence(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        idx = self.tree.index(selected[0])
        filepath = self.evidence_log[idx]['file']
        
        if Path(filepath).exists():
            os.startfile(filepath)

# ============================================================================
# ADDITIONAL TOOLS STUBS
# ============================================================================

class FullDashboard:
    def __init__(self):
        messagebox.showinfo("Dashboard", "Opening Full Dashboard...\n(This would launch the complete all-in-one interface)")

class DatabaseInspector:
    def __init__(self):
        messagebox.showinfo("DB Inspector", "Opening Database Inspector...\n(This would show all tables and data)")

class BackupManager:
    def __init__(self):
        messagebox.showinfo("Backup", "Opening Backup Manager...\n(This would handle exports and USB backups)")

# ============================================================================
# MAIN LAUNCHER
# ============================================================================

if __name__ == "__main__":
    # Set working directory
    os.chdir("C:/Semptify/Semptify")
    
    root = tk.Tk()
    app = SemptifyToolkit(root)
    root.mainloop()
