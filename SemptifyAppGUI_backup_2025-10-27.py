import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QLineEdit, QComboBox, QStackedWidget
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class SemptifyAppGUI(QMainWindow):
    def show_module_group_page(self):
        # Create a new QWidget for the grouped module page
        group_page = QWidget()
        layout = QVBoxLayout()
        group_page.setLayout(layout)

        # Title
        title = QLabel("Module Group: Rights & Violations")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(title)

        # Rights Scenario Explorer section
        rights_label = QLabel("Rights Scenario Explorer")
        rights_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 12px;")
        layout.addWidget(rights_label)

        rights_text = QLineEdit()
        rights_text.setPlaceholderText("Describe your scenario...")
        layout.addWidget(rights_text)

        rights_dropdown = QComboBox()
        rights_dropdown.addItems(["Eviction", "Rent Increase", "Repair Issue", "Other"])
        layout.addWidget(rights_dropdown)

        rights_button = QPushButton("Trigger Rights Modal")
        rights_button.clicked.connect(self.open_rights_scenario_explorer)
        layout.addWidget(rights_button)

        # Violation Pattern Mapper section
        violation_label = QLabel("Violation Pattern Mapper")
        violation_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 24px;")
        layout.addWidget(violation_label)

        violation_text = QLineEdit()
        violation_text.setPlaceholderText("Log a violation...")
        layout.addWidget(violation_text)

        violation_dropdown = QComboBox()
        violation_dropdown.addItems(["Noise", "Harassment", "Unsafe Conditions", "Other"])
        layout.addWidget(violation_dropdown)

        violation_button = QPushButton("Trigger Violation Modal")
        violation_button.clicked.connect(self.open_violation_pattern_mapper)
        layout.addWidget(violation_button)

        # Add the group page to the stacked widget and show it
        self.pages.addWidget(group_page)
        self.pages.setCurrentWidget(group_page)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semptify App GUI")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon("static/icons/Semptfylogo.svg"))
        self.initUI()

    def initUI(self):
        # Main window setup
        central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Top Bar (unchanged)
        top_bar = QFrame()
        top_bar.setFrameShape(QFrame.StyledPanel)
        top_bar.setStyleSheet("background: #fff; border-bottom: 1px solid #e9eef6; width: 100%;")
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)
        logo_label = QLabel()
        pixmap = QPixmap("static/icons/Semptfylogo.svg")
        logo_label.setPixmap(pixmap)
        top_bar_layout.addWidget(logo_label)

        self.main_layout.addWidget(top_bar)  # Use self.main_layout

        # Add a button to open the grouped module page for quick access
        group_page_button = QPushButton("Rights & Violations Group")
        group_page_button.setStyleSheet("background: #28a745; color: white; font-weight: bold; margin: 8px 0;")
        group_page_button.clicked.connect(self.show_grouped_modules)
        self.main_layout.addWidget(group_page_button)

        # Stacked widget for pages
        self.pages = QStackedWidget()
        self.main_layout.addWidget(self.pages)

        # Add core pages
        self.home_page = QWidget()
        self.register_page = QWidget()
        self.vault_page = QWidget()
        self.admin_page = QWidget()
        self.library_page = QWidget()
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.register_page)
        self.pages.addWidget(self.vault_page)
        self.pages.addWidget(self.admin_page)
        self.pages.addWidget(self.library_page)

        # Add Office module buttons
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
