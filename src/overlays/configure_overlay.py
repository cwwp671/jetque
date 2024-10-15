# jetque/src/overlays/configure_overlay.py

from PyQt6.QtCore import Qt
from src.overlays.overlay import Overlay

class ConfigureOverlay(Overlay):
    def __init__(self, name, overlay_data):
        super().__init__(name, overlay_data)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Set a semi-transparent black background
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
