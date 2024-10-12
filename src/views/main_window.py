# jetque/src/views/main_window.py

import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path
from .system_tray import SystemTrayIcon
from .home_view import HomeView
from .overlays_view import OverlaysView
from .triggers_view import TriggersView
from src.parsers.chat_log_parser import ChatLogParser
from src.parsers.dbg_log_parser import DBGLogParser
from src.events.event_handler import EventHandler
from src.events.event_factory import EventFactory

class ChatLogParsingThread(QThread):
    new_event_signal = pyqtSignal(str)

    def __init__(self, log_file_path):
        logging.debug("Here")
        super().__init__()
        self.log_file_path = log_file_path
        self.is_running = False
        self.chat_log_parser = None

    def run(self):
        """Start monitoring the log using the existing timer in ChatLogParser."""
        logging.debug("Here")
        self.is_running = True
        self.chat_log_parser = ChatLogParser(self.log_file_path, EventHandler(), EventFactory())
        self.chat_log_parser.monitor_log()  # This will start the parser's own timer
        self.exec()

    def stop(self):
        """Gracefully stop the parser."""
        logging.debug("Here")
        self.is_running = False
        if self.chat_log_parser:
            self.chat_log_parser.stop_monitoring()
        self.quit()

class DBGLogParsingThread(QThread):
    dbg_info_signal = pyqtSignal(str)  # Signal for emitting dbg-related events

    def __init__(self, log_file_path):
        logging.debug("Here")
        super().__init__()
        self.log_file_path = log_file_path
        self.is_running = False
        self.dbg_log_parser = None

    def run(self):
        """Start monitoring the log using the existing timer in DBGLogParser."""
        logging.debug("Here")
        self.is_running = True
        self.dbg_log_parser = DBGLogParser(self.log_file_path)
        self.dbg_log_parser.monitor_log()  # This will start the parser's own timer
        self.exec()

    def stop(self):
        """Gracefully stop the parser."""
        logging.debug("Here")
        self.is_running = False
        if self.dbg_log_parser:
            self.dbg_log_parser.stop_monitoring()
        self.quit()

class MainWindow(QMainWindow):
    def __init__(self):
        logging.debug("Here")
        super().__init__()
        self.setWindowTitle("JetQue")
        self.setGeometry(100, 100, 800, 600)
        self.chat_log_thread = None
        self.dbg_log_thread = None
        self.is_running = False
        self.setup_icon()
        self.setup_ui()
        self.setup_tray()
        self.setup_connections()

    def setup_icon(self):
        logging.debug("Here")
        current_dir = Path(__file__).parent
        icon_path = current_dir / 'resources' / 'JetQue_Icon.png'

        if icon_path.exists():
            icon = QIcon(str(icon_path))
            self.setWindowIcon(icon)
        else:
            self.setWindowIcon(QIcon.fromTheme("application-icon"))

    def setup_ui(self):
        logging.debug("Here")
        # Setup Menu Bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # Setup Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.home_view = HomeView()
        self.tabs.addTab(self.home_view, "Home")

        self.overlays_view = OverlaysView()
        self.tabs.addTab(self.overlays_view, "Overlays")

        self.triggers_view = TriggersView()
        self.tabs.addTab(self.triggers_view, "Triggers")

        # Add Play/Stop button at the top-right corner
        self.play_stop_button = QPushButton()
        self.set_play_button_icon()  # Initially set as Play button
        self.play_stop_button.clicked.connect(self.toggle_run_state)

        # Create a layout for the button at the top-right
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push button to the right
        button_layout.addWidget(self.play_stop_button)

        # Add the button layout above the tabs
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)  # Add button to top
        main_layout.addWidget(self.tabs)  # Tabs come below the button

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_play_button_icon(self):
        """Set the button icon to green play."""
        logging.debug("Here")
        play_icon = QIcon(str(Path(__file__).parent / 'resources' / 'play_icon.png'))
        self.play_stop_button.setIcon(play_icon)
        self.play_stop_button.setStyleSheet("background-color: green; border-radius: 10px;")

    def set_stop_button_icon(self):
        """Set the button icon to red stop."""
        logging.debug("Here")
        stop_icon = QIcon(str(Path(__file__).parent / 'resources' / 'stop_icon.png'))
        self.play_stop_button.setIcon(stop_icon)
        self.play_stop_button.setStyleSheet("background-color: red; border-radius: 10px;")

    def toggle_run_state(self):
        """Toggles the program's running state and updates the button."""
        logging.debug("Here")
        if self.is_running:
            self.is_running = False
            self.set_play_button_icon()
            if self.chat_log_thread:
                self.chat_log_thread.stop()
                self.chat_log_thread.wait()
                self.chat_log_thread = None
            if self.dbg_log_thread:
                self.dbg_log_thread.stop()
                self.dbg_log_thread.wait()
                self.dbg_log_thread = None
        else:
            self.is_running = True
            self.set_stop_button_icon()
            self.start_parsing()

    def start_parsing(self):
        logging.debug("Here")
        chat_log_file = self.home_view.config_data.get('char_file', '')
        dbg_log_file = self.home_view.config_data.get('dbg_file', '')

        if not chat_log_file or not dbg_log_file:
            print("Log file paths are not set properly. Please check your configuration.")
            return

        # Start the chat log parser thread
        self.chat_log_thread = ChatLogParsingThread(chat_log_file)
        self.chat_log_thread.new_event_signal.connect(self.handle_new_chat_event)
        self.chat_log_thread.start()

        # Start the dbg log parser thread
        self.dbg_log_thread = DBGLogParsingThread(dbg_log_file)
        self.dbg_log_thread.dbg_info_signal.connect(self.handle_new_dbg_event)
        self.dbg_log_thread.start()

    def handle_new_chat_event(self, event: str):
        """Handle a new chat log event."""
        logging.debug("Here")
        print(f"New chat event detected: {event}")

    def handle_new_dbg_event(self, info: str):
        """Handle new dbg information."""
        logging.debug("Here")
        print(f"New dbg info detected: {info}")

    def setup_tray(self):
        logging.debug("Here")
        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show()

    def setup_connections(self):
        logging.debug("Here")
        self.tray_icon.show_requested.connect(self.restore_window)

    def restore_window(self):
        logging.debug("Here")
        self.showNormal()
        self.show()
        self.raise_()
        self.activateWindow()

# Entry point for the application
def run_app():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    logging.debug("Here")
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
