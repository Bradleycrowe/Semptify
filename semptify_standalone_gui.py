# Create a standalone Python GUI using Tkinter - NO FLASK
# This isolates all functionality from web routing issues

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
import sqlite3
from datetime import datetime

class SemptifyStandaloneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Semptify - Standalone Core GUI")
        self.root.geometry("900x700")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Document Vault
        self.vault_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.vault_tab, text="Document Vault")
        self.create_vault_tab()
        
        # Tab 2: Payment Ledger
        self.ledger_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ledger_tab, text="Payment Ledger")
        self.create_ledger_tab()
        
        # Tab 3: Timeline
        self.timeline_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.timeline_tab, text="Timeline")
        self.create_timeline_tab()
        
        # Tab 4: Database Info
        self.db_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.db_tab, text="Database")
        self.create_db_tab()
        
        # Status bar
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status("✓ Standalone GUI loaded - No Flask required")
    
    def update_status(self, msg):
        self.status.config(text=msg)
        self.root.update()
    
    def create_vault_tab(self):
        ttk.Label(self.vault_tab, text="Document Vault", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # List documents
        ttk.Button(self.vault_tab, text="List Documents", 
                  command=self.list_vault_documents).pack(pady=5)
        
        # Document list
        self.vault_list = scrolledtext.ScrolledText(self.vault_tab, height=20)
        self.vault_list.pack(fill='both', expand=True, padx=20, pady=10)
    
    def create_ledger_tab(self):
        ttk.Label(self.ledger_tab, text="Payment Ledger", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Add payment form
        form = ttk.Frame(self.ledger_tab)
        form.pack(pady=10)
        
        ttk.Label(form, text="Amount:").grid(row=0, column=0, padx=5)
        self.amount_entry = ttk.Entry(form, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(form, text="Date:").grid(row=0, column=2, padx=5)
        self.date_entry = ttk.Entry(form, width=15)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=3, padx=5)
        
        ttk.Button(form, text="Add Payment", command=self.add_payment).grid(row=0, column=4, padx=5)
        
        # Payment list
        self.ledger_list = scrolledtext.ScrolledText(self.ledger_tab, height=20)
        self.ledger_list.pack(fill='both', expand=True, padx=20, pady=10)
    
    def create_timeline_tab(self):
        ttk.Label(self.timeline_tab, text="Timeline", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Timeline display
        self.timeline_text = scrolledtext.ScrolledText(self.timeline_tab, height=25)
        self.timeline_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Button(self.timeline_tab, text="Load Timeline", 
                  command=self.load_timeline).pack(pady=5)
    
    def create_db_tab(self):
        ttk.Label(self.db_tab, text="Database Info", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Button(self.db_tab, text="Check Database", 
                  command=self.check_database).pack(pady=5)
        
        self.db_info = scrolledtext.ScrolledText(self.db_tab, height=25)
        self.db_info.pack(fill='both', expand=True, padx=20, pady=10)
    
    def list_vault_documents(self):
        self.vault_list.delete(1.0, tk.END)
        vault_dir = "uploads/vault"
        
        if os.path.exists(vault_dir):
            files = []
            for root, dirs, filenames in os.walk(vault_dir):
                for f in filenames:
                    full_path = os.path.join(root, f)
                    size = os.path.getsize(full_path)
                    files.append((f, size, full_path))
            
            self.vault_list.insert(tk.END, f"Found {len(files)} documents:\n\n")
            for name, size, path in files:
                self.vault_list.insert(tk.END, f"📄 {name}\n")
                self.vault_list.insert(tk.END, f"   Size: {size:,} bytes\n")
                self.vault_list.insert(tk.END, f"   Path: {path}\n\n")
            
            self.update_status(f"✓ Listed {len(files)} vault documents")
        else:
            self.vault_list.insert(tk.END, "Vault directory not found\n")
            self.update_status("⚠️ Vault directory not found")
    
    def add_payment(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        
        if amount and date:
            self.ledger_list.insert(tk.END, f"✓ Added: ${amount} on {date}\n")
            self.amount_entry.delete(0, tk.END)
            self.update_status(f"✓ Added payment: ${amount}")
        else:
            messagebox.showwarning("Missing Data", "Please enter amount and date")
    
    def load_timeline(self):
        self.timeline_text.delete(1.0, tk.END)
        
        # Show sample timeline
        events = [
            ("2025-01-15", "Moved into apartment", "Started tenancy"),
            ("2025-02-01", "First rent payment", "$1500"),
            ("2025-03-01", "Maintenance request", "Broken heater"),
            ("2025-03-15", "Heater fixed", "Took 2 weeks"),
        ]
        
        self.timeline_text.insert(tk.END, "Timeline Events:\n")
        self.timeline_text.insert(tk.END, "="*60 + "\n\n")
        
        for date, title, desc in events:
            self.timeline_text.insert(tk.END, f"📅 {date}\n")
            self.timeline_text.insert(tk.END, f"   {title}\n")
            self.timeline_text.insert(tk.END, f"   {desc}\n\n")
        
        self.update_status("✓ Timeline loaded")
    
    def check_database(self):
        self.db_info.delete(1.0, tk.END)
        
        db_path = "users.db"
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Get tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                self.db_info.insert(tk.END, f"✓ Database: {db_path}\n")
                self.db_info.insert(tk.END, f"✓ Tables: {len(tables)}\n\n")
                
                for table in tables:
                    self.db_info.insert(tk.END, f"📊 {table[0]}\n")
                    
                    # Get row count
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                        count = cursor.fetchone()[0]
                        self.db_info.insert(tk.END, f"   Rows: {count}\n")
                    except:
                        self.db_info.insert(tk.END, f"   (cannot count)\n")
                    
                    self.db_info.insert(tk.END, "\n")
                
                conn.close()
                self.update_status(f"✓ Database has {len(tables)} tables")
                
            except Exception as e:
                self.db_info.insert(tk.END, f"✗ Error: {str(e)}\n")
                self.update_status("✗ Database error")
        else:
            self.db_info.insert(tk.END, "Database file not found\n")
            self.update_status("⚠️ Database not found")

if __name__ == "__main__":
    # Change to Semptify directory
    os.chdir("C:\\Semptify\\Semptify")
    
    root = tk.Tk()
    app = SemptifyStandaloneGUI(root)
    root.mainloop()
