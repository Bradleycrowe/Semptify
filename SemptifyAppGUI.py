import sys
import json
import os
from spellchecker import SpellChecker

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QStackedWidget, QDialog, QTextEdit, QListWidget, QComboBox, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class SemptifyAppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize attributes early so linters/tools know they exist.
        self.pages = None
        self.home_page = None
        self.library_page = None
        self.office_page = None
        self.tools_page = None
        self.vault_page = None
        self.help_page = None

        self.setWindowTitle("Semptify App GUI")
        self.setGeometry(100, 100, 900, 600)
        try:
            # setWindowIcon will be a no-op if QIcon is a stub
            self.setWindowIcon(QIcon("static/icons/Semptfylogo.svg"))
        except Exception:
            pass
        self.initUI()

    def initUI(self):
        # Main window setup
        central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Top Bar
        self.setup_top_bar()

        # Bottom layout: pages on left, concierge box on right
        bottom_layout = QHBoxLayout()
        self.pages = QStackedWidget()
        bottom_layout.addWidget(self.pages, 1)  # pages expand
        self.concierge_box = self.make_concierge_box()
        bottom_layout.addWidget(self.concierge_box, 0)  # concierge fixed
        self.main_layout.addLayout(bottom_layout)

        # Add core pages
        self.setup_core_pages()

        # Add Office module buttons
        self.setup_office_buttons()

    def setup_top_bar(self):
        top_bar = QFrame()
        top_bar.setFrameShape(QFrame.StyledPanel)
        top_bar.setStyleSheet("background: #fff; border-bottom: 1px solid #e9eef6; width: 100%;")
        # Set top-bar height to match logo height plus nudge
        top_bar.setFixedHeight(150)
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)

        logo_label = QLabel()
        pixmap = QPixmap("static/icons/Semptfylogo.svg")
        if pixmap.isNull():
            logo_label.setText("Semptify")
        else:
            # scale the logo to fit with border
            logo_size = 140  # increased for total image and border
            scaled_pixmap = pixmap.scaled(logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setFixedSize(logo_size, logo_size)

        top_bar_layout.addWidget(logo_label, alignment=Qt.AlignTop)

        # Navigation buttons to switch between core pages
        nav = [
            ("Home", lambda: self.pages.setCurrentWidget(self.home_page)),
            ("Library", lambda: self.pages.setCurrentWidget(self.library_page)),
            ("Office", lambda: self.pages.setCurrentWidget(self.office_page)),
            ("Tools", lambda: self.pages.setCurrentWidget(self.tools_page)),
            ("Vault", lambda: self.pages.setCurrentWidget(self.vault_page)),
            ("Admin", lambda: self.pages.setCurrentWidget(self.admin_page)),
        ]
        for (lbl, cb) in nav:
            b = QPushButton(lbl)
            b.setFlat(True)
            b.setStyleSheet("text-align: right;")
            b.clicked.connect(cb)
            top_bar_layout.addWidget(b)

        # push any future top-bar widgets to the right; keeps logo compact
        top_bar_layout.addStretch()

        self.main_layout.addWidget(top_bar)

    def setup_core_pages(self):
        # create simple placeholder content for each page so they open visibly
        def make_page(title_text):
            p = QWidget()
            layout = QVBoxLayout()
            p.setLayout(layout)
            lbl = QLabel(title_text)
            lbl.setStyleSheet("font-size:18px; font-weight:600; margin:12px;")
            layout.addWidget(lbl)
            layout.addStretch()
            return p

        self.home_page = make_page("Home")
        self.library_page = make_page("Library")
        self.office_page = self.make_office_page()
        self.tools_page = self.make_tools_page()
        self.vault_page = self.make_vault_page()
        self.temp_todo_page = self.make_temp_todo_page()
        self.admin_page = self.make_admin_page()

        for p in (self.home_page, self.library_page, self.office_page, self.tools_page, self.vault_page, self.temp_todo_page, self.admin_page):
            self.pages.addWidget(p)

    def make_office_page(self):
        p = QWidget()
        layout = QVBoxLayout()
        p.setLayout(layout)
        lbl = QLabel("Office")
        lbl.setStyleSheet("font-size:18px; font-weight:600; margin:12px;")
        layout.addWidget(lbl)

        # Add office-specific buttons
        generate_complaint_btn = QPushButton("Generate Complaint")
        generate_complaint_btn.clicked.connect(self.open_complaint_generator)
        layout.addWidget(generate_complaint_btn)

        layout.addStretch()
        return p

    def make_tools_page(self):
        p = QWidget()
        layout = QVBoxLayout()
        p.setLayout(layout)
        lbl = QLabel("Tools")
        lbl.setStyleSheet("font-size:18px; font-weight:600; margin:12px;")
        layout.addWidget(lbl)

        # Add tools buttons
        rights_explorer_btn = QPushButton("Rights Explorer")
        rights_explorer_btn.clicked.connect(self.open_rights_explorer)
        layout.addWidget(rights_explorer_btn)

        violation_mapper_btn = QPushButton("Violation Mapper")
        violation_mapper_btn.clicked.connect(self.open_violation_mapper)
        layout.addWidget(violation_mapper_btn)

        layout.addStretch()
        return p

    def make_temp_todo_page(self):
        p = QWidget()
        layout = QVBoxLayout()
        p.setLayout(layout)
        lbl = QLabel("Temp Todo Checklist")
        lbl.setStyleSheet("font-size:18px; font-weight:600; margin:12px;")
        layout.addWidget(lbl)

        self.todo_list = QListWidget()
        self.todo_list.setStyleSheet("font-size:14px;")
        layout.addWidget(self.todo_list)

        # Load existing todos
        self.load_temp_todos()

        # Add new todo input
        input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Add new temp todo...")
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_temp_todo)
        input_layout.addWidget(self.todo_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        # Save button
        save_btn = QPushButton("Save Todos")
        save_btn.clicked.connect(self.save_temp_todos)
        layout.addWidget(save_btn)

        layout.addStretch()
        return p


    def make_concierge_box(self):
        p = QWidget()
        p.setFixedWidth(120)  # as big as logo width
        p.setStyleSheet("border: 1px solid #ccc; padding: 2px;")
        layout = QVBoxLayout()
        p.setLayout(layout)
        lbl = QLabel("Concierge")
        lbl.setStyleSheet("font-size:12px; font-weight:600; margin:2px;")
        layout.addWidget(lbl)

        # Chat history - smaller
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMaximumHeight(200)
        layout.addWidget(self.chat_history)

        # Input - smaller
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask...")
        send_btn = QPushButton("Send")
        send_btn.setFixedSize(40, 20)
        send_btn.clicked.connect(self.send_to_concierge)
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

        return p

    def make_vault_page(self):
        p = QWidget()
        layout = QVBoxLayout()
        p.setLayout(layout)
        lbl = QLabel("Vault")
        lbl.setStyleSheet("font-size:18px; font-weight:600; margin:12px;")
        layout.addWidget(lbl)

        # Local AI Chat
        chat_layout = QVBoxLayout()
        chat_layout.addWidget(QLabel("Local AI Assistant:"))
        self.vault_chat_history = QTextEdit()
        self.vault_chat_history.setReadOnly(True)
        self.vault_chat_history.setMaximumHeight(200)
        chat_layout.addWidget(self.vault_chat_history)

        input_layout = QHBoxLayout()
        self.vault_chat_input = QLineEdit()
        self.vault_chat_input.setPlaceholderText("Ask local AI...")
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_to_local_ai)
        input_layout.addWidget(self.vault_chat_input)
        input_layout.addWidget(send_btn)
        chat_layout.addLayout(input_layout)
        layout.addLayout(chat_layout)

        layout.addStretch()
        return p

    def make_admin_page(self):
        p = QWidget()
        layout = QVBoxLayout()
        p.setLayout(layout)
        lbl = QLabel("Admin AI Management")
        lbl.setStyleSheet("font-size:18px; font-weight:600; margin:12px;")
        layout.addWidget(lbl)

        # AI Config
        layout.addWidget(QLabel("AI Configurations:"))
        update_local_btn = QPushButton("Update Local AI Model")
        update_local_btn.clicked.connect(self.update_local_model)
        layout.addWidget(update_local_btn)

        update_external_btn = QPushButton("Update External AI Settings")
        update_external_btn.clicked.connect(self.update_external_settings)
        layout.addWidget(update_external_btn)

        # Parenting/Training
        layout.addWidget(QLabel("AI Parenting & Learning:"))
        train_btn = QPushButton("Train AIs")
        train_btn.clicked.connect(self.train_ais)
        layout.addWidget(train_btn)

        # Journal
        layout.addWidget(QLabel("Journal:"))
        # Workspace input
        ws_layout = QHBoxLayout()
        ws_layout.addWidget(QLabel("Workspace/Environment:"))
        self.ws_input = QLineEdit()
        self.ws_input.setPlaceholderText("e.g., Semptify dev")
        ws_layout.addWidget(self.ws_input)
        layout.addLayout(ws_layout)

        # Notes editor
        self.notes_editor = QTextEdit()
        self.notes_editor.setPlaceholderText("Add notes here...")
        layout.addWidget(self.notes_editor)

        # Load/Save buttons
        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Load Journal")
        load_btn.clicked.connect(self.load_journal)
        save_btn = QPushButton("Save & Sync")
        save_btn.clicked.connect(self.save_journal)
        spellcheck_btn = QPushButton("Spellcheck")
        spellcheck_btn.clicked.connect(self.spellcheck_notes)
        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(spellcheck_btn)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return p

    def setup_office_buttons(self):
        office_button = QPushButton("Office Module")
        office_button.clicked.connect(self.open_office_page)
        self.main_layout.addWidget(office_button)

        create_room_button = QPushButton("Create Room")
        create_room_button.clicked.connect(self.create_room)
        self.main_layout.addWidget(create_room_button)

        list_rooms_button = QPushButton("List Rooms")
        list_rooms_button.clicked.connect(self.list_rooms)
        self.main_layout.addWidget(list_rooms_button)

        upload_document_button = QPushButton("Upload Document")
        upload_document_button.clicked.connect(self.upload_document)
        self.main_layout.addWidget(upload_document_button)

    def open_office_page(self):
        print("Office Module Opened")

    def create_room(self):
        print("Create Room Triggered")

    def list_rooms(self):
        print("List Rooms Triggered")

    def upload_document(self):
        print("Upload Document Triggered")

    def open_rights_explorer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Rights Scenario Explorer")
        dialog.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()

        label = QLabel("Select a legal scenario:")
        layout.addWidget(label)

        scenarios = QListWidget()
        scenarios.addItem("Eviction Notice")
        scenarios.addItem("Rent Increase")
        scenarios.addItem("Maintenance Issues")
        scenarios.addItem("Lease Violation")
        layout.addWidget(scenarios)

        generate_button = QPushButton("Generate Complaint")
        generate_button.clicked.connect(lambda: self.generate_complaint(scenarios.currentItem().text() if scenarios.currentItem() else "None"))
        layout.addWidget(generate_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def generate_complaint(self, scenario):
        print(f"Generating complaint for: {scenario}")
        # Placeholder for complaint generation logic

    def open_violation_mapper(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Violation Pattern Mapper")
        dialog.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()

        label = QLabel("Log a violation:")
        layout.addWidget(label)

        violation_input = QTextEdit()
        violation_input.setPlaceholderText("Describe the violation...")
        layout.addWidget(violation_input)

        log_button = QPushButton("Log Violation")
        log_button.clicked.connect(lambda: self.log_violation(violation_input.toPlainText()))
        layout.addWidget(log_button)

        visualize_button = QPushButton("Visualize Patterns")
        visualize_button.clicked.connect(self.visualize_patterns)
        layout.addWidget(visualize_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def log_violation(self, violation):
        print(f"Logged violation: {violation}")
        # Placeholder for logging logic

    def visualize_patterns(self):
        print("Visualizing violation patterns")
        # Placeholder for visualization logic

    def open_complaint_generator(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Complaint Generator")
        dialog.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()

        label = QLabel("Select a scenario to generate a complaint:")
        layout.addWidget(label)

        scenarios = QListWidget()
        scenarios.addItem("Eviction Notice")
        scenarios.addItem("Rent Increase")
        scenarios.addItem("Maintenance Issues")
        scenarios.addItem("Lease Violation")
        layout.addWidget(scenarios)

        generate_button = QPushButton("Generate Complaint")
        generate_button.clicked.connect(lambda: self.generate_complaint(scenarios.currentItem().text() if scenarios.currentItem() else "None"))
        layout.addWidget(generate_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def load_temp_todos(self):
        try:
            with open('temp_todo.json', 'r') as f:
                todos = json.load(f)
                for todo in todos:
                    self.todo_list.addItem(todo)
        except FileNotFoundError:
            pass

    def add_temp_todo(self):
        text = self.todo_input.text().strip()
        if text:
            self.todo_list.addItem(text)
            self.todo_input.clear()

    def save_temp_todos(self):
        todos = [self.todo_list.item(i).text() for i in range(self.todo_list.count())]
        with open('temp_todo.json', 'w') as f:
            json.dump(todos, f)

    def load_journal(self):
        try:
            with open('journal.json', 'r') as f:
                data = json.load(f)
                self.ws_input.setText(data.get('workspace', ''))
                self.notes_editor.setPlainText(data.get('notes', ''))
        except FileNotFoundError:
            pass

    def save_journal(self):
        data = {
            'workspace': self.ws_input.text(),
            'notes': self.notes_editor.toPlainText(),
            'timestamp': str(os.times())
        }
        with open('journal.json', 'w') as f:
            json.dump(data, f)
        # Sync via git if in repo
        try:
            os.system('git add journal.json temp_todo.json')
            os.system('git commit -m "Update journal and temp todos"')
        except Exception:
            pass

    def send_to_concierge(self):
        query = self.chat_input.text().strip()
        if not query:
            return
        self.chat_history.append(f"You: {query}")
        self.chat_input.clear()
        # Send to backend
        try:
            import requests
            response = requests.post("http://localhost:5000/api/copilot", json={"prompt": query}, timeout=10)
            if response.status_code == 200:
                result = response.json().get("response", "No response")
                self.chat_history.append(f"Concierge: {result}")
            else:
                self.chat_history.append("Concierge: Error communicating with AI.")
        except Exception as e:
            self.chat_history.append(f"Concierge: Error - {str(e)}")

    def send_to_local_ai(self):
        query = self.vault_chat_input.text().strip()
        if not query:
            return
        self.vault_chat_history.append(f"You: {query}")
        self.vault_chat_input.clear()
        # Send to Ollama
        try:
            import requests
            response = requests.post("http://localhost:11434/api/generate", json={"model": "llama3.2", "prompt": query, "stream": False}, timeout=30)
            if response.status_code == 200:
                result = response.json().get("response", "No response")
                self.vault_chat_history.append(f"Local AI: {result}")
            else:
                self.vault_chat_history.append("Local AI: Error communicating.")
        except Exception as e:
            self.vault_chat_history.append(f"Local AI: Error - {str(e)}")

    def update_local_model(self):
        try:
            import subprocess
            subprocess.run(["ollama", "pull", "llama3.2"], check=True)
            QMessageBox.information(self, "Update", "Local AI model updated!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update: {str(e)}")

    def update_external_settings(self):
        QMessageBox.information(self, "Update", "External AI settings updated (placeholder).")

    def train_ais(self):
        QMessageBox.information(self, "Train", "AIs trained (placeholder).")

    def spellcheck_notes(self):
        spell = SpellChecker()
        text = self.notes_editor.toPlainText()
        words = text.split()
        misspelled = spell.unknown(words)
        if misspelled:
            corrections = {}
            for word in misspelled:
                corrections[word] = spell.candidates(word)
            # Show dialog with corrections
            dialog = QDialog(self)
            dialog.setWindowTitle("Spellcheck Results")
            layout = QVBoxLayout()
            label = QLabel("Misspelled words and suggestions:")
            layout.addWidget(label)
            for word, sugg in corrections.items():
                layout.addWidget(QLabel(f"{word}: {', '.join(list(sugg)[:5])}"))  # Top 5 suggestions
            ok_btn = QPushButton("OK")
            ok_btn.clicked.connect(dialog.accept)
            layout.addWidget(ok_btn)
            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.information(self, "Spellcheck", "No misspellings found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SemptifyAppGUI()
    window.show()
    sys.exit(app.exec_())
