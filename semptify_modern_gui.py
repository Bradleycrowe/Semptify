"""
SEMPTIFY MODERN GUI - Web-Style Desktop Interface
Mimics the modern web GUI design with tabs and modern styling
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import sqlite3
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib
import webbrowser

class ModernSemptifyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Semptify - Tenant Rights Platform")
        self.root.geometry("1400x900")
        
        # Modern color scheme matching web GUI
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_medium': '#1a1f3a',
            'accent_blue': '#2196f3',
            'accent_green': '#4caf50',
            'accent_red': '#f44336',
            'accent_orange': '#ff9800',
            'text_white': '#ffffff',
            'text_gray': '#b0b0b0',
            'card_bg': '#1e2139',
            'hover': '#2a2f4a'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        self.db_path = "semptify_modern.db"
        self.init_database()
        
        # Create main layout
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()
        
        # Show home by default
        self.show_home()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                filepath TEXT,
                file_hash TEXT,
                category TEXT,
                size INTEGER,
                upload_date TEXT,
                notes TEXT
            )
        ''')
        
        # Payments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY,
                date TEXT,
                amount REAL,
                type TEXT,
                notes TEXT,
                created_at TEXT
            )
        ''')
        
        # Timeline
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timeline (
                id INTEGER PRIMARY KEY,
                date TEXT,
                title TEXT,
                category TEXT,
                description TEXT,
                created_at TEXT
            )
        ''')
        
        # Calendar
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calendar (
                id INTEGER PRIMARY KEY,
                date TEXT,
                title TEXT,
                description TEXT,
                priority TEXT,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_header(self):
        """Create modern header bar"""
        header = tk.Frame(self.root, bg=self.colors['bg_medium'], height=80)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        title_frame.pack(side='left', padx=30, pady=20)
        
        tk.Label(title_frame, text="🛡️ SEMPTIFY", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_medium'], 
                fg=self.colors['accent_blue']).pack(side='left')
        
        tk.Label(title_frame, text="Tenant Rights Protection Platform", 
                font=('Segoe UI', 10),
                bg=self.colors['bg_medium'], 
                fg=self.colors['text_gray']).pack(side='left', padx=15)
        
        # Quick actions
        actions_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        actions_frame.pack(side='right', padx=30)
        
        self.create_header_button(actions_frame, "📁 Upload", self.quick_upload, self.colors['accent_blue'])
        self.create_header_button(actions_frame, "💾 Backup", self.quick_backup, self.colors['accent_green'])
        self.create_header_button(actions_frame, "⚙️ Settings", self.show_settings, self.colors['accent_orange'])
    
    def create_header_button(self, parent, text, command, color):
        """Create modern header button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg='white',
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat', padx=15, pady=8,
                       cursor='hand2', bd=0)
        btn.pack(side='left', padx=5)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=self._lighten_color(color))
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = tk.Frame(self.root, bg=self.colors['bg_medium'], width=250)
        sidebar.pack(fill='y', side='left')
        sidebar.pack_propagate(False)
        
        # Navigation items
        nav_items = [
            ("🏠 Home", self.show_home, "Overview and quick stats"),
            ("📁 Documents", self.show_documents, "Secure document vault"),
            ("💰 Payments", self.show_payments, "Track rent and fees"),
            ("📅 Timeline", self.show_timeline, "Event history"),
            ("📆 Calendar", self.show_calendar, "Deadlines & reminders"),
            ("⚖️ Legal", self.show_legal, "Complaints & letters"),
            ("📊 Reports", self.show_reports, "Generate reports"),
            ("🔍 Evidence", self.show_evidence, "Photo logger"),
        ]
        
        tk.Label(sidebar, text="NAVIGATION", 
                font=('Segoe UI', 9, 'bold'),
                bg=self.colors['bg_medium'], 
                fg=self.colors['text_gray']).pack(pady=20, padx=20, anchor='w')
        
        self.nav_buttons = []
        for text, command, tooltip in nav_items:
            btn = self.create_nav_button(sidebar, text, command, tooltip)
            self.nav_buttons.append(btn)
    
    def create_nav_button(self, parent, text, command, tooltip):
        """Create sidebar navigation button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=self.colors['bg_medium'], 
                       fg=self.colors['text_white'],
                       font=('Segoe UI', 11),
                       relief='flat', anchor='w',
                       padx=20, pady=12, bd=0,
                       cursor='hand2')
        btn.pack(fill='x', padx=5, pady=2)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=self.colors['hover'])
        def on_leave(e):
            if btn != self.active_nav:
                btn.config(bg=self.colors['bg_medium'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_main_content(self):
        """Create main content area"""
        self.content_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.content_frame.pack(fill='both', expand=True, side='left')
        
        self.active_nav = None
    
    def create_status_bar(self):
        """Create status bar"""
        status = tk.Frame(self.root, bg=self.colors['bg_medium'], height=30)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status, text="✓ Ready", 
                                     font=('Segoe UI', 9),
                                     bg=self.colors['bg_medium'], 
                                     fg=self.colors['text_gray'],
                                     anchor='w')
        self.status_label.pack(side='left', padx=20)
        
        # Stats
        self.stats_label = tk.Label(status, text="", 
                                    font=('Segoe UI', 9),
                                    bg=self.colors['bg_medium'], 
                                    fg=self.colors['text_gray'],
                                    anchor='e')
        self.stats_label.pack(side='right', padx=20)
        
        self.update_stats()
    
    def clear_content(self):
        """Clear main content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def create_card(self, parent, title, icon="", color=None):
        """Create modern card component"""
        if color is None:
            color = self.colors['card_bg']
        
        card = tk.Frame(parent, bg=color, relief='flat', bd=0)
        
        header = tk.Frame(card, bg=color)
        header.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header, text=f"{icon} {title}", 
                font=('Segoe UI', 14, 'bold'),
                bg=color, fg=self.colors['text_white']).pack(side='left')
        
        content = tk.Frame(card, bg=color)
        content.pack(fill='both', expand=True, padx=20, pady=10)
        
        return card, content
    
    def show_home(self):
        """Home/Dashboard view"""
        self.clear_content()
        self.set_active_nav(0)
        
        # Welcome section
        welcome = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        welcome.pack(fill='x', padx=30, pady=20)
        
        tk.Label(welcome, text="Welcome to Semptify", 
                font=('Segoe UI', 28, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(anchor='w')
        
        tk.Label(welcome, text="Your personal tenant rights management system", 
                font=('Segoe UI', 12),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_gray']).pack(anchor='w', pady=5)
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        stats_frame.pack(fill='x', padx=30, pady=10)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*), COALESCE(SUM(size), 0) FROM documents')
        doc_count, doc_size = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM payments')
        pay_count, pay_total = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*) FROM timeline')
        event_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM calendar WHERE date >= date("now")')
        upcoming_count = cursor.fetchone()[0]
        
        conn.close()
        
        stats = [
            ("📁", "Documents", doc_count, f"{doc_size/1024/1024:.1f} MB", self.colors['accent_blue']),
            ("💰", "Payments", pay_count, f"${pay_total:,.2f}", self.colors['accent_green']),
            ("📅", "Events", event_count, "Timeline", self.colors['accent_orange']),
            ("📆", "Reminders", upcoming_count, "Upcoming", self.colors['accent_red']),
        ]
        
        for i, (icon, label, count, detail, color) in enumerate(stats):
            self.create_stat_card(stats_frame, icon, label, count, detail, color).grid(row=0, column=i, padx=10, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
        
        # Recent activity
        card, content = self.create_card(self.content_frame, "Recent Activity", "📊")
        card.pack(fill='both', expand=True, padx=30, pady=10)
        
        activity_text = scrolledtext.ScrolledText(content, height=15,
                                                  bg=self.colors['bg_dark'],
                                                  fg=self.colors['text_white'],
                                                  font=('Consolas', 10),
                                                  relief='flat', bd=0)
        activity_text.pack(fill='both', expand=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        activity_text.insert(tk.END, "RECENT TIMELINE EVENTS:\n\n")
        cursor.execute('SELECT date, title, category FROM timeline ORDER BY created_at DESC LIMIT 10')
        for row in cursor.fetchall():
            activity_text.insert(tk.END, f"• {row[0]} - [{row[2]}] {row[1]}\n")
        
        conn.close()
        
        self.update_status("✓ Dashboard loaded")
    
    def create_stat_card(self, parent, icon, label, count, detail, color):
        """Create statistics card"""
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief='flat', bd=0, padx=20, pady=20)
        
        tk.Label(card, text=icon, 
                font=('Segoe UI', 32),
                bg=self.colors['card_bg'], 
                fg=color).pack()
        
        tk.Label(card, text=str(count), 
                font=('Segoe UI', 28, 'bold'),
                bg=self.colors['card_bg'], 
                fg=self.colors['text_white']).pack()
        
        tk.Label(card, text=label, 
                font=('Segoe UI', 11),
                bg=self.colors['card_bg'], 
                fg=self.colors['text_gray']).pack()
        
        tk.Label(card, text=detail, 
                font=('Segoe UI', 9),
                bg=self.colors['card_bg'], 
                fg=color).pack(pady=5)
        
        return card
    
    def show_documents(self):
        """Documents vault view"""
        self.clear_content()
        self.set_active_nav(1)
        
        # Header with actions
        header = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        header.pack(fill='x', padx=30, pady=20)
        
        tk.Label(header, text="📁 Document Vault", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(side='left')
        
        btn_frame = tk.Frame(header, bg=self.colors['bg_dark'])
        btn_frame.pack(side='right')
        
        self.create_action_button(btn_frame, "📤 Upload", self.upload_document, self.colors['accent_green'])
        self.create_action_button(btn_frame, "👁️ Open", self.open_document, self.colors['accent_blue'])
        self.create_action_button(btn_frame, "🗑️ Delete", self.delete_document, self.colors['accent_red'])
        
        # Document list with modern styling
        list_frame = tk.Frame(self.content_frame, bg=self.colors['card_bg'])
        list_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Custom treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.Treeview',
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_white'],
                       fieldbackground=self.colors['bg_dark'],
                       borderwidth=0)
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text_white'],
                       borderwidth=0)
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['accent_blue'])])
        
        columns = ('Filename', 'Category', 'Date', 'Size', 'Hash')
        self.doc_tree = ttk.Treeview(list_frame, columns=columns, 
                                     show='headings', height=20,
                                     style='Modern.Treeview')
        
        for col in columns:
            self.doc_tree.heading(col, text=col)
            self.doc_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.doc_tree.yview)
        self.doc_tree.configure(yscrollcommand=scrollbar.set)
        
        self.doc_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        self.load_documents()
        self.update_status("✓ Documents loaded")
    
    def show_payments(self):
        """Payments ledger view"""
        self.clear_content()
        self.set_active_nav(2)
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        header.pack(fill='x', padx=30, pady=20)
        
        tk.Label(header, text="💰 Payment Ledger", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(side='left')
        
        # Add payment card
        card, content = self.create_card(self.content_frame, "Add Payment", "➕", self.colors['card_bg'])
        card.pack(fill='x', padx=30, pady=10)
        
        form = tk.Frame(content, bg=self.colors['card_bg'])
        form.pack(fill='x', pady=10)
        
        # Form fields
        fields = [
            ("Date:", tk.Entry(form, width=15, font=('Segoe UI', 10))),
            ("Amount:", tk.Entry(form, width=15, font=('Segoe UI', 10))),
            ("Type:", ttk.Combobox(form, values=['Rent', 'Late Fee', 'Deposit', 'Utility', 'Other'], width=13)),
            ("Notes:", tk.Entry(form, width=40, font=('Segoe UI', 10))),
        ]
        
        self.payment_entries = {}
        for i, (label, widget) in enumerate(fields):
            tk.Label(form, text=label, 
                    bg=self.colors['card_bg'], 
                    fg=self.colors['text_gray'],
                    font=('Segoe UI', 10)).grid(row=i//2, column=(i%2)*2, padx=10, pady=5, sticky='e')
            widget.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5, sticky='w')
            self.payment_entries[label.strip(':')] = widget
        
        self.payment_entries['Date'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.payment_entries['Type'].set('Rent')
        
        tk.Button(form, text="➕ Add Payment", command=self.add_payment,
                 bg=self.colors['accent_green'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=20, pady=10,
                 cursor='hand2').grid(row=2, column=0, columnspan=4, pady=15)
        
        # Payment list
        card2, content2 = self.create_card(self.content_frame, "Payment History", "📊")
        card2.pack(fill='both', expand=True, padx=30, pady=10)
        
        columns = ('Date', 'Amount', 'Type', 'Notes')
        self.pay_tree = ttk.Treeview(content2, columns=columns, 
                                     show='headings', height=15,
                                     style='Modern.Treeview')
        
        for col in columns:
            self.pay_tree.heading(col, text=col)
            self.pay_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(content2, orient='vertical', command=self.pay_tree.yview)
        self.pay_tree.configure(yscrollcommand=scrollbar.set)
        
        self.pay_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Summary
        self.pay_summary = tk.Label(content2, text="", 
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['card_bg'], 
                                    fg=self.colors['accent_green'])
        self.pay_summary.pack(pady=10)
        
        self.load_payments()
        self.update_status("✓ Payments loaded")
    
    def show_timeline(self):
        """Timeline view"""
        self.clear_content()
        self.set_active_nav(3)
        
        tk.Label(self.content_frame, text="📅 Timeline", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(padx=30, pady=20, anchor='w')
        
        # Add event card
        card, content = self.create_card(self.content_frame, "Add Event", "➕")
        card.pack(fill='x', padx=30, pady=10)
        
        form = tk.Frame(content, bg=self.colors['card_bg'])
        form.pack(fill='x', pady=10)
        
        self.timeline_entries = {}
        fields = [
            ("Date:", tk.Entry(form, width=15, font=('Segoe UI', 10))),
            ("Title:", tk.Entry(form, width=40, font=('Segoe UI', 10))),
            ("Category:", ttk.Combobox(form, values=['Issue', 'Maintenance', 'Payment', 'Communication', 'Legal'], width=13)),
            ("Description:", tk.Entry(form, width=40, font=('Segoe UI', 10))),
        ]
        
        for i, (label, widget) in enumerate(fields):
            tk.Label(form, text=label, 
                    bg=self.colors['card_bg'], 
                    fg=self.colors['text_gray'],
                    font=('Segoe UI', 10)).grid(row=i//2, column=(i%2)*2, padx=10, pady=5, sticky='e')
            widget.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5, sticky='w')
            self.timeline_entries[label.strip(':')] = widget
        
        self.timeline_entries['Date'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.timeline_entries['Category'].set('Issue')
        
        tk.Button(form, text="➕ Add Event", command=self.add_timeline_event,
                 bg=self.colors['accent_blue'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=20, pady=10,
                 cursor='hand2').grid(row=2, column=0, columnspan=4, pady=15)
        
        # Timeline display
        card2, content2 = self.create_card(self.content_frame, "Event History", "📊")
        card2.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.timeline_text = scrolledtext.ScrolledText(content2, height=15,
                                                       bg=self.colors['bg_dark'],
                                                       fg=self.colors['text_white'],
                                                       font=('Consolas', 10),
                                                       relief='flat')
        self.timeline_text.pack(fill='both', expand=True)
        
        self.load_timeline()
        self.update_status("✓ Timeline loaded")
    
    def show_calendar(self):
        """Calendar/reminders view"""
        self.clear_content()
        self.set_active_nav(4)
        
        tk.Label(self.content_frame, text="📆 Deadlines & Reminders", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(padx=30, pady=20, anchor='w')
        
        messagebox.showinfo("Calendar", "Calendar view - Add reminders and track deadlines")
        self.update_status("✓ Calendar opened")
    
    def show_legal(self):
        """Legal/complaint builder view"""
        self.clear_content()
        self.set_active_nav(5)
        
        tk.Label(self.content_frame, text="⚖️ Legal Documents", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(padx=30, pady=20, anchor='w')
        
        messagebox.showinfo("Legal", "Complaint builder with legal templates")
        self.update_status("✓ Legal tools opened")
    
    def show_reports(self):
        """Reports view"""
        self.clear_content()
        self.set_active_nav(6)
        
        tk.Label(self.content_frame, text="📊 Reports & Analytics", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(padx=30, pady=20, anchor='w')
        
        messagebox.showinfo("Reports", "Generate PDF reports and export data")
        self.update_status("✓ Reports opened")
    
    def show_evidence(self):
        """Evidence logger view"""
        self.clear_content()
        self.set_active_nav(7)
        
        tk.Label(self.content_frame, text="🔍 Evidence Logger", 
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_dark'], 
                fg=self.colors['text_white']).pack(padx=30, pady=20, anchor='w')
        
        messagebox.showinfo("Evidence", "Photo and document evidence logger")
        self.update_status("✓ Evidence logger opened")
    
    def show_settings(self):
        """Settings"""
        messagebox.showinfo("Settings", "Application settings and preferences")
    
    # Action methods
    
    def create_action_button(self, parent, text, command, color):
        """Create action button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg='white',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat', padx=15, pady=8,
                       cursor='hand2')
        btn.pack(side='left', padx=5)
        
        def on_enter(e):
            btn.config(bg=self._lighten_color(color))
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def upload_document(self):
        """Upload document"""
        filepath = filedialog.askopenfilename(title="Select Document")
        if not filepath:
            return
        
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
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
        
        category = simpledialog.askstring("Category", "Document category:", initialvalue="Document")
        
        size = Path(filepath).stat().st_size
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documents (filename, filepath, file_hash, category, size, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (dest.name, str(dest), file_hash, category, size, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.load_documents()
        self.update_status(f"✓ Uploaded: {dest.name}")
    
    def open_document(self):
        """Open selected document"""
        selected = self.doc_tree.selection()
        if not selected:
            return
        
        filename = self.doc_tree.item(selected[0])['values'][0]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT filepath FROM documents WHERE filename = ?', (filename,))
        result = cursor.fetchone()
        conn.close()
        
        if result and Path(result[0]).exists():
            import os
            os.startfile(result[0])
    
    def delete_document(self):
        """Delete document"""
        selected = self.doc_tree.selection()
        if not selected:
            return
        
        if messagebox.askyesno("Confirm", "Delete selected document?"):
            filename = self.doc_tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT filepath FROM documents WHERE filename = ?', (filename,))
            result = cursor.fetchone()
            
            if result:
                try:
                    Path(result[0]).unlink()
                except:
                    pass
                cursor.execute('DELETE FROM documents WHERE filename = ?', (filename,))
                conn.commit()
            
            conn.close()
            self.load_documents()
            self.update_status(f"✓ Deleted: {filename}")
    
    def load_documents(self):
        """Load documents into tree"""
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT filename, category, upload_date, size, file_hash FROM documents ORDER BY upload_date DESC')
        
        for row in cursor.fetchall():
            filename, cat, date, size, hash_val = row
            size_kb = f"{size/1024:.1f}KB"
            hash_short = hash_val[:16] + "..." if hash_val else "N/A"
            self.doc_tree.insert('', 'end', values=(filename, cat, date[:10], size_kb, hash_short))
        
        conn.close()
    
    def add_payment(self):
        """Add payment"""
        date = self.payment_entries['Date'].get()
        amount = self.payment_entries['Amount'].get()
        pay_type = self.payment_entries['Type'].get()
        notes = self.payment_entries['Notes'].get()
        
        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (date, amount, type, notes, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, pay_type, notes, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.payment_entries['Amount'].delete(0, tk.END)
        self.payment_entries['Notes'].delete(0, tk.END)
        
        self.load_payments()
        self.update_status(f"✓ Added payment: ${amount:.2f}")
    
    def load_payments(self):
        """Load payments"""
        for item in self.pay_tree.get_children():
            self.pay_tree.delete(item)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT date, amount, type, notes FROM payments ORDER BY date DESC')
        
        total = 0
        for row in cursor.fetchall():
            date, amount, pay_type, notes = row
            self.pay_tree.insert('', 'end', values=(date, f"${amount:.2f}", pay_type, notes))
            total += amount
        
        conn.close()
        
        self.pay_summary.config(text=f"Total Payments: ${total:,.2f}")
    
    def add_timeline_event(self):
        """Add timeline event"""
        date = self.timeline_entries['Date'].get()
        title = self.timeline_entries['Title'].get()
        category = self.timeline_entries['Category'].get()
        description = self.timeline_entries['Description'].get()
        
        if not title:
            messagebox.showwarning("Missing", "Please enter a title")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO timeline (date, title, category, description, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, title, category, description, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        self.timeline_entries['Title'].delete(0, tk.END)
        self.timeline_entries['Description'].delete(0, tk.END)
        
        self.load_timeline()
        self.update_status(f"✓ Added event: {title}")
    
    def load_timeline(self):
        """Load timeline"""
        self.timeline_text.delete(1.0, tk.END)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT date, title, category, description FROM timeline ORDER BY date DESC')
        
        self.timeline_text.insert(tk.END, "═" * 80 + "\n")
        self.timeline_text.insert(tk.END, "                    EVENT TIMELINE\n")
        self.timeline_text.insert(tk.END, "═" * 80 + "\n\n")
        
        for row in cursor.fetchall():
            date, title, category, description = row
            self.timeline_text.insert(tk.END, f"📅 {date} - [{category}]\n")
            self.timeline_text.insert(tk.END, f"   ▶ {title}\n")
            if description:
                self.timeline_text.insert(tk.END, f"   {description}\n")
            self.timeline_text.insert(tk.END, "\n")
        
        conn.close()
    
    def quick_upload(self):
        """Quick upload action"""
        self.show_documents()
        self.root.after(100, self.upload_document)
    
    def quick_backup(self):
        """Quick backup"""
        backup_dir = filedialog.askdirectory(title="Select Backup Location")
        if backup_dir:
            backup_path = Path(backup_dir) / f"semptify_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path.mkdir(exist_ok=True)
            
            shutil.copy(self.db_path, backup_path / "database.db")
            
            if Path("uploads").exists():
                shutil.copytree("uploads", backup_path / "uploads", dirs_exist_ok=True)
            
            messagebox.showinfo("Backup Complete", f"Backup created at:\n{backup_path}")
            self.update_status(f"✓ Backup created")
    
    # Utility methods
    
    def set_active_nav(self, index):
        """Set active navigation button"""
        for btn in self.nav_buttons:
            btn.config(bg=self.colors['bg_medium'])
        
        if 0 <= index < len(self.nav_buttons):
            self.active_nav = self.nav_buttons[index]
            self.active_nav.config(bg=self.colors['accent_blue'])
    
    def update_status(self, msg):
        """Update status bar"""
        self.status_label.config(text=msg)
        self.root.update()
    
    def update_stats(self):
        """Update stats in status bar"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM documents')
        docs = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM payments')
        payments = cursor.fetchone()[0]
        
        conn.close()
        
        self.stats_label.config(text=f"📁 {docs} docs  •  💰 {payments} payments")
        
        self.root.after(5000, self.update_stats)
    
    def _lighten_color(self, color):
        """Lighten a hex color"""
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        return f'#{r:02x}{g:02x}{b:02x}'

if __name__ == "__main__":
    import os
    os.chdir("C:/Semptify/Semptify")
    
    root = tk.Tk()
    app = ModernSemptifyGUI(root)
    root.mainloop()
