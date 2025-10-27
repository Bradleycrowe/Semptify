import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QGraphicsDropShadowEffect, QLineEdit, QComboBox, QStackedWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import hashlib
import secrets
from datetime import datetime, timedelta

# Create a Flask app instance
app = Flask(__name__)

# Placeholder for backend integration
@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'POST':
        data = request.json
        # Process the data and integrate with backend
        return {'status': 'success', 'message': 'Data processed successfully'}
    return {'status': 'success', 'data': 'Sample data from backend'}

# Example integration with core pages
@app.route('/dashboard')
def dashboard():
    # Fetch data from backend and render dashboard
    data = {'user': 'John Doe', 'notifications': 5}
    return render_template('dashboard.html', data=data)

class SemptifyAppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semptify App GUI")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon("static/icons/Semptfylogo.svg"))
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Top Bar
        top_bar = QFrame()
        top_bar.setFrameShape(QFrame.StyledPanel)
        top_bar.setStyleSheet("background: #fff; border-bottom: 1px solid #e9eef6; width: 100%;")
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("static/icons/Semptfylogo.svg")
        if pixmap.isNull():
            logo_label.setText("Semptify")
        else:
            logo_label.setPixmap(pixmap.scaled(192, 192, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        # Use the correct alignment type for the logo label
        top_bar_layout.addWidget(logo_label, alignment=int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop))

        # Nav Links
        nav_frame = QFrame()
        nav_layout = QHBoxLayout()
        nav_frame.setLayout(nav_layout)
        nav_links = ["Home", "Library", "Office", "Tools", "Vault", "Help"]
        for link in nav_links:
            btn = QPushButton(link)
            btn.setStyleSheet(
                "background: none; border: none; font-size: 16px; color: #222; padding: 0 16px; letter-spacing: 0.6px; font-style: italic;"
            )
            btn.clicked.connect(lambda checked, group=link: self.set_active_modules(group))
            nav_layout.addWidget(btn)
        # Correct alignment attribute
        top_bar_layout.addWidget(nav_frame, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Adjust the alignment of the text line in the top bar
        nav_frame.setContentsMargins(0, 0, 0, int(top_bar.height() * 0.25))

        # Adjust top bar height to match logo height
        top_bar.setMinimumHeight(192)

        layout.addWidget(top_bar)

        # Remove or hide the 'Button Box' text
        button_box_label = QLabel("Button Box:")
        button_box_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        button_box_label.setVisible(False)
        layout.addWidget(button_box_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Main Content Label
        content_label = QLabel("Main Content:")
        content_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(content_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Main Content Placeholder
        main_content = QLabel("Semptify App GUI - Main Content Area")
        main_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_content.setStyleSheet("font-size: 22px; color: #555; margin-top: 60px;")
        layout.addWidget(main_content)

        # Set the background color of the button box to match the top bar
        # Add drop shadows to buttons
        shadow_effect1 = QGraphicsDropShadowEffect()
        shadow_effect1.setBlurRadius(10)
        shadow_effect1.setOffset(2, 2)
        # button1.setGraphicsEffect(shadow_effect1)

        shadow_effect2 = QGraphicsDropShadowEffect()
        shadow_effect2.setBlurRadius(10)
        shadow_effect2.setOffset(2, 2)
        # button2.setGraphicsEffect(shadow_effect2)

        # Add Office module buttons
        office_button = QPushButton("Office Module")
        office_button.clicked.connect(self.open_office_page)
        # button_box_layout.addWidget(office_button)

        create_room_button = QPushButton("Create Room")
        create_room_button.clicked.connect(self.create_room)
        # button_box_layout.addWidget(create_room_button)

        list_rooms_button = QPushButton("List Rooms")
        list_rooms_button.clicked.connect(self.list_rooms)
        # button_box_layout.addWidget(list_rooms_button)

        # Add document-related buttons
        upload_document_button = QPushButton("Upload Document")
        upload_document_button.clicked.connect(self.upload_document)
        # button_box_layout.addWidget(upload_document_button)

        lock_document_button = QPushButton("Lock Document")
        lock_document_button.clicked.connect(self.lock_document)
        # button_box_layout.addWidget(lock_document_button)

        annotate_document_button = QPushButton("Annotate Document")
        annotate_document_button.clicked.connect(self.annotate_document)
        # button_box_layout.addWidget(button_box_layout.addWidget(annotate_document_button)

        # Add navigation for law notes
        law_notes_button = QPushButton("Law Notes")
        law_notes_button.clicked.connect(self.open_law_notes)
        # button_box_layout.addWidget(law_notes_button)

        # Add navigation for law notes modules
        self.add_navigation_option('Attorney Trail', '/law_notes/attorney_trail')
        self.add_navigation_option('Complaint Templates', '/law_notes/complaint_template')

        # Add navigation for new modules
        public_exposure_button = QPushButton("Public Exposure Module")
        public_exposure_button.clicked.connect(lambda: self.open_navigation_page('/public_exposure'))
        # button_box_layout.addWidget(public_exposure_button)

        enforcement_button = QPushButton("Enforcement Module")
        enforcement_button.clicked.connect(lambda: self.open_navigation_page('/enforcement'))
        # button_box_layout.addWidget(enforcement_button)

        # Remove the lowest box (dynamic content area)
        # layout.removeWidget(self.dynamic_content)
        # self.dynamic_content.deleteLater()
        # self.dynamic_content = None

        # Add a control bar for module settings and inputs
        self.control_bar = QFrame()
        self.control_bar.setFrameShape(QFrame.StyledPanel)
        self.control_bar.setStyleSheet("background: #f7f7f7; border-bottom: 1px solid #ccc;")
        self.control_bar_layout = QVBoxLayout()
        self.control_bar.setLayout(self.control_bar_layout)
        layout.addWidget(self.control_bar, alignment=Qt.AlignmentFlag.AlignTop)

        # Add module selector
        self.module_selector = QPushButton("Select Module")
        self.module_selector.setStyleSheet("background: #007bff; color: white; padding: 8px; border-radius: 4px;")
        self.module_selector.clicked.connect(self.show_module_options)
        self.control_bar_layout.addWidget(self.module_selector)

        # Add dynamic input area
        self.input_area = QFrame()
        self.input_area.setFrameShape(QFrame.StyledPanel)
        self.input_area.setStyleSheet("background: #fff; border: 1px solid #ddd; padding: 8px;")
        self.input_area_layout = QVBoxLayout()
        self.input_area.setLayout(self.input_area_layout)
        self.control_bar_layout.addWidget(self.input_area)

        # Add output buttons
        self.output_buttons = QFrame()
        self.output_buttons.setFrameShape(QFrame.StyledPanel)
        self.output_buttons.setStyleSheet("background: #fff; border: 1px solid #ddd; padding: 8px;")
        self.output_buttons_layout = QHBoxLayout()
        self.output_buttons.setLayout(self.output_buttons_layout)
        self.control_bar_layout.addWidget(self.output_buttons)

        # Remove the left sidebar and its widgets
        # layout.removeWidget(self.left_sidebar)
        # self.left_sidebar.deleteLater()
        # self.left_sidebar = None

        # Remove the active module label and its layout
        # self.left_sidebar_layout.removeWidget(self.active_module_label)
        # self.active_module_label.deleteLater()
        # self.active_module_label = None

        # Remove the right sidebar layout and its widgets
        # self.right_sidebar_layout.addWidget(lock_document_button)
        # self.right_sidebar_layout.addWidget(annotate_document_button)

        # Adjust the right button container bar to align to the top
        # self.right_sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Make the right button smaller
        lock_document_button.setFixedSize(100, 30)
        annotate_document_button.setFixedSize(100, 30)

        # Add a footer with a scrolling disclaimer
        footer = QFrame()
        footer.setFrameShape(QFrame.StyledPanel)
        footer.setStyleSheet("background: #f7f7f7; border-top: 1px solid #ccc; padding: 8px;")
        footer_layout = QHBoxLayout()
        footer.setLayout(footer_layout)

        disclaimer_label = QLabel("Not legal advice")
        disclaimer_label.setStyleSheet("font-size: 12px; color: #888;")
        footer_layout.addWidget(disclaimer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(footer, alignment=Qt.AlignmentFlag.AlignBottom)

        # Create a stacked widget to manage pages
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        # Add core pages
        self.home_page = QWidget()
        self.register_page = QWidget()
        self.vault_page = QWidget()
        self.admin_page = QWidget()
        self.library_page = QWidget()  # Add library page

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.register_page)
        self.pages.addWidget(self.vault_page)
        self.pages.addWidget(self.admin_page)
        self.pages.addWidget(self.library_page)  # Add library page to stack

        # Navigation buttons
        self.nav_buttons = QVBoxLayout()
        self.home_button = QPushButton("Home")
        self.register_button = QPushButton("Register")
        self.vault_button = QPushButton("Vault")
        self.admin_button = QPushButton("Admin")
        self.library_button = QPushButton("Library")  # Add library button

        self.nav_buttons.addWidget(self.home_button)
        self.nav_buttons.addWidget(self.register_button)
        self.nav_buttons.addWidget(self.vault_button)
        self.nav_buttons.addWidget(self.admin_button)
        self.nav_buttons.addWidget(self.library_button)  # Add library button to layout

        # Connect buttons to pages
        self.home_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.home_page))
        self.register_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.register_page))
        self.vault_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.vault_page))
        self.admin_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.admin_page))
        self.library_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.library_page))  # Connect library button

        # Set up the layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.nav_buttons)
        main_layout.addWidget(self.pages)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_office_page(self):
        pass

    def create_room(self):
        pass

    def list_rooms(self):
        pass

    def upload_document(self):
        pass

    def lock_document(self):
        pass

    def annotate_document(self):
        pass

    def open_law_notes(self):
        pass

    def add_navigation_option(self, name, path):
        pass

    def open_navigation_page(self, path):
        pass

    def show_module_options(self):
        pass

    def set_active_modules(self, group):
        # Functionality to change the active set of modules based on the clicked navigation link
        print(f"Active module group set to: {group}")
        # Add logic here to update the active modules in the GUI


class UserManager:
    def __init__(self):
        self.users = {}  # Store user data in memory for simplicity

    def generate_user_id(self):
        return secrets.token_hex(8)  # Generate a unique 16-character user ID

    def generate_token(self):
        return secrets.token_hex(16)  # Generate a secure 32-character token

    def hash_token(self, token):
        return hashlib.sha256(token.encode()).hexdigest()

    def create_user(self, user_data):
        user_id = self.generate_user_id()
        token = self.generate_token()
        hashed_token = self.hash_token(token)

        self.users[user_id] = {
            'data': user_data,
            'token': hashed_token,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=24)  # Token expires in 24 hours
        }

        return user_id, token

    def validate_token(self, user_id, token):
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        hashed_token = self.hash_token(token)

        if user['token'] != hashed_token:
            return False

        if datetime.now() > user['expires_at']:
            return False

        return True

class DocumentVault:
    def __init__(self):
        self.documents = {}  # Store documents with their metadata

    def add_document(self, user_token, document_id, document_data):
        if user_token not in self.documents:
            self.documents[user_token] = []

        self.documents[user_token].append({
            'document_id': document_id,
            'data': document_data,
            'uploaded_at': datetime.now()
        })

    def get_documents(self, user_token):
        return self.documents.get(user_token, [])

class AnonymousInteraction:
    def __init__(self):
        self.interactions = []  # Store interaction logs

    def log_interaction(self, user_token, entity, action, details):
        self.interactions.append({
            'user_token': user_token,
            'entity': entity,
            'action': action,
            'details': details,
            'timestamp': datetime.now()
        })

    def get_interactions(self, user_token):
        return [interaction for interaction in self.interactions if interaction['user_token'] == user_token]

class BreakGlassProcedure:
    def __init__(self, log_file="logs/breakglass.log"):
        self.log_file = log_file

    def trigger_break_glass(self, admin_token, reason):
        if not self._is_valid_token(admin_token):
            raise ValueError("Invalid admin token")

        self._log_break_glass(admin_token, reason)
        print("Break-glass procedure triggered. Admin access granted.")

    def _is_valid_token(self, token):
        # Placeholder for token validation logic
        return token == "emergency_admin_token"

    def _log_break_glass(self, admin_token, reason):
        with open(self.log_file, "a") as log:
            log.write(f"Break-glass triggered by token: {admin_token}\n")
            log.write(f"Reason: {reason}\n")
            log.write(f"Timestamp: {datetime.now()}\n\n")

# Example usage
if __name__ == "__main__":
    user_manager = UserManager()

    # Create a new user
    user_id, token = user_manager.create_user({'name': 'John Doe', 'email': 'john@example.com'})
    print("User ID:", user_id)
    print("Token:", token)

    # Validate the token
    is_valid = user_manager.validate_token(user_id, token)
    print("Is token valid?", is_valid)

    vault = DocumentVault()

    # Add a document
    user_token = "example_user_token"
    document_id = "doc_12345"
    document_data = "Sample document content"

    vault.add_document(user_token, document_id, document_data)

    # Retrieve documents for the user
    user_documents = vault.get_documents(user_token)
    print("User Documents:", user_documents)

    interaction_manager = AnonymousInteraction()

    # Log an interaction
    user_token = "example_user_token"
    entity = "Court"
    action = "Submit Document"
    details = "Submitted document ID doc_12345"

    interaction_manager.log_interaction(user_token, entity, action, details)

    # Retrieve interactions for the user
    user_interactions = interaction_manager.get_interactions(user_token)
    print("User Interactions:", user_interactions)

    break_glass = BreakGlassProcedure()

    try:
        break_glass.trigger_break_glass("emergency_admin_token", "System outage")
    except ValueError as e:
        print(e)

    qt_app = QApplication(sys.argv)
    window = SemptifyAppGUI()
    window.show()
    sys.exit(qt_app.exec_())
