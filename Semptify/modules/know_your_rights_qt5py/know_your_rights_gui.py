import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QTextEdit, QVBoxLayout, QHBoxLayout

class KnowYourRightsModal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Know Your Rights')
        self.setGeometry(100, 100, 600, 400)

        # Help text
        help_label = QLabel('Select a situation to learn your rights and generate a complaint.')
        help_label.setStyleSheet('font-size: 14px; color: #333;')

        # Scenario dropdown
        self.scenario_box = QComboBox()
        self.scenario_box.addItems([
            'Landlord entered without notice',
            'Rent raised after complaint',
            'Harassment or threats',
            'Utility shutoff',
            'Eviction notice received'
        ])

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setPlaceholderText('Your rights summary and complaint template will appear here.')

        # Buttons
        generate_button = QPushButton('Generate Rights Summary')
        escalate_button = QPushButton('Escalate Issue')
        graphics_button = QPushButton('View Legal Graphic')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(help_label)
        layout.addWidget(self.scenario_box)
        layout.addWidget(generate_button)
        layout.addWidget(escalate_button)
        layout.addWidget(graphics_button)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KnowYourRightsModal()
    window.show()
    sys.exit(app.exec_())
