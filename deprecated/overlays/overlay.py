from PyQt6.QtWidgets import QWidget, QVBoxLayout


class Overlay(QWidget):
    def __init__(self, name, overlay_data, overlay_manager):
        super().__init__()
        self.name = name
        self.overlay_data = overlay_data
        self.overlay_manager = overlay_manager  # Reference to overlay manager
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setup_overlay()

    def setup_overlay(self):
        self.setGeometry(
            self.overlay_data['position'][0],
            self.overlay_data['position'][1],
            self.overlay_data['width'],
            self.overlay_data['height']
        )

    def moveEvent(self, event):
        super().moveEvent(event)
        self.overlay_data['position'] = (self.pos().x(), self.pos().y())
        # Save updated data
        self.overlay_manager.save_overlay_data()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay_data['width'] = self.width()
        self.overlay_data['height'] = self.height()
        # Save updated data
        self.overlay_manager.save_overlay_data()
