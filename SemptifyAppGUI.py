import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

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
        top_bar.setStyleSheet("background: #fff; border-bottom: 1px solid #e9eef6;")
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("static/icons/Semptfylogo.svg")
        if pixmap.isNull():
            logo_label.setText("Semptify")
        else:
            logo_label.setPixmap(pixmap.scaled(192, 192, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        top_bar_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Nav Links
        nav_frame = QFrame()
        nav_layout = QHBoxLayout()
        nav_frame.setLayout(nav_layout)
        nav_links = ["Home", "Library", "Office", "Tools", "Vault", "Help"]
        for link in nav_links:
            btn = QPushButton(link)
            btn.setStyleSheet("background: none; border: none; font-size: 16px; color: #222; padding: 0 16px;")
            nav_layout.addWidget(btn)
        # Correct alignment attribute
        top_bar_layout.addWidget(nav_frame, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Button Box
        button_box = QFrame()
        button_box.setStyleSheet("background: #f5f7fb; border-radius: 8px; border: 1px solid #e9eef6;")
        button_box_layout = QVBoxLayout()
        button_box.setLayout(button_box_layout)
        button1 = QPushButton("New User Registration")
        button2 = QPushButton("User Log In")
        # Remove tooltips from buttons
        button1.setToolTip("")
        button2.setToolTip("")
        button_box_layout.addWidget(button1)

        # Align Button #1 to the top center with a single alignment flag
        button1_layout = QVBoxLayout()
        button1_layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignHCenter)
        button_box_layout.addLayout(button1_layout)

        # Separate Button #2
        button2_layout = QVBoxLayout()
        button2_layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignHCenter)
        button_box_layout.addLayout(button2_layout)

        # Correct alignment attributes with proper flag combination
        top_bar_layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignRight)

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
        button_box.setStyleSheet("background-color: #f0f0f0;")

        # Add drop shadows to buttons
        shadow_effect1 = QGraphicsDropShadowEffect()
        shadow_effect1.setBlurRadius(10)
        shadow_effect1.setOffset(2, 2)
        button1.setGraphicsEffect(shadow_effect1)

        shadow_effect2 = QGraphicsDropShadowEffect()
        shadow_effect2.setBlurRadius(10)
        shadow_effect2.setOffset(2, 2)
        button2.setGraphicsEffect(shadow_effect2)

        # Add Office module buttons
        office_button = QPushButton("Office Module")
        office_button.clicked.connect(self.open_office_page)
        button_box_layout.addWidget(office_button)

        create_room_button = QPushButton("Create Room")
        create_room_button.clicked.connect(self.create_room)
        button_box_layout.addWidget(create_room_button)

        list_rooms_button = QPushButton("List Rooms")
        list_rooms_button.clicked.connect(self.list_rooms)
        button_box_layout.addWidget(list_rooms_button)

        # Add document-related buttons
        upload_document_button = QPushButton("Upload Document")
        upload_document_button.clicked.connect(self.upload_document)
        button_box_layout.addWidget(upload_document_button)

        lock_document_button = QPushButton("Lock Document")
        lock_document_button.clicked.connect(self.lock_document)
        button_box_layout.addWidget(lock_document_button)

        annotate_document_button = QPushButton("Annotate Document")
        annotate_document_button.clicked.connect(self.annotate_document)
        button_box_layout.addWidget(annotate_document_button)

    def open_office_page(self):
        # Open the Office page in the default browser
        import webbrowser
        webbrowser.open("http://localhost:5000/office")

    # Update create_room to use backend route
    def create_room(self):
        import requests
        response = requests.post("http://localhost:5000/api/rooms/create", json={"type": "open", "expires_in": 3600})
        if response.status_code == 200:
            room = response.json()
            print("Room created:", room)
        else:
            print("Failed to create room:", response.text)

    # Update list_rooms to fetch from backend
    def list_rooms(self):
        import requests
        response = requests.get("http://localhost:5000/api/rooms")
        if response.status_code == 200:
            rooms = response.json()
            print("Rooms:", rooms)
        else:
            print("Failed to list rooms:", response.text)

    # Update upload_document to use backend route
    def upload_document(self):
        import requests
        response = requests.post("http://localhost:5000/api/documents/upload/init", json={"filename": "example.txt", "sha256": "dummyhash"})
        if response.status_code == 200:
            upload_info = response.json()
            print("Document upload initialized:", upload_info)
        else:
            print("Failed to initialize document upload:", response.text)

    # Update lock_document to use backend route
    def lock_document(self):
        import requests
        doc_id = "example-doc-id"  # Replace with actual document ID
        response = requests.post(f"http://localhost:5000/api/documents/{doc_id}/lock")
        if response.status_code == 200:
            print("Document locked:", response.json())
        else:
            print("Failed to lock document:", response.text)

    # Update annotate_document to use backend route
    def annotate_document(self):
        import requests
        doc_id = "example-doc-id"  # Replace with actual document ID
        response = requests.post(f"http://localhost:5000/api/documents/{doc_id}/annotate", json={"text": "Sample annotation", "timecode": 123})
        if response.status_code == 200:
            print("Document annotated:", response.json())
        else:
            print("Failed to annotate document:", response.text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SemptifyAppGUI()
    window.show()
    sys.exit(app.exec_())
