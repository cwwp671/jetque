# jetque/src/views/system_tray.py

import signal
import atexit
import logging
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication
from PyQt6.QtGui import QIcon, QAction, QMouseEvent, QCursor
from PyQt6.QtCore import pyqtSignal, QEvent, Qt
from pathlib import Path
import sys
import os


class SystemTrayIcon(QSystemTrayIcon):
    show_requested = pyqtSignal()

    def __init__(self, parent=None):
        logging.debug("Here")
        super().__init__(parent)
        self.parent = parent
        self.setup_icon()
        self.setup_menu()
        self.activated.connect(self.on_tray_activated)

        self.tray_cleaned = False

        # Handle app quitting via PyQt's aboutToQuit signal
        QApplication.instance().aboutToQuit.connect(self.cleanup_tray_icon)

        # Register cleanup functions for system signals
        atexit.register(self.cleanup_tray_icon)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def setup_icon(self):
        logging.debug("Here")
        # Determine the absolute path to the icon
        current_dir = Path(__file__).parent.resolve()
        icon_path = current_dir / 'resources' / 'JetQue_Icon.png'

        if icon_path.exists():
            icon = QIcon(str(icon_path))
        else:
            # Fallback to a default system icon if JetQue_Icon.png is not found
            icon = QIcon.fromTheme("application-icon")
            logging.warning(f"Warning: Icon file not found at {icon_path}. Using default icon.")

        self.setIcon(icon)
        self.setToolTip("JetQue")

    def setup_menu(self):
        logging.debug("Here")
        menu = QMenu(self.parent)

        show_action = QAction("Show", self.parent)
        quit_action = QAction("Quit", self.parent)

        menu.addAction(show_action)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

        # Connect actions
        show_action.triggered.connect(self.on_show)
        quit_action.triggered.connect(self.on_quit)

    def on_tray_activated(self, reason):
        logging.debug("Here")
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Single left click
            self.on_show()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:  # Double click
            self.on_show()
        elif reason == QSystemTrayIcon.ActivationReason.Context:  # Right-click
            if self.contextMenu():
                self.contextMenu().exec(QCursor.pos())
            else:
                logging.warning("No context menu available")

    def on_show(self):
        logging.debug("Here")
        self.show_requested.emit()
        self.parent.show()
        self.parent.raise_()
        self.parent.activateWindow()

    def on_quit(self):
        logging.debug("Here")
        self.cleanup_tray_icon()  # Hide the tray icon
        QApplication.quit()  # Directly quit the application

    def cleanup_tray_icon(self):
        logging.debug("Here")
        # Prevent cleanup from happening multiple times
        if not self.tray_cleaned:
            logging.debug("Cleaning up system tray icon")
            self.hide()  # Hide the tray icon
            self.tray_cleaned = True  # Set flag to True after cleanup

    def signal_handler(self, sig, frame):
        logging.debug("Here")
        logging.debug(f"Received signal {sig}, cleaning up system tray icon")
        self.cleanup_tray_icon()
        QApplication.quit()  # Exit the application cleanly

    def show_message(self, title: str, message: str):
        logging.debug("Here")
        self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 3000)

