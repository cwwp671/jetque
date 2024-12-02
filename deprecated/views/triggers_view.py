# jetque/src/views/triggers_view.py

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class TriggersView(QWidget):
    def __init__(self):
        logging.debug("Here")
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        logging.debug("Here")
        layout = QVBoxLayout()
        label = QLabel("Trigger View will be here and feature Trigger Configuration")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
