"""
gui_components.py

Reusable PyQt5 components for Semptify Desktop GUI.
These components are shared across all pages.

Usage:
    from gui_components import EvidenceCard, TimelineWidget, CaseOrganizer
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QGridLayout, QDialog, QFileDialog, QDateEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QTableWidget,
    QTableWidgetItem, QProgressBar, QSlider
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QDate, QSize, pyqtSignal, QTimer
from datetime import datetime, timedelta
import json
import os


class EvidenceCard(QFrame):
    """
    Displays a single piece of evidence (photo/video/audio).
    Used in Library page gallery.
    """
    clicked = pyqtSignal(dict)  # Signal when card is clicked

    def __init__(self, evidence_data):
        super().__init__()
        self.evidence_data = evidence_data
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                background: white;
            }
            QFrame:hover {
                border: 1px solid #0078d7;
                background: #f5f5f5;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(200, 200)

        # Thumbnail
        thumbnail_label = QLabel()
        if evidence_data.get('type') == 'photo':
            pixmap = QPixmap(evidence_data.get('path', ''))
            if not pixmap.isNull():
                scaled = pixmap.scaledToWidth(180, Qt.SmoothTransformation)
                thumbnail_label.setPixmap(scaled)
        elif evidence_data.get('type') == 'video':
            thumbnail_label.setText("🎥 VIDEO")
        elif evidence_data.get('type') == 'audio':
            thumbnail_label.setText("🎵 AUDIO")

        layout.addWidget(thumbnail_label)

        # Title
        title = QLabel(evidence_data.get('description', 'Unknown')[:30])
        title.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(title)

        # Date
        date_label = QLabel(evidence_data.get('timestamp', '')[:10])
        date_label.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(date_label)

        # Location (if GPS available)
        if evidence_data.get('location_lat'):
            location_label = QLabel(f"📍 GPS Tagged")
            location_label.setStyleSheet("color: #0078d7; font-size: 9px;")
            layout.addWidget(location_label)

    def mousePressEvent(self, event):
        self.clicked.emit(self.evidence_data)


class TimelineWidget(QWidget):
    """
    Visual timeline showing events chronologically.
    Used in Office page case organizer.
    """
    def __init__(self):
        super().__init__()
        self.events = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Timeline header
        header = QLabel("Case Timeline")
        header.setStyleSheet("font-size:14px; font-weight:bold;")
        layout.addWidget(header)

        # Scroll area for events
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.events_container = QWidget()
        self.events_layout = QVBoxLayout()
        self.events_container.setLayout(self.events_layout)
        scroll.setWidget(self.events_container)
        layout.addWidget(scroll)

    def add_event(self, date, title, description, event_type):
        """Add event to timeline"""
        event_widget = QFrame()
        event_widget.setFrameShape(QFrame.StyledPanel)
        event_widget.setStyleSheet("""
            QFrame {
                border-left: 4px solid #0078d7;
                padding: 8px;
                margin: 4px 0;
                background: #f9f9f9;
            }
        """)

        layout = QVBoxLayout()

        # Date and type
        header = QLabel(f"{date} - {event_type}")
        header.setStyleSheet("font-weight: bold; color: #0078d7;")
        layout.addWidget(header)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px;")
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 10px; color: #666;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        event_widget.setLayout(layout)
        self.events_layout.addWidget(event_widget)
        self.events.append({
            'date': date,
            'title': title,
            'description': description,
            'type': event_type
        })


class CourtPacketBuilder(QWidget):
    """
    Drag-and-drop interface for building court packets.
    Used in Office page.
    """
    def __init__(self):
        super().__init__()
        self.selected_evidence = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Court Packet Builder")
        title.setStyleSheet("font-size:14px; font-weight:bold;")
        layout.addWidget(title)

        # Available evidence (left side)
        available_label = QLabel("Available Evidence:")
        layout.addWidget(available_label)

        self.available_list = QTableWidget()
        self.available_list.setColumnCount(4)
        self.available_list.setHorizontalHeaderLabels(["Date", "Type", "Description", "Select"])
        layout.addWidget(self.available_list)

        # Selected evidence (right side)
        selected_label = QLabel("Court Packet Contents:")
        layout.addWidget(selected_label)

        self.selected_list = QTableWidget()
        self.selected_list.setColumnCount(3)
        self.selected_list.setHorizontalHeaderLabels(["Date", "Type", "Remove"])
        layout.addWidget(self.selected_list)

        # Action buttons
        button_layout = QHBoxLayout()

        generate_btn = QPushButton("Generate PDF")
        generate_btn.setStyleSheet("background: #0078d7; color: white; padding: 8px 16px; border-radius: 4px;")
        button_layout.addWidget(generate_btn)

        export_btn = QPushButton("Export to USB")
        export_btn.setStyleSheet("background: #107c10; color: white; padding: 8px 16px; border-radius: 4px;")
        button_layout.addWidget(export_btn)

        layout.addLayout(button_layout)

    def add_evidence(self, evidence_item):
        """Add evidence to packet"""
        row = self.selected_list.rowCount()
        self.selected_list.insertRow(row)

        self.selected_list.setItem(row, 0, QTableWidgetItem(evidence_item.get('date', '')))
        self.selected_list.setItem(row, 1, QTableWidgetItem(evidence_item.get('type', '')))

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.selected_list.removeRow(row))
        self.selected_list.setCellWidget(row, 2, remove_btn)

        self.selected_evidence.append(evidence_item)


class StatuteCalculator(QWidget):
    """
    Calculates statute of limitations and shows countdown.
    Used in Tools page.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Statute of Limitations Calculator")
        title.setStyleSheet("font-size:14px; font-weight:bold;")
        layout.addWidget(title)

        # Action type selector
        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("Action Type:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems([
            "Eviction Notice",
            "Complaint Filed",
            "Service of Process",
            "Appeal Deadline",
            "Payment Claim"
        ])
        action_layout.addWidget(self.action_combo)
        layout.addLayout(action_layout)

        # Jurisdiction selector
        jurisdiction_layout = QHBoxLayout()
        jurisdiction_layout.addWidget(QLabel("Jurisdiction:"))
        self.jurisdiction_combo = QComboBox()
        self.jurisdiction_combo.addItems([
            "California",
            "New York",
            "Texas",
            "Federal"
        ])
        jurisdiction_layout.addWidget(self.jurisdiction_combo)
        layout.addLayout(jurisdiction_layout)

        # Start date picker
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Start Date:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.start_date)
        layout.addLayout(date_layout)

        # Calculate button
        calc_btn = QPushButton("Calculate")
        calc_btn.setStyleSheet("background: #0078d7; color: white; padding: 8px 16px; border-radius: 4px;")
        calc_btn.clicked.connect(self.calculate)
        layout.addWidget(calc_btn)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size:16px; font-weight:bold; color: #0078d7; margin-top: 16px;")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        # Countdown progress bar
        self.countdown = QProgressBar()
        self.countdown.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                height: 25px;
                background: white;
            }
            QProgressBar::chunk {
                background: #0078d7;
            }
        """)
        layout.addWidget(self.countdown)

        layout.addStretch()

    def calculate(self):
        """Calculate statute expiration"""
        action = self.action_combo.currentText()
        jurisdiction = self.jurisdiction_combo.currentText()
        start_date = self.start_date.date().toPyDate()

        # Statute durations (simplified - fetch from backend in real app)
        durations = {
            ("Eviction Notice", "California"): 30,
            ("Complaint Filed", "California"): 1095,  # 3 years
            ("Service of Process", "California"): 90,
            ("Appeal Deadline", "California"): 60,
        }

        key = (action, jurisdiction)
        days = durations.get(key, 365)
        expiration = start_date + timedelta(days=days)
        today = datetime.now().date()
        remaining = (expiration - today).days

        percentage = max(0, min(100, int(100 * remaining / days)))
        self.countdown.setValue(percentage)

        color = "#107c10" if remaining > 14 else "#ffb900" if remaining > 7 else "#d13438"
        self.result_label.setText(
            f"<span style='color:{color}'>⏰ {remaining} days remaining</span><br>"
            f"Expires: {expiration.strftime('%B %d, %Y')}"
        )


class AdminConfigPanel(QWidget):
    """
    Admin configuration panel for system settings.
    Used in Admin page.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("System Configuration")
        title.setStyleSheet("font-size:14px; font-weight:bold;")
        layout.addWidget(title)

        # Config sections
        config_layout = QGridLayout()

        # Statute durations
        config_layout.addWidget(QLabel("Eviction Notice Duration (days):"), 0, 0)
        self.eviction_spin = QSpinBox()
        self.eviction_spin.setValue(30)
        config_layout.addWidget(self.eviction_spin, 0, 1)

        config_layout.addWidget(QLabel("Complaint Duration (days):"), 1, 0)
        self.complaint_spin = QSpinBox()
        self.complaint_spin.setValue(1095)
        config_layout.addWidget(self.complaint_spin, 1, 1)

        # Weather thresholds
        config_layout.addWidget(QLabel("Severe Wind Speed (mph):"), 2, 0)
        self.wind_spin = QSpinBox()
        self.wind_spin.setValue(35)
        config_layout.addWidget(self.wind_spin, 2, 1)

        config_layout.addWidget(QLabel("Weather Visibility (miles):"), 3, 0)
        self.visibility_spin = QDoubleSpinBox()
        self.visibility_spin.setValue(0.5)
        config_layout.addWidget(self.visibility_spin, 3, 1)

        # Notification settings
        config_layout.addWidget(QLabel("Alert Days Before Expiry:"), 4, 0)
        self.alert_spin = QSpinBox()
        self.alert_spin.setValue(30)
        config_layout.addWidget(self.alert_spin, 4, 1)

        layout.addLayout(config_layout)

        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.setStyleSheet("background: #0078d7; color: white; padding: 8px 16px; border-radius: 4px;")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)

        layout.addStretch()

    def save_config(self):
        """Save configuration to backend"""
        config = {
            'statute_durations': {
                'eviction_notice': self.eviction_spin.value(),
                'complaint': self.complaint_spin.value()
            },
            'weather_settings': {
                'wind_threshold': self.wind_spin.value(),
                'visibility_threshold': self.visibility_spin.value()
            },
            'notification_settings': {
                'alert_days': self.alert_spin.value()
            }
        }
        # In real app, POST to /admin/ledger/config/update
        print(f"Saved config: {json.dumps(config, indent=2)}")


# Export all components
__all__ = [
    'EvidenceCard',
    'TimelineWidget',
    'CourtPacketBuilder',
    'StatuteCalculator',
    'AdminConfigPanel'
]
