# jetque/src/views/overlays_view.py

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from src.overlays.overlay_manager import OverlayManager
from config.config_loader import load_config, save_config

class OverlaysView(QWidget):
    def __init__(self, overlay_manager):
        logging.debug("Initializing OverlaysView")
        super().__init__()
        self.overlay_manager = overlay_manager
        self.config_data = load_config()
        self.setup_ui()
        self.load_overlays_from_config()

    def setup_ui(self):
        logging.debug("Setting up UI for OverlaysView")
        layout = QVBoxLayout()
        # Label
        label = QLabel("Manage Overlays")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        # Overlays list
        self.overlays_list = QListWidget()
        layout.addWidget(self.overlays_list)
        # Buttons
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create Overlay")
        self.delete_button = QPushButton("Delete Selected Overlay")
        self.toggle_mode_button = QPushButton("Toggle Configure Mode")
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.toggle_mode_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        # Connect buttons to functions
        self.create_button.clicked.connect(self.create_overlay)
        self.delete_button.clicked.connect(self.delete_selected_overlay)
        self.toggle_mode_button.clicked.connect(self.toggle_configure_mode)

    def load_overlays_from_config(self):
        logging.debug("Loading overlays from config")
        overlays_data = self.config_data.get('overlays', {})
        if not overlays_data:
            # Create default overlays
            default_overlays = ['Incoming', 'Outgoing', 'Notifications']
            for name in default_overlays:
                # Get default overlay data from config if available
                overlay_config = self.config_data.get('scroll_areas', {}).get(name.lower(), {})
                overlay_data = {
                    'position': [
                        int(overlay_config.get('position', [100, 100])[0]),
                        int(overlay_config.get('position', [100, 100])[1])
                    ],
                    'width': int(overlay_config.get('width', 300)),
                    'height': int(overlay_config.get('height', 200))
                }
                self.overlay_manager.create_overlay(name, overlay_data)
                self.overlays_list.addItem(name)
                # Save to config
                self.config_data.setdefault('overlays', {})[name] = overlay_data
            save_config(self.config_data)
        else:
            for name, data in overlays_data.items():
                self.overlay_manager.create_overlay(name, data)
                self.overlays_list.addItem(name)

    def create_overlay(self):
        logging.debug("Creating a new overlay")
        # Prompt user for overlay name
        name, ok = QInputDialog.getText(self, 'Create Overlay', 'Enter overlay name:')
        if ok and name:
            if name in self.overlay_manager.overlays:
                QMessageBox.warning(self, "Duplicate Name", "An overlay with that name already exists.")
                return
            overlay_data = {
                'position': [100, 100],
                'width': 300,
                'height': 200
            }
            self.overlay_manager.create_overlay(name, overlay_data)
            self.overlays_list.addItem(name)
            self.config_data.setdefault('overlays', {})[name] = overlay_data
            save_config(self.config_data)
        else:
            logging.debug("Overlay creation canceled or empty name provided.")

    def delete_selected_overlay(self):
        logging.debug("Deleting selected overlay")
        selected_items = self.overlays_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an overlay to delete.")
            return
        for item in selected_items:
            name = item.text()
            self.overlay_manager.delete_overlay(name)
            self.overlays_list.takeItem(self.overlays_list.row(item))
            del self.config_data['overlays'][name]
        save_config(self.config_data)

    def toggle_configure_mode(self):
        logging.debug("Toggling configure mode for all overlays")
        for name in self.overlay_manager.overlays.keys():
            logging.debug(f"Overlay Keys Name: {name}")
            self.overlay_manager.toggle_mode(name)
        # No need to update config here as positions and sizes are updated in real-time
