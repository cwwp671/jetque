import sys
import logging

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QRectF, QPoint, QEvent
from PyQt6.QtGui import QFont, QCursor, QBrush
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsTextItem,
    QFrame,
    QMessageBox,
)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Initialize Scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Set Initial Window Properties
        self.setWindowTitle("PyQt6 Toggle Window")
        self.setGeometry(100, 100, 600, 400)

        # Hide Scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Remove QGraphicsView's frame to eliminate default outlines
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Add QGraphicsTextItem
        self.text_item = QGraphicsTextItem("Visible Text Only")
        font = QFont("Arial", 20)
        self.text_item.setFont(font)
        self.text_item.setDefaultTextColor(Qt.GlobalColor.white)
        self.text_item.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsMovable, False)
        self.text_item.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.text_item.setZValue(1)  # Ensure text is on top
        self.scene.addItem(self.text_item)

        # Center the text
        self.center_text()

        # State Variables
        self.is_configure = True  # Start in Configure state
        self.dragging = False
        self.resizing = False
        self.drag_position = QPoint()
        self.resize_margin = 10  # Margin in pixels for resizing

        # Initialize Window in Configure Mode
        self.initialize_configure_mode()

        # Enable mouse tracking
        self.setMouseTracking(True)

        # Install event filter (Optional)
        self.installEventFilter(self)

        # Show the window
        self.show()

    def initialize_configure_mode(self):
        """Initialize the window in Configure mode."""
        logging.debug("Initializing window in Configure mode.")
        try:
            # **Set Window Flags for Configure Mode**
            configure_flags = (
                    Qt.WindowType.Window
                    | Qt.WindowType.WindowSystemMenuHint
                    | Qt.WindowType.WindowMinMaxButtonsHint
                    | Qt.WindowType.WindowCloseButtonHint
            )
            self.setWindowFlags(configure_flags)
            logging.debug(f"Set window flags to: {self.windowFlags()}")

            # **Ensure Window Is Enabled**
            self.setEnabled(True)
            logging.debug("Enabled main window for mouse interaction")

            # **Set Window Opacity to Fully Opaque**
            self.setWindowOpacity(1.0)
            logging.debug("Set window opacity to 1.0")

            # Apply Configure Mode Stylesheet (Opaque Background)
            self.apply_configure_stylesheet()

            # Set Scene Background to Opaque Black
            # self.scene.setBackgroundBrush(QtGui.QBrush(Qt.GlobalColor.black))
            # self.scene.setBackgroundBrush(Qt.GlobalColor.black)
            logging.debug("Set scene background to opaque black")

            # Reset Cursor to Arrow
            # self.setCursor(Qt.CursorShape.ArrowCursor)
            # logging.debug("Reset cursor to ArrowCursor")

            # Force UI Update
            self.update()
            logging.debug("Forced UI update after initializing Configure mode")
        except Exception as e:
            logging.error(f"Error initializing Configure mode: {e}")
            raise

    def apply_configure_stylesheet(self):
        """Apply stylesheet for Configure state (opaque background)."""
        logging.debug("Applying Configure mode stylesheet.")
        self.setStyleSheet("""
            QGraphicsView {
                background-color: rgba(0, 0, 0, 255);  /* Make Black */
                border: none;  /* Remove any border */
            }
        """)

    def apply_transparent_stylesheet(self):
        """Apply stylesheet for Transparent state (fully transparent background)."""
        logging.debug("Applying Transparent mode stylesheet.")
        self.setStyleSheet("""
            QGraphicsView {
                background: transparent;  /* Make transparent */
                border: none;  /* Remove any border */
            }
        """)

    def center_text(self):
        """Center the text item in the scene."""
        logging.debug("Centering text.")
        self.scene.setSceneRect(QRectF(self.rect()))
        text_rect = self.text_item.boundingRect()
        view_rect = self.viewport().rect()
        center_x = (view_rect.width() - text_rect.width()) / 2
        center_y = (view_rect.height() - text_rect.height()) / 2
        self.text_item.setPos(center_x, center_y)
        logging.debug(f"Text positioned at: ({center_x}, {center_y})")

    def resizeEvent(self, event):
        """Handle window resizing to keep the text centered."""
        super().resizeEvent(event)
        self.center_text()

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_F12:
            logging.debug("F12 pressed. Toggling window state.")
            self.toggle_state()
        else:
            super().keyPressEvent(event)

    def toggle_state(self):
        """Toggle between Configure and Transparent states."""
        logging.debug(f"Toggling state. Current state: {'Configure' if self.is_configure else 'Transparent'}.")
        if self.is_configure:
            self.switch_to_transparent()
        else:
            self.switch_to_configure()

    def switch_to_transparent(self):
        """Configure the window to Transparent state."""
        logging.debug("Switching to Transparent mode.")
        try:
            # Hide window before changing flags
            self.is_configure = False
            self.hide()
            logging.debug("Window hidden before switching to Transparent mode.")

            # **Set Window Flags: Frameless and Always on Top**
            transparent_flags = (
                    Qt.WindowType.WindowTransparentForInput
                    | Qt.WindowType.Window
                    | Qt.WindowType.FramelessWindowHint
                    | Qt.WindowType.WindowStaysOnTopHint
            )
            self.setWindowFlags(transparent_flags)
            logging.debug(f"Set window flags to: {self.windowFlags()}")

            # **Apply Transparent Stylesheet**
            self.apply_transparent_stylesheet()

            # **Set Scene Background to Transparent**
            # self.scene.setBackgroundBrush()
            # self.scene.setBackgroundBrush(Qt.GlobalColor.transparent)
            logging.debug("Set scene background to transparent")

            # **Disable Mouse Tracking**
            # self.setMouseTracking(False)
            logging.debug("Disabled mouse tracking")

            # **Ensure Window is Opaque and Interactable**
            # self.setWindowOpacity(-1.0)
            # logging.debug("Set window opacity to 1.0")

            # Show window to apply changes
            self.show()
            logging.debug("Window shown after switching to Transparent mode.")

            # **Bring Window to Front and Activate**
            self.raise_()
            self.activateWindow()
            self.setFocus()
            logging.debug("Raised, activated, and focused the window in Transparent mode.")

            # Reset Cursor to Arrow (just in case)
            # self.setCursor(Qt.CursorShape.ArrowCursor)
            # logging.debug("Reset cursor to ArrowCursor in Transparent mode.")

            # Force UI Update
            self.update()
            logging.debug("Forced UI update after switching to Transparent mode.")
        except Exception as e:
            logging.error(f"Error switching to Transparent mode: {e}")
            raise

    def switch_to_configure(self):
        """Configure the window to Configure state."""
        logging.debug("Switching to Configure mode.")
        try:
            # Hide window before changing flags
            self.is_configure = True
            self.hide()
            logging.debug("Window hidden before switching to Configure mode.")

            # **Set Window Flags: Windowed with System Menu and Min/Max Buttons**
            configure_flags = (
                    Qt.WindowType.Window
                    | Qt.WindowType.WindowSystemMenuHint
                    | Qt.WindowType.WindowMinMaxButtonsHint
                    | Qt.WindowType.WindowCloseButtonHint
            )
            self.setWindowFlags(configure_flags)
            logging.debug(f"Set window flags to: {self.windowFlags()}")

            # **Ensure Window Is Enabled**
            self.setEnabled(True)
            logging.debug("Enabled main window for mouse interaction")

            # **Apply Opaque Stylesheet**
            self.apply_configure_stylesheet()

            # **Set Scene Background to Opaque Black**
            # self.scene.setBackgroundBrush(QtGui.QBrush(Qt.GlobalColor.black))
            # self.scene.setBackgroundBrush(Qt.GlobalColor.black)
            logging.debug("Set scene background to opaque black")

            # **Enable Mouse Tracking**
            # self.setMouseTracking(True)
            logging.debug("Enabled mouse tracking")

            # **Ensure Window is Opaque and Interactable**
            self.setWindowOpacity(1.0)
            logging.debug("Set window opacity to 1.0")

            # Show window to apply changes
            self.show()
            logging.debug("Window shown after switching to Configure mode.")

            # **Bring Window to Front and Activate**
            self.raise_()
            self.activateWindow()
            self.setFocus()
            logging.debug("Raised, activated, and focused the window in Configure mode.")

            # Reset Cursor to Arrow
            self.setCursor(Qt.CursorShape.ArrowCursor)
            logging.debug("Reset cursor to ArrowCursor in Configure mode.")

            # Force UI Update
            self.update()
            logging.debug("Forced UI update after switching to Configure mode.")
        except Exception as e:
            logging.error(f"Error switching to Configure mode: {e}")
            raise

    def mousePressEvent(self, event):
        """Handle mouse press events for dragging and resizing."""
        logging.debug("mousePressEvent triggered.")
        if not self.is_configure:
            logging.debug("Mouse press ignored in Transparent mode.")
            return  # Do nothing in Transparent state

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            rect = self.rect()
            # Check if near the bottom-right corner for resizing
            if pos.x() >= rect.width() - self.resize_margin and pos.y() >= rect.height() - self.resize_margin:
                self.resizing = True
                logging.debug("Resizing initiated.")
            else:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                logging.debug("Dragging initiated.")
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging and resizing."""
        logging.debug("mouseMoveEvent triggered.")
        if not self.is_configure:
            return  # Do nothing in Transparent mode

        pos = event.position().toPoint()
        rect = self.rect()

        if self.resizing:
            # Calculate new size based on mouse position
            new_width = event.globalPosition().toPoint().x() - self.frameGeometry().topLeft().x()
            new_height = event.globalPosition().toPoint().y() - self.frameGeometry().topLeft().y()
            # Set minimum size to prevent too small window
            new_width = max(new_width, 200)
            new_height = max(new_height, 100)
            self.setFixedSize(new_width, new_height)
            self.center_text()
            logging.debug(f"Resizing to width: {new_width}, height: {new_height}.")
            event.accept()
            return

        if self.dragging:
            # Move window based on mouse movement
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            logging.debug(f"Moving window to position: {new_pos}.")
            event.accept()
            return

        # Change cursor if near the bottom-right corner for resizing
        if (
                pos.x() >= rect.width() - self.resize_margin and
                pos.y() >= rect.height() - self.resize_margin
        ):
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        logging.debug("mouseReleaseEvent triggered.")
        if not self.is_configure:
            return  # Do nothing in Transparent mode

        if event.button() == Qt.MouseButton.LeftButton:
            if self.dragging:
                logging.debug("Dragging ended.")
            if self.resizing:
                logging.debug("Resizing ended.")
            self.dragging = False
            self.resizing = False
            event.accept()

    def add_label(self, text):
        """Add an additional label to the scene."""
        label = QGraphicsTextItem(text)
        font = QFont("Arial", 16)
        label.setFont(font)
        label.setDefaultTextColor(Qt.GlobalColor.white)
        label.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsMovable, False)
        label.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable, False)
        label.setZValue(1)
        self.scene.addItem(label)
        # Position the label at a predefined location
        label.setPos(50, 50)  # Example position
        logging.debug(f"Added label with text: {text}")

    def event(self, event):
        """Override the event method to manage mouse events more granularly."""
        if event.type() in [QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, QEvent.Type.MouseMove]:
            if not self.is_configure:
                logging.debug(f"Event {event.type()} ignored in Transparent mode.")
                return True  # Event handled (ignored)
        return super().event(event)

    def eventFilter(self, source, event):
        """Optional: Implement an event filter to intercept mouse events."""
        if not self.is_configure:
            if event.type() in [QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, QEvent.Type.MouseMove]:
                logging.debug(f"Event {event.type()} filtered out in Transparent mode.")
                return True  # Event handled (ignored)
        return super().eventFilter(source, event)


def main():
    app = QApplication(sys.argv)

    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    window = MainWindow()

    # Example: Add an additional label (optional)
    # window.add_label("Another Label")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
