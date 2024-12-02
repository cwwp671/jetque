# jetque/src/views/home_view.py

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from config.config_loader import load_config, save_config

class HomeView(QWidget):
    def __init__(self):
        logging.debug("Here")
        super().__init__()
        self.config_path = "jetque/config/config.json"
        self.config_data = load_config(self.config_path)
        self.setup_ui()

    def setup_ui(self):
        logging.debug("Here")
        layout = QVBoxLayout()

        # Main Title Label with White Space
        label = QLabel("Home View Settings")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        # layout.addSpacing(10)  # Add white space to make it cleaner

        # Log Directory Section (Horizontal layout)
        self.create_divider(layout)
        log_layout = QHBoxLayout()
        self.log_dir_status = QLabel(f"Log Directory set to: {self.config_data.get('log_directory', '')}")
        log_dir_button = QPushButton("Select Log Directory")
        self.style_button(log_dir_button)
        log_dir_button.clicked.connect(self.select_log_directory)
        log_layout.addWidget(log_dir_button)
        log_layout.addWidget(self.log_dir_status)
        layout.addLayout(log_layout)
        # layout.addSpacing(10)  # More spacing between sections

        # DBG File Section
        self.create_divider(layout)
        dbg_layout = QHBoxLayout()
        self.dbg_file_status = QLabel(f"DBG File set to: {self.config_data.get('dbg_file', '')}")
        dbg_file_button = QPushButton("Select DBG File (.txt)")
        self.style_button(dbg_file_button)
        dbg_file_button.clicked.connect(self.select_dbg_file)
        dbg_layout.addWidget(dbg_file_button)
        dbg_layout.addWidget(self.dbg_file_status)
        layout.addLayout(dbg_layout)
        # layout.addSpacing(10)

        # Char File Section
        self.create_divider(layout)
        char_layout = QHBoxLayout()
        self.char_file_status = QLabel(f"Char File set to: {self.config_data.get('char_file', '')}")
        char_file_button = QPushButton("Select Char File (.txt)")
        self.style_button(char_file_button)
        char_file_button.clicked.connect(self.select_char_file)
        char_layout.addWidget(char_file_button)
        char_layout.addWidget(self.char_file_status)
        layout.addLayout(char_layout)
        # layout.addSpacing(10)

        self.setLayout(layout)

    def create_divider(self, layout):
        """Adds a visual divider between sections."""
        logging.debug("Here")
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

    def style_button(self, button):
        """Applies clean, modern button styling."""
        logging.debug("Here")
        button.setFixedWidth(180)  # Reduced width for buttons
        button.setStyleSheet("""
            QPushButton {
                border: 1px solid #cccccc;
                padding: 6px;
                background-color: #f7f7f7;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
        """)

    def select_log_directory(self):
        logging.debug("Here")
        log_directory = QFileDialog.getExistingDirectory(
            self,
            "Select Log Directory",
            self.config_data.get('log_directory', '')
        )
        if log_directory:
            self.config_data['log_directory'] = log_directory
            save_config(self.config_data, self.config_path)
            self.log_dir_status.setText(f"Log Directory set to: {log_directory}")

    def select_dbg_file(self):
        logging.debug("Here")
        log_directory = self.config_data.get('log_directory', '')
        dbg_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select DBG File",
            log_directory,
            "Text Files (*.txt)"
        )
        if dbg_file:
            self.config_data['dbg_file'] = dbg_file
            save_config(self.config_data, self.config_path)
            self.dbg_file_status.setText(f"DBG File set to: {dbg_file}")

    def select_char_file(self):
        logging.debug("Here")
        log_directory = self.config_data.get('log_directory', '')
        char_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Char File",
            log_directory,
            "Text Files (*.txt)"
        )
        if char_file:
            self.config_data['char_file'] = char_file
            save_config(self.config_data, self.config_path)
            self.char_file_status.setText(f"Char File set to: {char_file}")
