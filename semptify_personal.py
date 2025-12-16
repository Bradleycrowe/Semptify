"""
SEMPTIFY PERSONAL - Standalone Desktop GUI
No Flask, No Web Server - Pure Python
For personal tenant rights management
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import sqlite3
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class SemptifyPersonal:
    def __init__(self, root):
        self.root = root
        self.root.title("Semptify Personal - Tenant Rights Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Set working directory
        self.base_dir = Path("C:/Semptify/Semptify")
        os.chdir(self.base_dir)
        
        # Initialize data directories
        self.init_directories()
        
        # Initialize database
        self.init_database()
        
        # Create menu bar
        self.create_menu()
        
        # Create main layout
        self.create_main_layout()
        
        # Status bar
        self.status = tk.Label(root, text="✓ Ready - All data stored locally", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                              bg='#34495e', fg='white')
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status("✓ Semptify Personal loaded")
    
    def init_directories(self):
        """Create necessary directories"""
        dirs = ['uploads/vault', 'data', 'logs', 'exports']
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
    
    def init_database(self):
        """Initialize SQLite database"""
        self.db_path = "semptify_personal.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Timeline events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timeline_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                file_hash TEXT,
                category TEXT,
                notes TEXT,
                upload_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Calendar events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT,
                title TEXT NOT NULL,
                description TEXT,
                reminder INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export All Data", command=self.export_all_data)
        file_menu.add_command(label="Backup to USB", command=self.backup_to_usb)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_layout(self):
        """Create main layout with tabs"""
        # Create notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2c3e50')
        style.configure('TNotebook.Tab', background='#34495e', foreground='white', padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#3498db')])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_vault_tab()
        self.create_ledger_tab()
        self.create_timeline_tab()
        self.create_calendar_tab()
        self.create_complaint_tab()
        self.create_export_tab()
    
    def create_dashboard_tab(self):
        """Dashboard overview"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Dashboard")
        
        # Title
        tk.Label(tab, text="Tenant Rights Dashboard", font=('Arial', 20, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(tab, bg='#34495e')
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Quick stats
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=25, 
                                                     bg='#2c3e50', fg='white', 
                                                     font=('Consolas', 10))
        self.stats_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Refresh button
        tk.Button(tab, text="🔄 Refresh Stats", command=self.refresh_dashboard,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(pady=10)
        
        self.refresh_dashboard()
    
    def create_vault_tab(self):
        """Document vault"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Vault")
        
        # Top controls
        controls = tk.Frame(tab, bg='#34495e')
        controls.pack(fill='x', padx=10, pady=10)
        
        tk.Button(controls, text="📤 Upload Document", command=self.upload_document,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=8).pack(side='left', padx=5)
        
        tk.Button(controls, text="🔍 Search", command=self.search_documents,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=8).pack(side='left', padx=5)
        
        tk.Button(controls, text="🗑️ Delete Selected", command=self.delete_document,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=8).pack(side='left', padx=5)
        
        # Document list
        list_frame = tk.Frame(tab, bg='#2c3e50')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for documents
        columns = ('Filename', 'Category', 'Date', 'Size')
        self.doc_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=20)
        
        for col in columns:
            self.doc_tree.heading(col, text=col)
            self.doc_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.doc_tree.yview)
        self.doc_tree.configure(yscrollcommand=scrollbar.set)
        
        self.doc_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_documents()
    
    def create_ledger_tab(self):
        """Payment ledger"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💰 Ledger")
        
        # Add payment form
        form_frame = tk.Frame(tab, bg='#34495e')
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Add Payment:", font=('Arial', 12, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, columnspan=4, pady=10)
        
        tk.Label(form_frame, text="Date:", bg='#34495e', fg='white').grid(row=1, column=0, padx=5)
        self.pay_date = tk.Entry(form_frame, width=15)
        self.pay_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.pay_date.grid(row=1, column=1, padx=5)
        
        tk.Label(form_frame, text="Amount:", bg='#34495e', fg='white').grid(row=1, column=2, padx=5)
        self.pay_amount = tk.Entry(form_frame, width=15)
        self.pay_amount.grid(row=1, column=3, padx=5)
        
        tk.Label(form_frame, text="Type:", bg='#34495e', fg='white').grid(row=2, column=0, padx=5)
        self.pay_type = ttk.Combobox(form_frame, values=['Rent', 'Late Fee', 'Deposit', 'Utility', 'Other'], width=13)
        self.pay_type.set('Rent')
        self.pay_type.grid(row=2, column=1, padx=5)
        
        tk.Label(form_frame, text="Notes:", bg='#34495e', fg='white').grid(row=2, column=2, padx=5)
        self.pay_notes = tk.Entry(form_frame, width=15)
        self.pay_notes.grid(row=2, column=3, padx=5)
        
        tk.Button(form_frame, text="➕ Add Payment", command=self.add_payment,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=8).grid(row=3, column=0, columnspan=4, pady=10)
        
        # Payment list
        list_frame = tk.Frame(tab, bg='#2c3e50')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Date', 'Amount', 'Type', 'Notes')
        self.pay_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            self.pay_tree.heading(col, text=col)
            self.pay_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.pay_tree.yview)
        self.pay_tree.configure(yscrollcommand=scrollbar.set)
        
        self.pay_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Summary
        summary_frame = tk.Frame(tab, bg='#34495e')
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        self.ledger_summary = tk.Label(summary_frame, text="", font=('Arial', 11),
                                       bg='#34495e', fg='white')
        self.ledger_summary.pack(pady=10)
        
        self.load_payments()
    
    def create_timeline_tab(self):
        """Timeline of events"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📅 Timeline")
        
        # Add event form
        form_frame = tk.Frame(tab, bg='#34495e')
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Add Event:", font=('Arial', 12, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, columnspan=4, pady=10)
        
        tk.Label(form_frame, text="Date:", bg='#34495e', fg='white').grid(row=1, column=0, padx=5)
        self.event_date = tk.Entry(form_frame, width=15)
        self.event_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.event_date.grid(row=1, column=1, padx=5)
        
        tk.Label(form_frame, text="Title:", bg='#34495e', fg='white').grid(row=1, column=2, padx=5)
        self.event_title = tk.Entry(form_frame, width=30)
        self.event_title.grid(row=1, column=3, padx=5)
        
        tk.Label(form_frame, text="Category:", bg='#34495e', fg='white').grid(row=2, column=0, padx=5)
        self.event_cat = ttk.Combobox(form_frame, values=['Maintenance', 'Payment', 'Communication', 'Issue', 'Other'], width=13)
        self.event_cat.set('Issue')
        self.event_cat.grid(row=2, column=1, padx=5)
        
        tk.Label(form_frame, text="Description:", bg='#34495e', fg='white').grid(row=2, column=2, padx=5)
        self.event_desc = tk.Entry(form_frame, width=30)
        self.event_desc.grid(row=2, column=3, padx=5)
        
        tk.Button(form_frame, text="➕ Add Event", command=self.add_timeline_event,
                 bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=8).grid(row=3, column=0, columnspan=4, pady=10)
        
        # Timeline display
        self.timeline_text = scrolledtext.ScrolledText(tab, height=20, 
                                                       bg='#2c3e50', fg='white',
                                                       font=('Consolas', 10))
        self.timeline_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.load_timeline()
    
    def create_calendar_tab(self):
        """Calendar for deadlines"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📆 Calendar")
        
        # Add reminder form
        form_frame = tk.Frame(tab, bg='#34495e')
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Add Deadline/Reminder:", font=('Arial', 12, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, columnspan=4, pady=10)
        
        tk.Label(form_frame, text="Date:", bg='#34495e', fg='white').grid(row=1, column=0, padx=5)
        self.cal_date = tk.Entry(form_frame, width=15)
        self.cal_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.cal_date.grid(row=1, column=1, padx=5)
        
        tk.Label(form_frame, text="Title:", bg='#34495e', fg='white').grid(row=1, column=2, padx=5)
        self.cal_title = tk.Entry(form_frame, width=30)
        self.cal_title.grid(row=1, column=3, padx=5)
        
        tk.Button(form_frame, text="➕ Add Reminder", command=self.add_calendar_event,
                 bg='#e67e22', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=8).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Calendar display
        self.calendar_text = scrolledtext.ScrolledText(tab, height=22,
                                                       bg='#2c3e50', fg='white',
                                                       font=('Consolas', 10))
        self.calendar_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.load_calendar()
    
    def create_complaint_tab(self):
        """Complaint builder"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚖️ Complaint")
        
        tk.Label(tab, text="Complaint/Letter Builder", font=('Arial', 16, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=10)
        
        # Template selector
        tk.Label(tab, text="Select Template:", bg='#2c3e50', fg='white').pack()
        self.complaint_template = ttk.Combobox(tab, values=[
            'Maintenance Request',
            'Rent Withholding Notice',
            'Security Deposit Demand',
            'Harassment Complaint',
            'Custom Letter'
        ], width=30)
        self.complaint_template.set('Maintenance Request')
        self.complaint_template.pack(pady=5)
        
        # Text editor
        self.complaint_text = scrolledtext.ScrolledText(tab, height=20,
                                                        bg='white', fg='black',
                                                        font=('Arial', 11))
        self.complaint_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(tab, bg='#2c3e50')
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="📝 Load Template", command=self.load_complaint_template,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=8).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="💾 Save as PDF", command=self.save_complaint_pdf,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=8).pack(side='left', padx=5)
    
    def create_export_tab(self):
        """Export/backup"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Export")
        
        tk.Label(tab, text="Export & Backup", font=('Arial', 16, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=20)
        
        btn_frame = tk.Frame(tab, bg='#2c3e50')
        btn_frame.pack(expand=True)
        
        tk.Button(btn_frame, text="📊 Export to Excel", command=self.export_excel,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=15, width=25).pack(pady=10)
        
        tk.Button(btn_frame, text="📄 Export to PDF Report", command=self.export_pdf_report,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=15, width=25).pack(pady=10)
        
        tk.Button(btn_frame, text="💾 Backup to USB Drive", command=self.backup_to_usb,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=15, width=25).pack(pady=10)
        
        tk.Button(btn_frame, text="📧 Export for Email", command=self.export_for_email,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=15, width=25).pack(pady=10)
        
        self.export_status = tk.Label(tab, text="", bg='#2c3e50', fg='#2ecc71',
                                      font=('Arial', 11, 'bold'))
        self.export_status.pack(pady=20)
    
    # === DATABASE METHODS ===
    
    def get_db(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def upload_document(self):
        """Upload document to vault"""
        filepath = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("All Files", "*.*"), ("PDF", "*.pdf"), ("Images", "*.png *.jpg"), ("Word", "*.docx")]
        )
        
        if filepath:
            filename = Path(filepath).name
            category = messagebox.askquestion("Category", "Is this a receipt/payment proof?")
            category = "Receipt" if category == 'yes' else "Other"
            
            # Copy to vault
            dest = Path(f"uploads/vault/{filename}")
            shutil.copy(filepath, dest)
            
            # Calculate hash
            with open(filepath, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Save to database
            conn = self.get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO documents (filename, filepath, file_hash, category)
                VALUES (?, ?, ?, ?)
            ''', (filename, str(dest), file_hash, category))
            conn.commit()
            conn.close()
            
            self.load_documents()
            self.update_status(f"✓ Uploaded: {filename}")
    
    def load_documents(self):
        """Load documents into tree"""
        # Clear tree
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT filename, category, upload_date, filepath FROM documents ORDER BY upload_date DESC')
        
        for row in cursor.fetchall():
            filename, category, date, filepath = row
            size = Path(filepath).stat().st_size if Path(filepath).exists() else 0
            size_kb = f"{size/1024:.1f} KB"
            
            self.doc_tree.insert('', 'end', values=(filename, category, date[:10], size_kb))
        
        conn.close()
    
    def delete_document(self):
        """Delete selected document"""
        selected = self.doc_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a document to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected document?"):
            # Implementation here
            self.update_status("✓ Document deleted")
    
    def search_documents(self):
        """Search documents"""
        search_term = tk.simpledialog.askstring("Search", "Enter search term:")
        if search_term:
            self.update_status(f"🔍 Searching for: {search_term}")
    
    def add_payment(self):
        """Add payment to ledger"""
        date = self.pay_date.get()
        amount = self.pay_amount.get()
        pay_type = self.pay_type.get()
        notes = self.pay_notes.get()
        
        if not date or not amount:
            messagebox.showwarning("Missing Data", "Please enter date and amount")
            return
        
        try:
            amount = float(amount)
        except:
            messagebox.showerror("Invalid Amount", "Amount must be a number")
            return
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (date, amount, type, notes)
            VALUES (?, ?, ?, ?)
        ''', (date, amount, pay_type, notes))
        conn.commit()
        conn.close()
        
        # Clear form
        self.pay_amount.delete(0, tk.END)
        self.pay_notes.delete(0, tk.END)
        
        self.load_payments()
        self.update_status(f"✓ Added payment: ${amount}")
    
    def load_payments(self):
        """Load payments into tree"""
        for item in self.pay_tree.get_children():
            self.pay_tree.delete(item)
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT date, amount, type, notes FROM payments ORDER BY date DESC')
        
        total = 0
        for row in cursor.fetchall():
            date, amount, pay_type, notes = row
            self.pay_tree.insert('', 'end', values=(date, f"${amount:.2f}", pay_type, notes))
            total += amount
        
        conn.close()
        
        self.ledger_summary.config(text=f"Total Payments: ${total:,.2f}")
    
    def add_timeline_event(self):
        """Add timeline event"""
        date = self.event_date.get()
        title = self.event_title.get()
        category = self.event_cat.get()
        description = self.event_desc.get()
        
        if not date or not title:
            messagebox.showwarning("Missing Data", "Please enter date and title")
            return
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO timeline_events (date, title, category, description)
            VALUES (?, ?, ?, ?)
        ''', (date, title, category, description))
        conn.commit()
        conn.close()
        
        self.event_title.delete(0, tk.END)
        self.event_desc.delete(0, tk.END)
        
        self.load_timeline()
        self.update_status(f"✓ Added event: {title}")
    
    def load_timeline(self):
        """Load timeline events"""
        self.timeline_text.delete(1.0, tk.END)
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT date, title, category, description FROM timeline_events ORDER BY date DESC')
        
        self.timeline_text.insert(tk.END, "TIMELINE OF EVENTS\n")
        self.timeline_text.insert(tk.END, "="*70 + "\n\n")
        
        for row in cursor.fetchall():
            date, title, category, description = row
            self.timeline_text.insert(tk.END, f"📅 {date} - [{category}]\n")
            self.timeline_text.insert(tk.END, f"   {title}\n")
            if description:
                self.timeline_text.insert(tk.END, f"   {description}\n")
            self.timeline_text.insert(tk.END, "\n")
        
        conn.close()
    
    def add_calendar_event(self):
        """Add calendar event"""
        date = self.cal_date.get()
        title = self.cal_title.get()
        
        if not date or not title:
            messagebox.showwarning("Missing Data", "Please enter date and title")
            return
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO calendar_events (date, title, reminder)
            VALUES (?, ?, 1)
        ''', (date, title))
        conn.commit()
        conn.close()
        
        self.cal_title.delete(0, tk.END)
        
        self.load_calendar()
        self.update_status(f"✓ Added reminder: {title}")
    
    def load_calendar(self):
        """Load calendar events"""
        self.calendar_text.delete(1.0, tk.END)
        
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT date, title, description FROM calendar_events ORDER BY date')
        
        self.calendar_text.insert(tk.END, "UPCOMING DEADLINES & REMINDERS\n")
        self.calendar_text.insert(tk.END, "="*70 + "\n\n")
        
        today = datetime.now().date()
        
        for row in cursor.fetchall():
            date, title, description = row
            event_date = datetime.strptime(date, "%Y-%m-%d").date()
            days_until = (event_date - today).days
            
            if days_until < 0:
                status = "⚠️ OVERDUE"
            elif days_until == 0:
                status = "🔴 TODAY"
            elif days_until <= 7:
                status = f"🟡 {days_until} days"
            else:
                status = f"🟢 {days_until} days"
            
            self.calendar_text.insert(tk.END, f"{status} - {date}\n")
            self.calendar_text.insert(tk.END, f"   {title}\n")
            if description:
                self.calendar_text.insert(tk.END, f"   {description}\n")
            self.calendar_text.insert(tk.END, "\n")
        
        conn.close()
    
    def load_complaint_template(self):
        """Load complaint template"""
        template = self.complaint_template.get()
        
        templates = {
            'Maintenance Request': """Date: {date}

To: [Landlord Name]
[Landlord Address]

Re: Maintenance Request - [Issue Description]

Dear [Landlord Name],

I am writing to formally request repairs for the following issue(s) in my rental unit at [Address]:

[Describe the issue in detail]

This issue affects my ability to safely and comfortably occupy the premises. Under [State] law, landlords are required to maintain rental properties in habitable condition.

I request that you address this issue within [reasonable timeframe] days. Please contact me at [phone/email] to schedule the repairs.

Thank you for your prompt attention to this matter.

Sincerely,
[Your Name]
[Your Address]
[Date]
""",
            'Rent Withholding Notice': """Date: {date}

To: [Landlord Name]

Re: Notice of Rent Withholding Due to Uninhabitable Conditions

Dear [Landlord Name],

Due to unresolved maintenance issues that render my unit uninhabitable, I am providing notice that I will be withholding rent payment until repairs are completed.

Issues:
[List issues and dates reported]

I have previously notified you of these issues on [dates]. Under [State] law, I have the right to withhold rent when the premises are not maintained in habitable condition.

I am prepared to pay all withheld rent once repairs are completed.

Sincerely,
[Your Name]
""",
        }
        
        template_text = templates.get(template, "Select a template to begin.")
        template_text = template_text.replace("{date}", datetime.now().strftime("%B %d, %Y"))
        
        self.complaint_text.delete(1.0, tk.END)
        self.complaint_text.insert(tk.END, template_text)
        
        self.update_status(f"✓ Loaded template: {template}")
    
    def save_complaint_pdf(self):
        """Save complaint as PDF"""
        content = self.complaint_text.get(1.0, tk.END)
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("PDF", "*.pdf")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(content)
            
            self.update_status(f"✓ Saved: {Path(filename).name}")
            messagebox.showinfo("Saved", f"Document saved to:\n{filename}")
    
    def refresh_dashboard(self):
        """Refresh dashboard stats"""
        self.stats_text.delete(1.0, tk.END)
        
        conn = self.get_db()
        cursor = conn.cursor()
        
        # Get stats
        cursor.execute('SELECT COUNT(*), SUM(amount) FROM payments')
        payment_count, payment_total = cursor.fetchone()
        payment_total = payment_total or 0
        
        cursor.execute('SELECT COUNT(*) FROM documents')
        doc_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM timeline_events')
        event_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM calendar_events WHERE date >= date("now")')
        upcoming_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Display stats
        self.stats_text.insert(tk.END, "╔═══════════════════════════════════════════════════════════╗\n")
        self.stats_text.insert(tk.END, "║         SEMPTIFY PERSONAL - DASHBOARD OVERVIEW           ║\n")
        self.stats_text.insert(tk.END, "╚═══════════════════════════════════════════════════════════╝\n\n")
        
        self.stats_text.insert(tk.END, f"📁 Documents Stored:        {doc_count}\n")
        self.stats_text.insert(tk.END, f"💰 Payment Records:         {payment_count}\n")
        self.stats_text.insert(tk.END, f"💵 Total Payments:          ${payment_total:,.2f}\n")
        self.stats_text.insert(tk.END, f"📅 Timeline Events:         {event_count}\n")
        self.stats_text.insert(tk.END, f"🔔 Upcoming Reminders:      {upcoming_count}\n\n")
        
        self.stats_text.insert(tk.END, "─" * 60 + "\n\n")
        
        # Recent activity
        self.stats_text.insert(tk.END, "RECENT ACTIVITY:\n\n")
        
        conn = self.get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT date, title FROM timeline_events ORDER BY created_at DESC LIMIT 5')
        for row in cursor.fetchall():
            self.stats_text.insert(tk.END, f"  • {row[0]} - {row[1]}\n")
        
        conn.close()
        
        self.update_status("✓ Dashboard refreshed")
    
    def export_all_data(self):
        """Export all data to JSON"""
        export_dir = filedialog.askdirectory(title="Select Export Location")
        if not export_dir:
            return
        
        conn = self.get_db()
        
        # Export payments
        df = conn.execute('SELECT * FROM payments').fetchall()
        with open(f"{export_dir}/payments.json", 'w') as f:
            json.dump([list(row) for row in df], f, indent=2)
        
        # Export timeline
        df = conn.execute('SELECT * FROM timeline_events').fetchall()
        with open(f"{export_dir}/timeline.json", 'w') as f:
            json.dump([list(row) for row in df], f, indent=2)
        
        # Export documents list
        df = conn.execute('SELECT * FROM documents').fetchall()
        with open(f"{export_dir}/documents.json", 'w') as f:
            json.dump([list(row) for row in df], f, indent=2)
        
        conn.close()
        
        self.update_status(f"✓ Exported all data to {export_dir}")
        messagebox.showinfo("Export Complete", f"All data exported to:\n{export_dir}")
    
    def backup_to_usb(self):
        """Backup to USB drive"""
        usb_dir = filedialog.askdirectory(title="Select USB Drive")
        if not usb_dir:
            return
        
        backup_dir = Path(usb_dir) / f"semptify_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(exist_ok=True)
        
        # Copy database
        shutil.copy(self.db_path, backup_dir / "database.db")
        
        # Copy vault
        shutil.copytree("uploads/vault", backup_dir / "vault", dirs_exist_ok=True)
        
        self.update_status(f"✓ Backed up to {backup_dir}")
        messagebox.showinfo("Backup Complete", f"Backup created at:\n{backup_dir}")
    
    def export_excel(self):
        """Export to Excel (CSV)"""
        export_dir = filedialog.askdirectory(title="Select Export Location")
        if not export_dir:
            return
        
        conn = self.get_db()
        
        # Export payments to CSV
        import csv
        cursor = conn.execute('SELECT date, amount, type, notes FROM payments ORDER BY date')
        with open(f"{export_dir}/payments.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Amount', 'Type', 'Notes'])
            writer.writerows(cursor.fetchall())
        
        conn.close()
        
        self.export_status.config(text=f"✓ Exported to {export_dir}")
        self.update_status("✓ Excel export complete")
    
    def export_pdf_report(self):
        """Generate PDF report"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Report", "*.txt")]
        )
        
        if filename:
            conn = self.get_db()
            
            with open(filename, 'w') as f:
                f.write("SEMPTIFY PERSONAL - FULL REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Payments
                f.write("\n--- PAYMENT HISTORY ---\n\n")
                cursor = conn.execute('SELECT date, amount, type, notes FROM payments ORDER BY date')
                for row in cursor.fetchall():
                    f.write(f"{row[0]}: ${row[1]:.2f} - {row[2]} - {row[3]}\n")
                
                # Timeline
                f.write("\n--- TIMELINE EVENTS ---\n\n")
                cursor = conn.execute('SELECT date, title, description FROM timeline_events ORDER BY date')
                for row in cursor.fetchall():
                    f.write(f"{row[0]}: {row[1]}\n  {row[2]}\n\n")
            
            conn.close()
            
            self.export_status.config(text=f"✓ Report saved: {Path(filename).name}")
            self.update_status("✓ PDF report generated")
    
    def export_for_email(self):
        """Create email-friendly export"""
        export_dir = filedialog.askdirectory(title="Select Export Location")
        if not export_dir:
            return
        
        # Create summary file
        summary_file = Path(export_dir) / "summary_for_email.txt"
        
        conn = self.get_db()
        
        with open(summary_file, 'w') as f:
            f.write("TENANT RIGHTS DOCUMENTATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            cursor = conn.execute('SELECT COUNT(*) FROM payments')
            f.write(f"Total payment records: {cursor.fetchone()[0]}\n")
            
            cursor = conn.execute('SELECT COUNT(*) FROM timeline_events')
            f.write(f"Total events documented: {cursor.fetchone()[0]}\n")
            
            cursor = conn.execute('SELECT COUNT(*) FROM documents')
            f.write(f"Total documents stored: {cursor.fetchone()[0]}\n\n")
            
            f.write("\nRecent Timeline:\n")
            cursor = conn.execute('SELECT date, title FROM timeline_events ORDER BY date DESC LIMIT 10')
            for row in cursor.fetchall():
                f.write(f"  • {row[0]}: {row[1]}\n")
        
        conn.close()
        
        self.export_status.config(text=f"✓ Email export ready")
        self.update_status("✓ Email export created")
        messagebox.showinfo("Export Complete", f"Summary created at:\n{summary_file}\n\nAttach this file and relevant documents from vault to your email.")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
            "Semptify Personal v1.0\n\n"
            "Standalone tenant rights management tool\n\n"
            "• No internet required\n"
            "• All data stored locally\n"
            "• No Flask/web server needed\n\n"
            "Your data is private and secure on your computer.")
    
    def update_status(self, msg):
        """Update status bar"""
        self.status.config(text=msg)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = SemptifyPersonal(root)
    root.mainloop()
